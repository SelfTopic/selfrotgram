import importlib
import sys
from abc import ABC
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Generic, List, Optional, Sequence, Set, Type, Union

from ..context.context import TContext
from ..exceptions import DefinitionError, RouterError
from ..handlers import BaseHandler
from ..middleware import BaseMiddleware


@dataclass
class _Match:
    path: List["BaseRouter[Any]"]
    handler: BaseHandler[Any]


_building: List[type] = []


def _load_router(path: str, package: Optional[str]) -> Any:
    if path.startswith(".") and not package:
        raise RouterError(
            f"auto_connect: путь {path!r} относительный, а у роутера нет пакета"
        )

    try:
        module = importlib.import_module(path, package=package)
    except ModuleNotFoundError as e:
        raise RouterError(f"auto_connect: не удалось импортировать {path!r}: {e}") from e

    if not hasattr(module, "router"):
        raise RouterError(f"auto_connect: в модуле {module.__name__!r} нет объекта `router`")

    return module.router


async def _run_middlewares(
    middlewares: Sequence[Type[BaseMiddleware[Any]]],
    ctx: Any,
    inner: Callable[[], Awaitable[None]],
) -> None:
    called_middlewares: List[BaseMiddleware[Any]] = []
    passed = True
    exc: Optional[BaseException] = None

    try:
        # pre_handle тоже внутри try: если он упал у третьей мидлвари, первые
        # две уже открыли ресурсы (сессию БД), и их post_handle обязан отработать.
        # Сама упавшая мидлварь в called_middlewares не попадает.
        for middleware in middlewares:
            called_middleware = middleware(ctx)
            # Без create_task: pre_handle, handle и post_handle работают в одной задаче,
            # поэтому ContextVar, выставленный в pre_handle (сессия БД у DI), виден в
            # хендлере, а reset() в post_handle проходит (токен создан в том же контексте).
            pre = await called_middleware.pre_handle()

            if pre != True:
                passed = False
                break

            called_middlewares.append(called_middleware)

        if passed:
            await inner()
    except BaseException as e:
        exc = e
        raise
    finally:
        # post_handle обязан отработать даже если handle() упал —
        # иначе мидлварь вроде DatabaseMiddleware никогда не закроет
        # сессию и будет копить утечки при любой ошибке в хендлере.
        # exc передаём явно, чтобы post_handle мог отличить
        # commit-путь от rollback-пути, а не гадать.
        for middleware in reversed(called_middlewares):
            await middleware.post_handle(exc)


async def _run_path(
    routers: List["BaseRouter[Any]"], handler: BaseHandler[Any], ctx: Any
) -> None:
    if not routers:
        await handler.pre_handle()
        await handler.handle()
        return

    head, *rest = routers
    await _run_middlewares(head.middlewares, ctx, lambda: _run_path(rest, handler, ctx))


class BaseRouter(ABC, Generic[TContext]):
    """
    Дерево роутеров: у каждого свои handlers, middlewares и вложенные routers.

    Порядок поиска хендлера: сначала собственные handlers роутера (по порядку
    в списке), потом вложенные routers (по порядку, вглубь). Апдейт забирает
    первый подошедший.

    Мидлвари корня (Dispatcher) — внешние: срабатывают на каждый апдейт.
    Мидлвари вложенного роутера — внутренние: только вокруг хендлера,
    найденного в его поддереве (от внешнего роутера к внутреннему), а не на
    каждый апдейт, который мог бы сюда попасть.
    """

    context: Type[TContext]
    # Кортежи: неизменяемые, поэтому общие для всех экземпляров безопасно,
    # и линтеру не за что ругаться (RUF012). register_* пересобирают кортеж
    # у экземпляра, класс не трогают.
    handlers: Sequence[Type[BaseHandler[Any]]] = ()
    middlewares: Sequence[Type[BaseMiddleware[Any]]] = ()
    routers: Sequence[Type["BaseRouter[Any]"]] = ()
    auto_connect: Sequence[str] = ()

    def __init__(self) -> None:
        super().__init__()
        self._children: List[BaseRouter[Any]] = []

        # Порядок подключения: routers, затем auto_connect, затем register_routers().
        _building.append(type(self))
        try:
            for router in self.routers:
                self.register_router(router)

            package = self._auto_connect_package()
            for path in self.auto_connect:
                self.register_router(_load_router(path, package))

            self.register_routers()
        finally:
            _building.pop()

    @property
    def children(self) -> List["BaseRouter[Any]"]:
        return list(self._children)

    def used_update_types(self) -> Set[str]:
        """Поля Update, на которые есть хендлеры в этом роутере и ниже."""
        used = {handler.update_field for handler in self.handlers}
        for child in self._children:
            used |= child.used_update_types()

        return used

    def register_handler(self, handler: Type[BaseHandler[Any]]) -> None:
        self.handlers = (*self.handlers, handler)

    def register_middleware(self, middleware: Type[BaseMiddleware[Any]]) -> None:
        self.middlewares = (*self.middlewares, middleware)

    def register_routers(self) -> None:
        """Переопределяется в наследнике: self.register_router(...) по одному."""

    def register_router(self, router: Union[Type["BaseRouter[Any]"], "BaseRouter[Any]"]) -> None:
        if isinstance(router, type) and issubclass(router, BaseRouter):
            if router in _building:
                chain = " -> ".join(c.__name__ for c in [*_building, router])
                raise RouterError(f"Цикл в дереве роутеров: {chain}")
            router = router()

        if not isinstance(router, BaseRouter):
            raise DefinitionError(
                f"{type(self).__name__}: router должен быть классом или экземпляром "
                f"BaseRouter, получено {router!r}"
            )

        self._children.append(router)

    def _auto_connect_package(self) -> Optional[str]:
        # Относительные пути считаются от пакета модуля, где объявлен auto_connect.
        for klass in type(self).__mro__:
            if "auto_connect" in klass.__dict__:
                return getattr(sys.modules.get(klass.__module__), "__package__", None)

        return None

    async def _find(
        self, ctx: Any, path: List["BaseRouter[Any]"]
    ) -> Optional[_Match]:
        path = [*path, self]

        for handler_type in self.handlers:
            handler = handler_type(ctx)
            if handler.check_type_ctx() and await handler.filter():
                return _Match(path, handler)

        for child in self._children:
            match = await child._find(ctx, path)
            if match is not None:
                return match

        return None

    async def propagate(self, ctx: TContext) -> None:
        found: List[BaseHandler[Any]] = []

        async def route() -> None:
            match = await self._find(ctx, [])
            if match is not None:
                found.append(match.handler)
                await _run_path(match.path[1:], match.handler, ctx)

        try:
            await _run_middlewares(self.middlewares, ctx, route)
        except Exception as exc:
            # К этому моменту post_handle всех мидлварей уже отработал (сессия БД
            # откатилась). Если хендлер был найден, первым ошибку видит он: вернулся
            # нормально — обработано, иначе (по умолчанию он делает raise) ошибка
            # идёт выше, в on_error диспетчера.
            if not found:
                raise

            await found[0].on_error(exc)
