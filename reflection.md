# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Three core actions:
1. Add a new pet to the inventory
2. Schedule a pet walk
3. Go through today's tasks

Pet class - attributes (name, type, breed, owner), methods (goForWalk, getGrooming)
Owner class - attributes (name, address, pets)

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Replaced the original seven classes with the requested four: Task, Pet, Owner, and Scheduler.
Added task details: description, time, frequency, and completion status.
Added a task list to Pet, and pet management plus get_all_tasks() to Owner.
Added scheduler methods for retrieving, organizing, and updating tasks.
Updated relationships to show that an owner manages multiple pets, pets track multiple tasks, and the scheduler retrieves tasks through the owner.
Removed the separate planning-constraints and daily-plan classes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The clearest improvement is in sort_by_time(): since Task.time is already a datetime.time, compare it directly instead of converting it to a string.


For detect_conflicts() in pawpal_system.py, the pairwise scan is easy to follow but takes O(n2) comparisons even when there are no conflicts. If schedules grow, group tasks by (due_date, time) first, then report only groups with multiple tasks. That’s O(n) to group and scan, as long as you produce one warning per conflicting time slot. If you want a separate warning for every conflicting pair, generating those warnings can still take O(n2).

filter_tasks() could also use explicit for loops and continue checks instead of a multi-clause list comprehension. That’s a readability choice, not a meaningful performance improvement for this app’s likely task counts.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to design the classes in UML diagram, add the classes in python and the unit tests. I rejected the other classes that AI suggested. I accepted the others.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I read through the AI suggestions, understood them, executed the unit tests, etc. In the initial design, it gave me a more complicated design with many classes and I did not accept it as such a complicated design was not needed for achieving the tasks in this project. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested all the methods added to the classes in the design. These tests are important to understand the working of the methods and they also act as regression tests to ensure that any future changes do not break any existing functionality. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

1. No tasks: An owner with no pets, and a pet with no tasks, should produce empty results for organizing, filtering, and conflict detection.
2. Equal sort times: Two distinct tasks at the same time should both remain in the sorted result, in their original relative order. Also check that sorting leaves the input list unchanged.
3. Conflict boundaries: Same date and time should conflict; same time on different dates should not. A single task should not conflict with itself, including if the same task object appears twice.
4. Recurring completion: Assert that a one-time task becomes completed without creating a successor. For daily and weekly tasks, verify the successor is the only new task, starts incomplete, and preserves the description and time.
5. Date edge cases: Test recurrence across a month or year boundary. The existing test covers a leap-day transition. Decide whether the next occurrence is based on today or the task’s due date; the implementation currently uses today.
Conflict policy for completed tasks: Decide whether completed tasks should still trigger warnings, then add a test for that behavior.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

Testing suite covers a great deal of scenarios

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Add more edge cases in the tests. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I must give clear instructions to the AI so that it understands my intention and its implementation matches my expectation. 