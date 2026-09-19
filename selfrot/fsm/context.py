from typing import Any, cast, overload

from pydantic import BaseModel, ValidationError

from ..exceptions import FSMError
from .state import State, TModel
from .storage import Storage, StoredState


class FSM:
    """
    Состояние диалога одного пользователя в одном чате (ключ задаёт
    Dispatcher.fsm_key). Сам ничего не хранит: это ручка к хранилищу диспетчера,
    на каждый апдейт создаётся заново. Берётся из контекста: ctx.fsm.
    """

    def __init__(self, storage: Storage, key: str | None) -> None:
        self._storage = storage
        self._key = key

    def _require_key(self) -> str:
        if self._key is None:
            raise FSMError(
                "У этого апдейта нет ни чата, ни пользователя, поэтому состояние "
                "некуда привязать (переопределите Dispatcher.fsm_key)"
            )

        return self._key

    async def state(self) -> str | None:
        """Имя текущего состояния или None. Без ключа тоже None: «состояния нет»."""
        if self._key is None:
            return None

        stored = await self._storage.load(self._key)
        return stored.name if stored else None

    @overload
    async def set(self, state: State[None]) -> None: ...

    @overload
    async def set(self, state: State[TModel], data: TModel) -> None: ...

    async def set(self, state: State[Any], data: BaseModel | None = None) -> None:
        """Перейти в состояние; у состояния с данными их нужно передать."""
        key = self._require_key()
        if state.model is None:
            if data is not None:
                raise FSMError(f"{state}: у состояния нет данных, а переданы {data!r}")
        elif not isinstance(data, state.model):
            raise FSMError(
                f"{state}: нужны данные {state.model.__name__}, получено {data!r}"
            )

        payload = data.model_dump(mode="json") if data is not None else None
        await self._storage.save(key, StoredState(state.name, payload))

    async def get(self, state: State[TModel]) -> TModel:
        """
        Данные текущего состояния, уже типизированные. Вызывается в хендлере с
        InState(state); в другом состоянии (или если оно истекло) — FSMError.
        """
        key = self._require_key()
        stored = await self._storage.load(key)
        if stored is None or stored.name != state.name:
            now = stored.name if stored else "нет состояния"
            raise FSMError(f"Ожидалось {state}, а сейчас: {now}")

        if state.model is None:
            raise FSMError(f"{state}: у состояния нет данных")

        try:
            return cast(TModel, state.model.model_validate(stored.data))
        except ValidationError as e:
            raise FSMError(
                f"{state}: сохранённые данные не подходят {state.model.__name__}"
            ) from e

    async def clear(self) -> None:
        """Выйти из диалога: состояние и данные удаляются."""
        await self._storage.delete(self._require_key())
