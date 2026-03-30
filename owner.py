"""Owner context and scheduling constraints."""


class Owner:
    def __init__(
        self,
        name: str,
        available_minutes: int,
        preferred_task_order: list[str],
    ) -> None:
        self.name = name
        self.available_minutes = available_minutes
        self.preferred_task_order = preferred_task_order
