import pytest

from owner import Owner
from pet import Pet
from scheduler import Scheduler
from task import Task


def _run_schedule(owner: Owner, pet: Pet, tasks: list[Task]):
    return Scheduler().schedule(owner, pet, tasks)


def test_priority_sorting_schedules_high_then_medium_then_low():
    owner = Owner(name="Jordan", available_minutes=200, preferred_task_order=[])
    pet = Pet(name="Mochi", species="dog")

    tasks = [
        Task(title="Walk", duration_minutes=20, priority="low"),
        Task(title="Play", duration_minutes=30, priority="high"),
        Task(title="Groom", duration_minutes=10, priority="medium"),
    ]

    plan = _run_schedule(owner, pet, tasks)

    assert [i.task.title for i in plan.scheduled_items] == ["Play", "Groom", "Walk"]
    assert plan.not_scheduled == []
    assert plan.total_scheduled_minutes == 60


def test_preference_tie_break_schedules_by_owner_preferred_order():
    owner = Owner(
        name="Jordan",
        available_minutes=100,
        preferred_task_order=["Feed", "Walk"],  # Feed should come first
    )
    pet = Pet(name="Mochi", species="dog")

    tasks = [
        Task(title="Walk", duration_minutes=15, priority="high"),
        Task(title="Feed", duration_minutes=10, priority="high"),
    ]

    plan = _run_schedule(owner, pet, tasks)

    assert [i.task.title for i in plan.scheduled_items] == ["Feed", "Walk"]
    assert plan.total_scheduled_minutes == 25


def test_budget_greedy_packing_schedules_what_fits_and_moves_others_to_not_scheduled():
    owner = Owner(name="Jordan", available_minutes=30, preferred_task_order=[])
    pet = Pet(name="Mochi", species="dog")

    # Sorted by priority: A(high, 20), B(medium, 15), C(low, 10)
    # Budget 30 => after A, 10 minutes left => B does not fit, C fits.
    tasks = [
        Task(title="B", duration_minutes=15, priority="medium"),
        Task(title="C", duration_minutes=10, priority="low"),
        Task(title="A", duration_minutes=20, priority="high"),
    ]

    plan = _run_schedule(owner, pet, tasks)

    assert [i.task.title for i in plan.scheduled_items] == ["A", "C"]
    assert [t.title for t in plan.not_scheduled] == ["B"]
    assert plan.total_scheduled_minutes == 30


def test_start_minute_and_order_are_accumulated_sequentially():
    owner = Owner(name="Jordan", available_minutes=50, preferred_task_order=[])
    pet = Pet(name="Mochi", species="dog")

    tasks = [
        Task(title="A", duration_minutes=10, priority="high"),
        Task(title="B", duration_minutes=15, priority="high"),
        Task(title="C", duration_minutes=5, priority="low"),
    ]

    plan = _run_schedule(owner, pet, tasks)

    scheduled = plan.scheduled_items
    assert [i.order for i in scheduled] == [1, 2, 3]
    assert [i.start_minute for i in scheduled] == [0, 10, 25]


def test_planitem_reason_mentions_priority_and_start_minute():
    owner = Owner(name="Jordan", available_minutes=25, preferred_task_order=[])
    pet = Pet(name="Mochi", species="dog")

    tasks = [
        Task(title="Walk", duration_minutes=20, priority="high"),
        Task(title="Feed", duration_minutes=10, priority="low"),  # doesn't fit
    ]

    plan = _run_schedule(owner, pet, tasks)
    assert len(plan.scheduled_items) == 1

    reason = plan.scheduled_items[0].reason
    assert "High priority" in reason
    assert "starts at minute 0" in reason

