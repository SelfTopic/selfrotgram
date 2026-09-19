from typing import Any, Generic, TypeVar, overload

from pydantic import BaseModel

from ..exceptions import DefinitionError

TModel = TypeVar("TModel", bound=BaseModel)
TData = TypeVar("TData", bound="BaseModel | None")


class State(Generic[TData]):
    """
    Одно состояние диалога. Несёт тип данных, которые к нему привязаны:

        class Register(States):
            name = State()                 # данных нет
            age = State(AgeStep)           # данные — модель pydantic
            confirm = State(ConfirmStep)

    Тип виден проверке типов: fsm.set(Register.age, AgeStep(...)) принимает только
    AgeStep, а fsm.get(Register.age) возвращает AgeStep без cast и проверок.
    """

    name: str
    model: type[BaseModel] | None

    @overload
    def __init__(self: "State[None]") -> None: ...

    @overload
    def __init__(self: "State[TModel]", model: type[TModel]) -> None: ...

    def __init__(self, model: type[BaseModel] | None = None) -> None:
        self.model = model
        self.name = ""

    def __set_name__(self, owner: type, attr: str) -> None:
        if not issubclass(owner, States):
            raise DefinitionError(
                f"State {attr!r} объявлен в {owner.__name__}, а нужен подкласс States"
            )

        # Полное имя вместе с модулем: одноимённые группы в разных модулях не путаются.
        self.name = f"{owner.__module__}.{owner.__qualname__}:{attr}"

    def __repr__(self) -> str:
        return f"State({self.name})"


class States:
    """Группа состояний одного сценария: class Register(States): name = State()."""

    @classmethod
    def all(cls) -> tuple[State[Any], ...]:
        return tuple(v for v in vars(cls).values() if isinstance(v, State))
