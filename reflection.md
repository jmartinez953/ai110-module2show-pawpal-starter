# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design includes four classes: Owner, Pet, Task, and Scheduler. Owner stores the owner's name, available time, preferences, and pets. Pet stores its name, species, and care tasks, and checks whether feeding or walking has been completed today. Task stores a care activity's name, category, duration, priority, and completion date and time. Scheduler uses the owner's information and pet tasks to create a daily plan and explain its choices. An Owner has Pets, and each Pet has Tasks. Scheduler works with these objects without inheriting from them.
### Core user actions

1. The owner can add and manage care tasks for their pet, including walks, feeding, grooming, and medication.
2. The owner can specify their available time, task priorities, and preferences to guide scheduling.
3. The owner can view a daily care plan and understand why the app selected and ordered those tasks. 

These were my initial design goals. The constraints and improvements sections below explain which features are implemented and which remain planned.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
During the AI review, I changed Scheduler's daily_plan from a list of Tasks to a list of (Pet, Task) pairs. A list of Tasks alone did not directly identify which pet each scheduled task belonged to. Keeping the pet and task together makes the plan clearer when multiple pets have similar care tasks, such as morning feeding.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler uses scheduled start dates and times, task durations, and completion status. It sorts unfinished tasks chronologically and uses their durations to detect overlaps across pets. It also supports filtering by pet name and completion status. I focused first on making task timing clear and identifying conflicts so the owner can see when care activities overlap. Priority, available minutes, and owner preferences are stored, but they do not yet control task selection or ordering.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
I kept an explicit loop for filtering tasks instead of using a more compact list comprehension. I combined nested if statements and prepared the requested pet name once before the loop. This makes the method easier for me to read while avoiding repeated name formatting. The tradeoff is that the code takes more lines than a list comprehension, but I find it easier to explain and debug. Running the CLI demo confirmed that filtering by pet and completion status still produced the expected results.
Some of these algorithms were already ai created so i decided to change the one that were harder to understand and i made sure the updated version were easier to explain

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?



I used AI chat to brainstorm the four classes, create a Mermaid diagram, and build the implementation one method at a time. Code explanations and reviews were especially useful because I wanted to type the code myself and understand it. I asked questions about parameters, loops, and filtering, then used CLI output and browser checks to verify the behavior. A separate planning chat helped keep algorithm suggestions separate from the implementation work. Asking for small steps, comments, and simpler alternatives helped me evaluate suggestions instead of accepting code without understanding it.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?



I modified the initial recurrence plan because keeping only the latest completion time would not support my requirement to report on past days. I wanted completed occurrences to remain available, so we kept each completed Task and created a separate unfinished Task for its next occurrence. This preserved the existing four-class design. I checked the CLI output to confirm that daily tasks advanced one day and weekly tasks advanced seven days, while the original occurrences remained completed. These records currently exist in memory; they are not saved permanently between sessions.


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I ran two automated pytest tests: one checked that completing a task changed its status and recorded a completion time, and the other checked that adding a task increased a pet's task count and stored the correct task. Both passed. I also used the CLI demo to check chronological sorting, filtering by pet and completion status, daily and weekly recurrence, and overlapping-task warnings. In the browser, I checked that pets and tasks stayed in session memory across reruns, that filters changed the displayed results, and that the schedule showed tasks in time order with conflict warnings. These checks helped me verify both the backend methods and their connections to the interface. 


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?


I am confident in the behaviors I checked, but the two automated tests do not cover all scheduling features. The CLI and browser demonstrations showed that the tested examples worked. Next, I would add automated tests for unscheduled tasks, empty filter results, tasks that end exactly when another begins, overlaps across midnight, and recurrence across month or year boundaries. I would also verify that completing the same recurring task twice does not create duplicate occurrences.


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?


I am most satisfied with building the project in small steps and understanding the code as I typed it. Starting with the CLI helped me check the backend before connecting it to Streamlit. Seeing the browser sort tasks and identify an overlap showed that the interface was using the Scheduler correctly. Asking for explanations and adding comments also made the code easier for me to follow and explain to someone else.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?


I would add browser controls for completing tasks, choosing recurrence, and changing scheduled times so owners can resolve conflicts directly. I would also save pet and task data permanently and add reports covering a selected date range. Another improvement would be making available time, priorities, and owner preferences influence the schedule instead of only storing that information. Before expanding these features, I would add automated tests for the scheduling algorithms.


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?



I learned that being the lead architect means deciding what the system should do, understanding the design, and checking whether the implementation meets those requirements. AI helped suggest code and explain options, but I still needed to question assumptions, choose readable solutions, and verify results. Asking for smaller steps and explanations helped me participate in the coding instead of simply copying it. Working with AI is most useful when I can explain why a change belongs in the system and show evidence that it works.