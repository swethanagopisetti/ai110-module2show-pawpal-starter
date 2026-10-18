from datetime import date, time

import pawpal_system
from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_complete_updates_status() -> None:
	task = Task("Morning walk", time(8, 0), "daily")

	task.mark_complete()

	assert task.completed is True


def test_pet_add_task_increases_task_count() -> None:
	pet = Pet("Mochi", "cat")
	task = Task("Breakfast", time(7, 30), "daily")
	initial_task_count = len(pet.tasks)

	pet.add_task(task)

	assert len(pet.tasks) == initial_task_count + 1


def test_scheduler_sort_by_time_orders_tasks_chronologically() -> None:
	tasks = [
		Task("Evening feeding", time(18, 0), "daily"),
		Task("Breakfast", time(7, 30), "daily"),
		Task("Morning walk", time(8, 0), "daily"),
	]

	result = Scheduler().sort_by_time(tasks)

	assert [task.description for task in result] == [
		"Breakfast",
		"Morning walk",
		"Evening feeding",
	]


def test_scheduler_filter_tasks_by_status_and_pet_name() -> None:
	mochi = Pet("Mochi", "cat")
	biscuit = Pet("Biscuit", "dog")
	completed_task = Task("Breakfast", time(7, 30), "daily", completed=True)
	uncompleted_task = Task("Medication", time(8, 0), "daily")
	mochi.tasks.extend([completed_task, uncompleted_task])
	biscuit.add_task(Task("Walk", time(9, 0), "daily", completed=True))
	owner = Owner("Jordan", [mochi, biscuit])

	result = Scheduler().filter_tasks(owner, completed=True, pet_name="MOCHI")

	assert result == [completed_task]


def test_scheduler_completion_creates_next_daily_and_weekly_tasks(monkeypatch) -> None:
	class FixedDate(date):
		@classmethod
		def today(cls):
			return cls(2024, 2, 28)

	monkeypatch.setattr(pawpal_system, "date", FixedDate)
	expected_dates = {
		"daily": date(2024, 2, 29),
		"weekly": date(2024, 3, 6),
	}

	for frequency in ("daily", "weekly"):
		pet = Pet("Mochi", "cat")
		task = Task("Medication", time(8, 0), frequency)
		pet.add_task(task)
		owner = Owner("Jordan", [pet])

		next_task = Scheduler().mark_task_complete(owner, task)

		assert task.completed is True
		assert next_task is not None
		assert next_task is not task
		assert next_task.description == task.description
		assert next_task.time == task.time
		assert next_task.frequency == frequency
		assert next_task.due_date == expected_dates[frequency]
		assert next_task.completed is False
		assert pet.tasks == [task, next_task]


def test_scheduler_completion_does_not_repeat_one_time_or_completed_tasks() -> None:
	pet = Pet("Mochi", "cat")
	task = Task("Vet visit", time(8, 0), "once")
	pet.add_task(task)
	owner = Owner("Jordan", [pet])
	scheduler = Scheduler()

	assert scheduler.mark_task_complete(owner, task) is None
	assert scheduler.mark_task_complete(owner, task) is None
	assert pet.tasks == [task]


def test_scheduler_detect_conflicts_for_same_pet_and_different_pets() -> None:
	mochi = Pet("Mochi", "cat")
	biscuit = Pet("Biscuit", "dog")
	mochi.add_task(Task("Breakfast", time(8, 0), "daily"))
	mochi.add_task(Task("Medication", time(8, 0), "daily"))
	biscuit.add_task(Task("Walk", time(8, 0), "daily"))
	owner = Owner("Jordan", [mochi, biscuit])

	warnings = Scheduler().detect_conflicts(owner)

	assert len(warnings) == 1
	assert any("for the same pet" in warning for warning in warnings)
	assert any("for different pets" in warning for warning in warnings)
	assert "Breakfast (Mochi)" in warnings[0]
	assert "Medication (Mochi)" in warnings[0]
	assert "Walk (Biscuit)" in warnings[0]
	assert all(warning.startswith("Warning:") for warning in warnings)


def test_scheduler_detect_conflicts_returns_empty_list_when_clear() -> None:
	pet = Pet("Mochi", "cat")
	pet.add_task(Task("Breakfast", time(8, 0), "daily"))
	pet.add_task(Task("Dinner", time(18, 0), "daily"))
	owner = Owner("Jordan", [pet])

	assert Scheduler().detect_conflicts(owner) == []
