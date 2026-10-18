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

	def organize_tasks(self, owner: Owner) -> list[Task]:
		"""Return all pet tasks ordered by scheduled time."""
		return sorted(self.get_all_tasks(owner), key=lambda task: task.time)

	def mark_task_complete(self, task: Task) -> None:
		"""Mark the given task as completed."""
		task.completed = True
