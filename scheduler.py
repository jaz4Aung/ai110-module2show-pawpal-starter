"""Builds a DailyPlan from owner constraints, pet context, and tasks."""

from __future__ import annotations

from owner import Owner
from pet import Pet
from plan import DailyPlan, PlanItem
from task import Task


class Scheduler:
    def schedule(self, owner: Owner, pet: Pet, tasks: list[Task]) -> DailyPlan:
        raise NotImplementedError

    def _priority_rank(self, priority: str) -> int:
        raise NotImplementedError

    def _sort_tasks(self, tasks: list[Task], owner: Owner) -> list[Task]:
        raise NotImplementedError

    def _pack_tasks(
        self, sorted_tasks: list[Task], budget: int
    ) -> tuple[list[PlanItem], list[Task], int]:
        raise NotImplementedError
