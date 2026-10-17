from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Owner:
	name: str
	preferences: str = ""
	pets: list[Pet] = field(default_factory=list)
	tasks: list[CareTask] = field(default_factory=list)

	def add_task(self, task: CareTask) -> None:
		raise NotImplementedError

	def update_preferences(self, preferences: str) -> None:
		raise NotImplementedError


@dataclass
class Pet:
	name: str
	species: str
	breed: str = ""
	care_tasks: list[CareTask] = field(default_factory=list)


@dataclass
class CareTask:
	title: str
	category: str
	duration_minutes: int
	priority: str
	recurrence: str = "daily"
	due_time: str | None = None
	is_complete: bool = False

	def mark_complete(self) -> None:
		raise NotImplementedError

	def update_details(self) -> None:
		raise NotImplementedError


@dataclass
class PlanningConstraints:
	available_minutes: int
	day_start: str
	day_end: str
	preferences: str = ""


@dataclass
class DailyPlan:
	plan_date: date
	total_available_minutes: int
	total_scheduled_minutes: int = 0
	overall_rationale: str = ""
	scheduled_items: list[PlanItem] = field(default_factory=list)
	skipped_tasks: list[CareTask] = field(default_factory=list)

	def get_scheduled_items(self) -> list[PlanItem]:
		raise NotImplementedError

	def get_skipped_tasks(self) -> list[CareTask]:
		raise NotImplementedError


@dataclass
class PlanItem:
	task: CareTask
	start_time: str
	end_time: str
	rationale: str


class Planner:
	def generate_plan(
		self,
		owner: Owner,
		pet: Pet,
		tasks: list[CareTask],
		constraints: PlanningConstraints,
	) -> DailyPlan:
		raise NotImplementedError

	def rank_tasks(
		self,
		tasks: list[CareTask],
		owner: Owner,
		constraints: PlanningConstraints,
	) -> list[CareTask]:
		raise NotImplementedError

	def explain_selection(
		self, task: CareTask, constraints: PlanningConstraints
	) -> str:
		raise NotImplementedError
