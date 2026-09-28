# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design includes four classes: Owner, Pet, Task, and Scheduler. Owner stores the owner's name, available time, preferences, and pets. Pet stores its name, species, and care tasks, and checks whether feeding or walking has been completed today. Task stores a care activity's name, category, duration, priority, and completion date and time. Scheduler uses the owner's information and pet tasks to create a daily plan and explain its choices. An Owner has Pets, and each Pet has Tasks. Scheduler works with these objects without inheriting from them.
### Core user actions

1. feeding, grooming, and medication.
2. The owner can specify their available time, task priorities, and preferences to guide scheduling.
3. The owner can view a daily care plan and understand why the app selected and ordered those tasks.The owner can add and manage care tasks for their pet, including walks, 
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
During the AI review, I changed Scheduler's daily_plan from a list of Tasks to a list of (Pet, Task) pairs. A list of Tasks alone did not directly identify which pet each scheduled task belonged to. Keeping the pet and task together makes the plan clearer when multiple pets have similar care tasks, such as morning feeding.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
