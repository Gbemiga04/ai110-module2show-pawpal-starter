# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

1. The user can enter basic information about themselves and their pet so the app can tailor care planning to them.
2. The user can add or edit pet care tasks, including each task's duration and priority.
3. The user can generate and review a daily care plan that accounts for available time, priorities, and preferences, with an explanation of the choices.

**a. Initial design**

The final design uses four classes:

- **Task** stores a care activity's description, scheduled time, frequency, duration, priority, due date, and completion status. Its methods mark it complete or pending.
- **Pet** stores a pet's name, species, and tasks. Its methods add, remove, and list tasks.
- **Owner** stores an owner's name and pets. Its methods add or remove pets, retrieve all their tasks, and save/load owner data as JSON.
- **Scheduler** works with an owner to retrieve and filter tasks, order due work by priority and time, find an open time slot, detect conflicts, and create recurring task instances after completion.

An owner can have multiple pets, each pet can have multiple tasks, and the scheduler retrieves task data through its owner.

**b. Design changes**

The original draft used `CareTask` and `DailyPlan`. During implementation, I replaced those with the requested `Task` and `Scheduler` classes so task ownership and management across pets are explicit. I later added task due dates, recurring instances, JSON persistence, a next-available-slot search, and priority-first scheduling, updating the UML and UI to match.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler currently considers each task's due date, scheduled start time, duration, priority, and completion status. It puts due, pending tasks into an ordered schedule, using priority to break ties at the same start time, and checks task intervals for overlaps. I prioritized showing tasks at the right time and warning about conflicts because those behaviors make a daily care list immediately useful. The current version does not yet enforce an owner's total available-time limit or use owner preferences to select tasks; those remain possible improvements rather than implemented constraints.

**b. Tradeoffs**

The conflict detector sorts the day's pending tasks by start time, then compares each task with later tasks until their start time is beyond the first task's end. This makes the overlap check clear and reports all conflicts, but can take quadratic time when many tasks overlap. That tradeoff is reasonable for a pet owner's small daily task list, where readable, complete warnings matter more than optimizing for very large schedules. The scheduler warns about conflicts instead of moving tasks automatically, preserving the owner's chosen times and letting them decide what to change.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI coding assistant to brainstorm the initial classes, translate the design into Python dataclasses, wire the backend into Streamlit, add scheduling algorithms and persistence, and draft focused tests. Asking for concrete behavior—such as how `timedelta` should create a task due tomorrow, or what edge cases mattered for sorting and recurrence—was more useful than asking for broad code generation. Separate chat sessions for algorithm planning and test planning helped me keep each discussion focused and return to the implementation with a smaller, clearer checklist.

**b. Judgment and verification**

An early AI-assisted design keyed scheduled times by task title. I changed it so each task stays paired with its time, because two tasks can share a title and otherwise be associated with the wrong time. I also kept conflict detection as a warning rather than letting the scheduler automatically move or discard tasks, which leaves the owner's chosen schedule intact for a human to resolve. I refined the warning to name both pets, tasks, and overlapping times, then used a Streamlit AppTest with two simultaneous tasks to verify that the UI showed the warning and schedule. I also reviewed generated test cases and ran them with `python -m pytest` rather than treating generated code as correct without evidence.

---

## 4. Testing and Verification

**a. What you tested**

I tested adding tasks and collecting them across pets, chronological and priority ordering, completion and pet-name filtering, daily and weekly recurrence, and conflict detection within one pet and across pets. I also tested duplicate start times, completed and future tasks, invalid ownership, and invalid task values. These cases check both ordinary use and situations where a misleading schedule or accidental duplicate would be especially confusing.

**b. Confidence**

I am reasonably confident in the core behaviors because all 24 automated tests pass, and I exercised the UI flow for adding a pet and task, generating a schedule, and showing a conflict warning. I would next test recurrence and conflict warnings through more complete UI scenarios, tasks that cross midnight, empty schedules, and overlapping groups of three or more tasks. I would also add tests for weekly recurrence through the UI and for how an available-time limit should affect the schedule once that feature exists.

---

## 5. Reflection

**a. What went well**

I am most satisfied that the same Scheduler logic is used by both the command-line demo and the Streamlit app. Sorting, filtering, recurrence, conflict warnings, next-slot suggestions, and persistence are demonstrated by runnable code and tests rather than being only design ideas.

**b. What you would improve**

In another iteration, I would add explicit owner preferences and a user-configurable planning window, then apply them when selecting and suggesting tasks. I would also let users edit and delete tasks in the UI, provide a more deliberate rule for weekly task days, and expand UI tests so changes to the interaction flow are caught automatically.

**c. Key takeaway**

I learned that being the lead architect means deciding what the system should do, keeping the model and UI aligned, and checking AI-generated ideas against the requirements and actual behavior. The AI helped me move quickly, but I was responsible for choosing the scope, reviewing tradeoffs, and requiring tests and an interactive check before trusting the result.
