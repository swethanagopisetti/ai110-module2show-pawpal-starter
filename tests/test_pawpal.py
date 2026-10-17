from datetime import time

from pawpal_system import Pet, Task


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
