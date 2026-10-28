# Estimate from demonstrated progress

Estimate the user's path to the chosen milestone from their actual delivery history and abilities. AI-assisted coding speed alone is not a product-delivery rate. The work may be dominated by understanding the problem, designing behavior, making tradeoffs, communicating intent, evaluating outputs, and iterating until the result works as intended. Establish which activities actually dominate this project rather than substituting a universal claim about either AI capability or technical difficulty.

## Reconstruct the last few months

Use a recent representative period, usually the last two or three months when available, or the project's actual lifetime if shorter. Establish what worked at the beginning and what works now. Inspect relevant release notes, dated demos, issues, pull requests, tests, or repository history when accessible; supplement with the user's account. Ask for missing facts without requiring a perfect time log. Label observed evidence, user recollection, and assumptions separately.

Track meaningful delivered outcomes: what can a real user now complete that they could not complete before? Distinguish working end-to-end behavior from scaffolding, a generated screen, a mock, or a partially connected feature. Use the intended acceptance criteria, not visual polish alone. Keep unfinished work and reverted or redesigned work visible: it consumed effort and may have produced learning, but it is not additional completed functionality. Do not use commits, lines of code, model tokens, or an unweighted feature count as a proxy for finished product progress.

A compact history can record the outcome, starting and accepted state, dates, available effort information, design or review cycles, blockers, and supporting artifact. Do not infer active hours from commit timestamps. Separate hands-on effort from calendar time, external waits, interruptions, and periods spent on other projects. When hours are unknown, preserve that uncertainty rather than inventing them.

Ask where time went: deciding what should happen, modeling workflows and edge cases, designing the system or interface, implementing, integrating, reviewing, testing against intent, or revising after feedback. Identify changes in scope and repeated changes of direction. These can explain slower visible delivery without indicating weak coding ability or laziness.

## Assess proficiency for the work that remains

Assess relevant tasks individually. Use specific examples of work the user has completed, how independently they completed it, the help or tools used, and whether the outcome was successful. Useful descriptions include practiced independently, some experience with support, first attempt, or unknown; avoid invented numerical skill scores.

Include product discovery, system design, implementation, quality assurance, deployment, positioning, content, distribution, sales, onboarding, and support only as the project requires. Engineering experience is not evidence of marketing proficiency, and a job title is not proof that someone lacks it. Ask about actual experience. A polished AI-generated campaign draft is not evidence that the user can acquire customers through that channel.

For unfamiliar work, include learning, setup, practice, feedback, and likely revision as explicit work packages or clearly identified parts of a package. Estimate them from relevant experience when possible. Otherwise use a provisional range and a small representative exercise to learn more. Do not apply a generic “beginner takes three times longer” factor. Distinguish producing a first artifact from performing the activity effectively and repeatedly. Avoid assuming that engineering delivery speed transfers to customer interviews, marketing, sales, or support.

Account for how the user's actual AI tools help each activity and what human judgment remains. A changed model or workflow may improve throughput, but the improvement must be observed or labeled as a scenario. Do not automatically extrapolate a benchmark, a code-generation demo, or the user's initial burst of enthusiasm into faster end-to-end delivery. For outside help, include briefing, coordination, and review by the user as well as the helper's work.

## Build the forecast from comparable work

Group remaining work by comparable outcome and workflow, not by treating all features as equal. Match it to recent examples with similar clarity of intent, integration needs, acceptance criteria, and user proficiency. Use the observed range where meaningful, state the small sample or other limits, and explain adjustments for reuse, better-defined requirements, unfamiliar work, dependencies, or new responsibilities. Historical progress is a baseline, not a permanent ceiling or a promise that every remaining task will behave similarly.

Use a consistent estimation basis:

- If credible active effort data exists, estimate remaining human effort from analogous completed work plus explicitly identified new work, then schedule it against the user's capacity. Include design, review, and revision already present in those examples without adding them a second time.
- If only elapsed delivery history is known, estimate a calendar range for comparable outcomes under similar availability. This baseline already contains the ordinary interruptions and iteration in that period. Do not divide it by weekly hours again or add the same delays twice.
- If availability, tools, proficiency, or scope have materially changed, explain why the baseline may no longer transfer. Show conditional scenarios or calibrate again; do not assume doubling hours halves the schedule. Independent activities still compete for one person's attention.
- For unfamiliar task types without usable analogues, keep a separate uncertainty range. Do not use technical throughput to estimate marketing effectiveness or customer response time. Acquisition and revenue also depend on demand and channel evidence, not only the user's competence.

Identify the dominant constraint and its consequence. If repeated design changes are slowing delivery, define a smaller workflow and acceptance criteria before forecasting a broad feature list. If the issue is unfamiliar distribution work, give learning and testing that channel real capacity in the plan. If technical integration or reliability is demonstrably the bottleneck, retain it explicitly. Avoid assigning uncertainty to every task simply because one part is unresolved.

When there is too little evidence, leave the larger forecast unresolved. A bounded calibration step can help, but first compare its value with the other projects and check the shared monthly budget in [portfolio-planning.md](portfolio-planning.md). Propose it only for an allocated priority; otherwise recommend deferring it. Specify what effort, iterations, and outcome to record and what would update the forecast. Do not start implementation, publish a campaign, or contact customers solely to improve an assessment without authorization.

Schedule estimated effort into this month's remaining allocation and next month's independent allocation, after their respective outside-work commitments. A month with little or no usable time must visibly slow or suspend the plan. Do not give a project the entire portfolio's monthly cap or extrapolate a fixed weekly pace through known busy periods. Time to conduct a demand test does not establish when a buyer will pay.

## Report and revise

Show the history window, accepted outcomes, estimate basis, relevant proficiency, named uncertainties, and what changed from the historical conditions. Prefer ranges with reasons to a single deadline or unsupported confidence percentage. A thin record may support only a near-term milestone estimate, not a defensible full-product completion date.

At the next checkpoint, compare the accepted outcome and actual effort or elapsed time with the assumptions. Revise the remaining forecast based on what was learned, including changes to intent, scope, capacity, and proficiency. This checkpoint is part of the plan; it does not authorize a recurring monitor.
