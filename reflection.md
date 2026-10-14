# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

1. The user can enter basic information about themselves and their pet so the app can tailor care planning to them.
2. The user can add or edit pet care tasks, including each task's duration and priority.
3. The user can generate and review a daily care plan that accounts for available time, priorities, and preferences, with an explanation of the choices.

**a. Initial design**

The current design uses four classes:

- **Task** stores a care activity's description, scheduled time, frequency, duration, priority, and completion status. Its methods mark it complete or pending.
- **Pet** stores a pet's name, species, and tasks. Its methods add, remove, and list tasks.
- **Owner** stores an owner's name and pets. Its methods add or remove pets and retrieve all their tasks.
- **Scheduler** works with an owner to retrieve tasks across pets, filter by completion or pet, organize tasks by time and priority, and update completion status.

An owner can have multiple pets, each pet can have multiple tasks, and the scheduler retrieves task data through its owner.

**b. Design changes**

The original draft used `CareTask` and `DailyPlan`. During implementation, I replaced those with the requested `Task` and `Scheduler` classes so task ownership and management across pets are explicit. The scheduler gets tasks from the owner's pets and sorts them by scheduled time, with priority as a tie-breaker. I updated the UML to match the implemented classes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The conflict detector sorts the day's pending tasks by start time, then compares each task with later tasks until their start time is beyond the first task's end. This makes the overlap check clear and reports all conflicts, but can take quadratic time when many tasks overlap. That tradeoff is reasonable for a pet owner's small daily task list, where readable, complete warnings matter more than optimizing for very large schedules. The scheduler warns about conflicts instead of moving tasks automatically, preserving the owner's chosen times and letting them decide what to change.

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
