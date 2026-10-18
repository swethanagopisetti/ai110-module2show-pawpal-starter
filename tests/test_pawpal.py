from datetime import time

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
