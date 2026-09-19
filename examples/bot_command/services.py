import random
from typing import Dict, List, Optional

DEFAULT_PHRASES: Dict[str, List[str]] = {
    "bot": [
        "Ты шото хотел?",
        "Чо надо?",
        "Ну я",
        "Чо?",
        "Тут я",
        "Ась?",
        "Чего?",
        "Ну, говори.",
    ],
}


class DialogService:
    def __init__(self, phrases: Optional[Dict[str, List[str]]] = None) -> None:
        self.phrases = phrases if phrases is not None else DEFAULT_PHRASES

    def random(self, key: str) -> str:
        return random.choice(self.phrases[key])
