"""Schedule output: plan items and tasks that did not fit."""

from __future__ import annotations

from task import Task


class PlanItem:
    def __init__(
        self,
        task: Task,
        order: int,
        start_minute: int,
        reason: str,
    ) -> None:
        self.task = task
        self.order = order
        self.start_minute = start_minute
        self.reason = reason


class DailyPlan:
    def __init__(
        self,
        scheduled_items: list[PlanItem],
        not_scheduled: list[Task],
        total_scheduled_minutes: int,
        summary: str,
    ) -> None:
        self.scheduled_items = scheduled_items
        self.not_scheduled = not_scheduled
        self.total_scheduled_minutes = total_scheduled_minutes
        self.summary = summary
