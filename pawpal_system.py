from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time as time_type


@dataclass
class Task:
	description: str
	time: time_type
	frequency: str
	completed: bool = False

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

	def mark_task_complete(self, task: Task) -> None:
		"""Mark the given task as completed."""
		task.completed = True
