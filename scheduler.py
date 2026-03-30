"""Builds a DailyPlan from owner constraints, pet context, and tasks."""

from __future__ import annotations

from owner import Owner
from pet import Pet
from plan import DailyPlan, PlanItem
from task import Task


class Scheduler:
    def schedule(self, owner: Owner, pet: Pet, tasks: list[Task]) -> DailyPlan:
        ordered = self._sort_tasks(tasks, owner)
        scheduled_items, not_scheduled, total_minutes = self._pack_tasks(
            ordered, owner.available_minutes
        )
        n_sched = len(scheduled_items)
        n_skip = len(not_scheduled)
        summary = (
            f"Plan for {pet.name} ({pet.species}): {n_sched} task(s) scheduled, "
            f"{total_minutes} min of {owner.available_minutes} min available for {owner.name}."
        )
        if n_skip:
            summary += f" {n_skip} task(s) did not fit the time budget."
        return DailyPlan(scheduled_items, not_scheduled, total_minutes, summary)

    def _priority_rank(self, priority: str) -> int:
        ranks = {"low": 0, "medium": 1, "high": 2}
        return ranks.get(priority.strip().lower(), 0)

    def _preference_index(self, title: str, owner: Owner) -> int:
        try:
            return owner.preferred_task_order.index(title)
        except ValueError:
            return len(owner.preferred_task_order)

    def _sort_tasks(self, tasks: list[Task], owner: Owner) -> list[Task]:
        return sorted(
            tasks,
            key=lambda t: (
                -self._priority_rank(t.priority),
                self._preference_index(t.title, owner),
                t.title,
            ),
        )

    def _pack_tasks(
        self, sorted_tasks: list[Task], budget: int
    ) -> tuple[list[PlanItem], list[Task], int]:
        scheduled: list[PlanItem] = []
        not_scheduled: list[Task] = []
        total = 0
        start_minute = 0
        for task in sorted_tasks:
            remaining = budget - total
            if task.duration_minutes <= remaining:
                order = len(scheduled) + 1
                reason = (
                    f"{task.priority.capitalize()} priority; "
                    f"placed by owner preference among same-priority tasks; "
                    f"fits {task.duration_minutes} min with {remaining} min left in budget; "
                    f"starts at minute {start_minute}."
                )
                scheduled.append(
                    PlanItem(task, order, start_minute, reason)
                )
                start_minute += task.duration_minutes
                total += task.duration_minutes
            else:
                not_scheduled.append(task)
        return scheduled, not_scheduled, total
