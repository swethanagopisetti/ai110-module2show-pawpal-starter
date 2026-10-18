from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time as time_type, timedelta


@dataclass
class Task:
	description: str
	time: time_type
	frequency: str
	completed: bool = False
	due_date: date = field(default_factory=date.today)

	def mark_complete(self) -> None:
		"""Mark this task as completed."""
		self.completed = True


@dataclass
class Pet:
	name: str
	species: str
	breed: str = ""
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a task to this pet's care list."""
		self.tasks.append(task)


@dataclass
class Owner:
	name: str
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this owner's household."""
		self.pets.append(pet)

	def get_all_tasks(self) -> list[Task]:
		"""Return the tasks belonging to all of this owner's pets."""
		return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
	def get_all_tasks(self, owner: Owner) -> list[Task]:
		"""Retrieve all tasks through the owner."""
		return owner.get_all_tasks()

	def filter_tasks(
		self,
		owner: Owner,
		completed: bool | None = None,
		pet_name: str | None = None,
	) -> list[Task]:
		"""Filter tasks by completion status, pet name, or both."""
		return [
			task
			for pet in owner.pets
			if pet_name is None or pet.name.casefold() == pet_name.casefold()
			for task in pet.tasks
			if completed is None or task.completed is completed
		]

	def sort_by_time(self, tasks: list[Task]) -> list[Task]:
		"""Return tasks ordered by their scheduled time."""
		return sorted(tasks, key=lambda task: task.time.strftime("%H:%M"))

	def organize_tasks(self, owner: Owner) -> list[Task]:
		"""Return all pet tasks ordered by scheduled time."""
		return self.sort_by_time(self.get_all_tasks(owner))

	def detect_conflicts(self, owner: Owner) -> list[str]:
		"""Return warnings for tasks sharing a due date and scheduled time."""
		scheduled_tasks = [
			(pet, task)
			for pet in owner.pets
			for task in pet.tasks
		]
		warnings = []

		for index, (pet, task) in enumerate(scheduled_tasks):
			for other_pet, other_task in scheduled_tasks[index + 1:]:
				if task is other_task:
					continue
				if task.due_date != other_task.due_date or task.time != other_task.time:
					continue

				pet_scope = "the same pet" if pet is other_pet else "different pets"
				warnings.append(
					f"Warning: {task.description} ({pet.name}) and "
					f"{other_task.description} ({other_pet.name}) are scheduled for "
					f"{task.time.strftime('%H:%M')} on {task.due_date} for {pet_scope}."
				)

		return warnings

	def mark_task_complete(self, owner: Owner, task: Task) -> Task | None:
		"""Complete a task and schedule its next recurring occurrence."""
		pet = next(
			(
				pet
				for pet in owner.pets
				if any(pet_task is task for pet_task in pet.tasks)
			),
			None,
		)
		if pet is None:
			raise ValueError("Task does not belong to a pet in this owner.")
		if task.completed:
			return None

		task.mark_complete()
		frequency = task.frequency.casefold()
		if frequency not in {"daily", "weekly"}:
			return None

		days_until_next = 1 if frequency == "daily" else 7
		next_due_date = date.today() + timedelta(days=days_until_next)
		next_task = Task(
			task.description,
			task.time,
			task.frequency,
			due_date=next_due_date,
		)
		pet.add_task(next_task)
		return next_task
