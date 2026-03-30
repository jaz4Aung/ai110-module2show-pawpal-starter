# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- I started from the UML in `UML.md`, which defined a stateless `Scheduler` service that reads an `Owner` and `Pet`, consumes a list of `Task` objects, and produces a `DailyPlan`.
- I implemented in the same order as the workflow: first I worked from the class stubs/structure (Owner/Pet/Task/PlanItem/DailyPlan/Scheduler), then I filled in `Scheduler` with the sort + pack logic, and finally I connected it to the Streamlit UI in `app.py`.
- I included:
  - `Owner`: represented scheduling constraints (`available_minutes`) and the tie-break preference (`preferred_task_order`).
  - `Pet`: represented planning context for display (`name`, `species`).
  - `Task`: represented individual care items (`title`, `duration_minutes`, `priority`).
  - `PlanItem`: represented one scheduled line (which `Task`, its `order`, its `start_minute`, and a human-readable `reason`).
  - `DailyPlan`: represented the final output (a list of scheduled `PlanItem`s, the `not_scheduled` tasks, total minutes scheduled, and a summary).
  - `Scheduler`: owned the actual scheduling logic and built the `DailyPlan`.

**b. Design changes**

- The core UML structure stayed the same (same class responsibilities), but I made two practical adjustments while implementing:
  1. I added a `preferred_task_order` input to the Streamlit UI (via a textarea) so the tie-breaking logic was actually usable and easy to demo.
  2. I made the `PlanItem.reason` more explicit about *why* a task landed where it did (priority, tie-break, remaining budget, and start minute). This helped the “explain the plan” requirement show up clearly in the UI.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers three main constraints:
  1. **Time budget** (`Owner.available_minutes`): tasks are only scheduled if their `duration_minutes` fits in the remaining time.
  2. **Priority** (`Task.priority`): tasks are sorted so higher priority tasks are considered first.
  3. **Owner preferences** (`Owner.preferred_task_order`): when tasks have the same priority, the scheduler breaks ties by the earliest title found in `preferred_task_order`.
- I prioritized these because they directly map to the explicit fields in the starter UI (duration + priority) and the `Owner` constraints provided by the UML starter (available time + preferred order). This made the behavior predictable and easy to explain.
- For determinism, tasks with unknown priority strings default to the lowest rank, and tasks not found in `preferred_task_order` effectively get pushed to the end of the tie-break ordering.

**b. Tradeoffs**

- The main tradeoff is that I used a **greedy, first-fit packing** strategy rather than an optimal optimization approach (like knapsack/dynamic programming).
- This is reasonable here because the project focuses on designing the system and producing an explainable plan: greedy packing is deterministic, easy to justify, and it still respects the key constraints (priority ordering and the time budget).

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI to help translate the UML into concrete implementations (especially the `Scheduler.schedule` method), and to think through how to connect the scheduling output to the Streamlit UI.
- The most helpful prompts were ones that asked for an end-to-end implementation using the existing data fields and return types (for example: “rank tasks, greedily pack into budget, and generate a human-readable reason per PlanItem”).

**b. Judgment and verification**

- I didn’t accept the idea of “sorting only” as enough; I made sure the implementation also produced the full `DailyPlan` output the UI needs (ordered `PlanItem`s with correct `order` and `start_minute`, plus `not_scheduled` and a summary).
- I evaluated the implementation by running a small Python sanity check that asserted which tasks should fit vs. not fit under a known time budget, and then confirmed that the generated `PlanItem.reason` and `total_scheduled_minutes` matched the expected logic.

---

## 4. Testing and Verification

**a. What you tested**

- I tested that:
  - tasks are sorted by priority (high → medium → low),
  - tasks with equal priority are ordered by `Owner.preferred_task_order`,
  - tasks are packed greedily until the time budget is exhausted,
  - and the remaining tasks appear in `not_scheduled`.
- These checks were important because the scheduler’s output directly drives what the UI displays, so incorrect ordering or budget accounting would immediately make the plan misleading.

**b. Confidence**

- I’m moderately confident for typical inputs: the implementation is deterministic and consistently matches the intended UML behavior.
- If I had more time, I would add more verification around edge cases like:
  - unknown priority strings,
  - tasks with zero/negative durations,
  - empty or missing `preferred_task_order`,
  - and duplicate task titles inside `preferred_task_order` (to clarify which one should win).

---

## 5. Reflection

**a. What went well**

- I’m most satisfied with the end-to-end “explainable plan” experience: the scheduler doesn’t just decide order, it also fills `PlanItem.reason` with a human-readable explanation grounded in the same rules used for sorting and packing.
- I also liked how the Streamlit integration became straightforward once the scheduler was cleanly separated as a stateless service (`Scheduler().schedule(...)`).

**b. What you would improve**

- If I iterated again, I would add a small automated test suite (using `pytest`) that covers key scheduling behaviors so changes to the scheduler don’t silently break the UI expectations.
- I would also consider a more optimal scheduling strategy if the scenario required maximizing a metric (for example maximizing total priority impact) rather than using a greedy plan.

**c. Key takeaway**

- The key takeaway is that “good design” means the details line up end-to-end: the scheduler must generate exactly the structured fields the rest of the app expects, and the explanation text must reflect the same logic that produced the plan.
