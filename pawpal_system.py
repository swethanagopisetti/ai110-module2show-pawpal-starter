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
		self.completed = True


@dataclass
class Pet:
	name: str
	species: str
	breed: str = ""
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		self.tasks.append(task)


@dataclass
class Owner:
	name: str
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		self.pets.append(pet)

	def get_all_tasks(self) -> list[Task]:
		return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
	def get_all_tasks(self, owner: Owner) -> list[Task]:
		return owner.get_all_tasks()

	def organize_tasks(self, owner: Owner) -> list[Task]:
		return sorted(self.get_all_tasks(owner), key=lambda task: task.time)

	def mark_task_complete(self, task: Task) -> None:
		task.completed = True
