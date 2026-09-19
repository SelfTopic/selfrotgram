from selfrot import BaseRouter

from .dispatcher import AppDispatcher


def show(router: BaseRouter, depth: int = 0) -> None:
    middlewares = ", ".join(m.__name__ for m in router.middlewares)
    suffix = f"  [{middlewares}]" if middlewares else ""
    print("  " * depth + type(router).__name__ + suffix)

    for child in router.children:
        show(child, depth + 1)


if __name__ == "__main__":
    show(AppDispatcher())
