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
		"""Return tasks matching the optional completion and pet-name filters.

		Pet names are matched case-insensitively. If both filters are provided,
		a task must match both conditions.
		"""
		filtered_tasks = []
		target_pet_name = pet_name.casefold() if pet_name is not None else None

		for pet in owner.pets:
			if target_pet_name is not None and pet.name.casefold() != target_pet_name:
				continue
			for task in pet.tasks:
				if completed is not None and task.completed is not completed:
					continue
				filtered_tasks.append(task)

		return filtered_tasks

	def sort_by_time(self, tasks: list[Task]) -> list[Task]:
		"""Return a new list ordered by scheduled clock time.

		The input list is not modified; tasks with equal times retain their order.
		"""
		return sorted(tasks, key=lambda task: task.time)

	def organize_tasks(self, owner: Owner) -> list[Task]:
		"""Return all pet tasks ordered by scheduled time."""
		return self.sort_by_time(self.get_all_tasks(owner))

	def detect_conflicts(self, owner: Owner) -> list[str]:
		"""Return one warning per due-date/time slot containing multiple tasks.

		Tasks are grouped by due date and clock time. Repeated references to the
		same task object are counted only once.
		"""
		conflicts: dict[tuple[date, time_type], list[tuple[Pet, Task]]] = {}
		seen_tasks: set[int] = set()

		for pet in owner.pets:
			for task in pet.tasks:
				task_id = id(task)
				if task_id in seen_tasks:
					continue
				seen_tasks.add(task_id)
				key = (task.due_date, task.time)
				conflicts.setdefault(key, []).append((pet, task))

		warnings = []
		for (due_date, task_time), entries in conflicts.items():
			if len(entries) < 2:
				continue

			task_names = ", ".join(
				f"{task.description} ({pet.name})" for pet, task in entries
			)
			pet_task_counts: dict[int, int] = {}
			for pet, _ in entries:
				pet_id = id(pet)
				pet_task_counts[pet_id] = pet_task_counts.get(pet_id, 0) + 1

			has_same_pet_conflict = any(count > 1 for count in pet_task_counts.values())
			has_different_pet_conflict = len(pet_task_counts) > 1
			conflict_types = []
			if has_same_pet_conflict:
				conflict_types.append("for the same pet")
			if has_different_pet_conflict:
				conflict_types.append("for different pets")

			warnings.append(
				f"Warning: {task_names} are scheduled for "
				f"{task_time.strftime('%H:%M')} on {due_date} "
				f"{' and '.join(conflict_types)}."
			)

		return warnings

	def mark_task_complete(self, owner: Owner, task: Task) -> Task | None:
		"""Complete a task and append its next daily or weekly occurrence.

		Returns the new task, or ``None`` for a one-time or already-completed task.
		Raises ``ValueError`` if the task does not belong to one of the owner's pets.
		The next due date is calculated from today.
		"""
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
