from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
	owner = Owner("Jordan")
	mochi = Pet("Mochi", "cat")
	biscuit = Pet("Biscuit", "dog")

	mochi.tasks.extend(
		[
			Task("Breakfast", time(7, 30), "daily"),
			Task("Evening feeding", time(18, 0), "daily"),
		]
	)
	biscuit.tasks.append(Task("Morning walk", time(8, 0), "daily"))
	biscuit.tasks.append(Task("Nap", time(14, 0), "daily"))
	biscuit.tasks.append(Task("Snack", time(16, 0), "daily"))
	biscuit.tasks.append(Task("Play", time(16, 0), "daily"))

	owner.add_pet(mochi)
	owner.add_pet(biscuit)

	scheduler = Scheduler()
	print("Today's Schedule")
	print("Owner: ", owner.name)
	for task in Scheduler().organize_tasks(owner):
		print(f"{task.time.strftime('%H:%M')} - {task.description}")

	for warning in scheduler.detect_conflicts(owner):
		print(warning)

if __name__ == "__main__":
	main()
