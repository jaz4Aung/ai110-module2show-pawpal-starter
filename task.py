"""A single pet care task."""


class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str) -> None:
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
