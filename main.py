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

	owner.add_pet(mochi)
	owner.add_pet(biscuit)

	print("Today's Schedule")
	for task in Scheduler().organize_tasks(owner):
		print(f"{task.time.strftime('%H:%M')} - {task.description}")


if __name__ == "__main__":
	main()
