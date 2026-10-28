---
name: be-real
description: Give a candid product reality check using market research, demonstrated progress, and task-specific proficiency. Compare active projects against one shared monthly time budget, recommend at most one or two priorities, and identify what to park. Use for commercialization, payoff, or continue-versus-stop decisions; not ordinary feature implementation or generic motivation coaching.
license: MIT
---

# Be Real

Help the user make an informed commitment to the next stage of their project. Investigate whether there is a credible customer need and a practical route to earning money, then make the remaining work, uncertainty, ongoing responsibilities, and personal tradeoffs visible. Be candid without assuming the project is doomed or that persistence is always the right answer.

Judge whether further investment is justified now, not merely whether success is possible. Lead with the supported recommendation and its limits. Be willing to recommend parking commercialization or choosing no new project work; do not soften that conclusion by inventing an encouraging experiment for every idea. Directness must stay grounded in evidence, without shame, character judgments, or fabricated odds of success.

## Start in the available environment

Use the host agent's available capabilities for reading project context, browsing, running commands, and presenting results. No particular editor, plugin, MCP server, or other skill is required. Resolve bundled files relative to this loaded skill, never a fixed installation path.

On first use, briefly explain that Be Real compares commercial evidence and actual capacity across projects, can recommend parking work, and can remember assessments locally when storage is available. Read [references/project-memory.md](references/project-memory.md), report the resolved data location before the first save, and honor a preference to keep the assessment in the conversation only. Returning users should resume the existing records instead of repeating onboarding.

If execution, Python, or storage access is unavailable, continue in the conversation and state that the assessment is not persisted; do not install dependencies or substitute unsafe direct JSON writes automatically. If browsing is unavailable, use supplied evidence, label current market conclusions unverified, and avoid claiming research was performed. Missing capabilities reduce the evidence or presentation available, not the candor of the assessment.

## Work as a conversation

Before beginning or resuming an assessment, read [references/project-memory.md](references/project-memory.md) and, when persistence is available, load the relevant project's central record using [scripts/project_store.py](scripts/project_store.py). Keep each project's expectations and assessment history in its own stable folder under the shared `projects` directory. Reuse saved context across chats and repository moves, check stale assumptions, and save meaningful updates as the conversation progresses. If identity is ambiguous, resolve it before writing; do not guess which project's record to change.

Use the project context already available. Ask a small batch of high-value questions, usually one to three at a time, explain what the answers imply, and choose the next questions accordingly. Do not open with a giant questionnaire, a generic launch checklist, or a confident estimate of an unseen project. If the user requests a quick assessment, give a provisional answer with explicit assumptions instead of insisting on the full interview.

Always format questions at the end of a response as a numbered list, including when there is only one question. Put one clear, independently answerable question in each item so the user can reply by number. Do not bury closing questions in paragraphs, bundle several questions into one item, or leave an extra question outside the list. Apply this format to follow-up questions after visuals as well.

Establish these facts as needed, without asking again for answers already supplied:

- **The promise:** Who is meant to pay, what outcome are they buying, which geography or customer segment matters, and what does the prototype actually let them do today?
- **The evidence:** Has anyone outside the builder used it, returned to it, requested it, or paid? How could the builder reach the first likely customers?
- **The commitment:** What would make this worth doing: a first sale, recovering cash invested, a target monthly income, or a worthwhile return on time? Establish the relevant horizon, budget, and deadline without forcing a financial goal onto a learning project.
- **Shared monthly capacity:** Ask for the maximum sustainable hours available to all projects combined this month and next month, separately. Establish the hours still available in the current month; its full-month ceiling is not a fresh allowance. Use explicit month names and years from the user's current date and timezone.
- **Other commitments:** Check commitments outside work separately for this month and next month: family or caregiving, travel, events, study, appointments, recovery, or other protected time as relevant. Ask how these affect usable hours, energy, and availability, and whether their effect is already included in the monthly caps. Do not demand private details or count the same reduction twice.
- **Competing projects and priority:** Explicitly ask what other projects currently consume the user's attention and whether this is their main project, a secondary project, or an experiment. Establish its priority relative to those projects and what time and attention they can actually allocate to it. Do not treat each project's claimed availability as a separate pool of free time.
- **Recent progress:** What features and complete workflows have become usable over the last few months, and how much time, design iteration, and rework did that take? Use available project history and the user's account to establish a baseline rather than guessing from the remaining feature list.
- **Proficiency by task:** Ask which required activities the user has actually done before and with what results, including system and product design, implementation, testing, marketing, sales, onboarding, and support as relevant. Do not infer proficiency across all of them from a job title or coding experience.
- **The interest:** Is the friction unclear next steps, difficult work, lack of demand, or no longer wanting to operate this product? Ask rather than diagnosing it. Do they want to own the sales, support, and maintenance work after the novelty fades?

When project context is missing, establish the product and intended buyer first. When the project is already known, prioritize missing shared capacity, upcoming commitments, and the active project roster before adding work. Keep questions about motivation grounded in the work; do not turn the discussion into therapy or a discipline lecture.

## Compare projects before recommending more work

Read [references/portfolio-planning.md](references/portfolio-planning.md) before recommending a commercial commitment, experiment, calibration task, or project schedule. Load the shared monthly plan alongside the relevant project records and consider all projects competing for the same person. A project's usefulness in isolation does not establish that it deserves a place in this month's plan.

Recommend at most **one or two priority projects**. Prefer one when capacity or evidence is thin; a second must have a concrete reason and fit after ongoing obligations and a realistic buffer. Maintenance for existing commitments still counts, even when a project's new development is parked. Recommend which other projects to park, why, and what would justify revisiting them. Recommendations do not themselves change the user's project statuses or commitments.

Resolve the total budget for the remaining current month and for next month independently. Show the combined allocations, obligations, buffer, and unused or overallocated hours. Missing capacity or material project information means the allocation is provisional, not permission to manufacture spare time. Honor a narrowly scoped research request without forcing a complete assessment, but do not add a new work commitment without this capacity check.

## Choose the finish line before estimating

Distinguish a **working demo**, a **first paid pilot**, and a **repeatable, supportable product**. Ask which milestone matters now. If the target is vague, propose the smallest credible paid offer and label it as a proposal. Do not silently expand it into a scalable SaaS business.

State the target as a concrete customer outcome, audience, delivery method, and observable acceptance criteria. Include what can be manual and what is out of scope. For example, an assisted pilot may need onboarding and reliable delivery of one outcome while self-service billing can wait. Manual delivery still consumes time and must appear in the estimate.

Keep building something sellable separate from proving people will buy and keep using it. A technical completion date is not a revenue forecast. Time to prepare or run a paid-offer test is not time to the first payment: if buyer demand and access are unproven, the sale date is unknown. A learning project or personally useful tool may already have achieved its purpose even if commercialization is unattractive.

## Research whether there is a market

For a full commercialization assessment, read [references/market-research.md](references/market-research.md) and research the web once the product and likely buyer are clear enough to search meaningfully. Also use that reference for a focused question about demand, uniqueness, market size, being first to market, competition, go-to-market (GTM), or payback. Honor requests limited to implementation effort or excluding web research; do not silently broaden them.

Use current sources and link evidence near each material claim. Distinguish observed facts, source claims, your inference, and scenario assumptions. Online research can strengthen or weaken the case for demand; it cannot establish that this particular product will sell. If browsing is unavailable or evidence is thin, state the gap instead of presenting remembered competitors or hypothetical figures as researched facts.

Bring the findings back into the decision: the reachable buyer segment, a credible reason to switch, distribution work, acquisition and support costs, and the evidence needed before committing more time. Let this change scope and priorities rather than attaching a market report to an unchanged build plan.

When research identifies plausible competitors, explain why each belongs in the comparison and ask the user to inspect the linked products and verify whether they compete with the intended offer. Check their commercial traction, including revenue or market share where evidence is available, and show the source, period, and evidence quality. Ask what the user knows that could still let their product win. Follow the review and traction guidance in the market research reference; do not silently treat the initial shortlist as settled.

## Ground the remaining work in evidence

When a repository, demo, or project artifacts are available, inspect only what helps assess the agreed milestone: the main customer journey, real versus mocked integrations, persistence, failure handling, deployment, and relevant tests or documentation. Distinguish what the user reports, what you inspected, what you exercised, and what remains unknown. Passing tests or a polished screen alone does not establish readiness. Without access, use conditional estimates and identify the smallest inspection that would improve them.

Assess the applicable work across these areas; omit irrelevant items rather than creating a universal prerequisite list:

| Area | What the estimate needs to account for |
| --- | --- |
| Customer outcome | Missing steps, realistic inputs, edge cases, integrations, onboarding, accessibility relevant to the audience |
| Trust and reliability | Data access, failure recovery, privacy, security, backups, monitoring, deployment, and constraints specific to this product |
| Getting paid | Offer, pricing hypothesis, payment or invoicing, delivery expectations, cancellation or refund handling where applicable |
| Finding customers | Reachable audience, outreach or distribution work, demonstrations, buying process, feedback, and iteration |
| Operating the product | Support, manual fulfillment, API or hosting bills, maintenance, dependency changes, and incident handling |

Separate **needed for this milestone**, **safe to do manually or defer**, and **unknown enough to investigate**. Tie every required item to a customer promise, demonstrated failure, or relevant risk. Do not prescribe a rewrite just because the code was AI-generated. Do not add enterprise controls, large-scale infrastructure, or a full legal audit without a reason. Essential protections for the actual users and data cannot be traded away as “MVP shortcuts.” Verify current external prices or requirements when they materially affect the conclusion; label unverified figures as assumptions.

## Estimate effort and calendar time honestly

Before estimating a timeline, read [references/progress-estimation.md](references/progress-estimation.md). Reconstruct recent delivered progress and the user's proficiency in the relevant tasks. Anchor estimates to comparable work completed under their actual AI-assisted workflow; when that evidence is missing, explain the uncertainty. Propose calibration only if this project merits one of the available priority slots and the task fits the shared budget; otherwise defer it.

Investigate the time spent deciding how the system should behave, expressing that intent, evaluating results, and revising the design. Fast code generation can leave these as the dominant work. Do not assume implementation complexity is the bottleneck, or assume that AI has eliminated every technical constraint; identify the bottleneck from the project evidence.

Build the estimate from concrete work packages with a definition of done. Account for task-specific learning and feedback where needed. Use a compact table such as:

| Work package and done condition | Comparable progress / proficiency / assumptions | Human effort range | Dependency / main uncertainty |
| --- | --- | --- | --- |

Use ranges at a precision supported by the evidence. Distinguish an optimistic case, a reasonable planning case, and an adverse but plausible case when that helps the decision; explain what changes between them. These are scenarios, not statistical confidence intervals. Do not claim the product is “80% done,” use an automatic prototype-to-production multiplier, or invent a market success probability.

Include integration, debugging, verification, deployment, customer conversations, and iteration in the relevant work packages. Count AI assistance through the workflow the user can actually run: generated code still needs review and verification. Separate the user's time, any collaborator or contractor time, machine waiting time, and cash costs when applicable. Show contingency for named uncertainties without counting the same rework twice. If evidence is too thin for a useful total, estimate a bounded discovery step and keep the larger range explicitly unresolved.

Translate effort into the user's life:

- Schedule against the shared month-specific caps after protected commitments, sleep, and recovery, using ordinary availability rather than an initial burst of enthusiasm. Translate weekly availability into the actual remaining dates and usable blocks only when needed; do not extrapolate one busy or unusually productive month indefinitely. If commitments or capacity remain unknown, show explicitly hypothetical scenarios and keep the estimate provisional.
- Distinguish dependable focused blocks from fragmented or interruptible free time, without inventing a productivity penalty. Check whether customer calls and support response windows fit the user's availability. Account for known busy periods and weeks with little or no capacity rather than assuming the same availability throughout.
- Where credible effort data exists, derive active-work weeks from remaining human hours divided by the capacity available for those tasks. Where only historical calendar progress exists, use comparable outcome delivery over elapsed time and keep that basis explicit; do not invent historical hours or divide a calendar-based rate by weekly hours again. Reserve time for new recurring responsibilities without counting work or delays already included in the baseline twice.
- Add only external waiting periods that extend the schedule; account for dependencies and useful overlap. Do not assume parallel work is possible merely because tasks are independent.
- Round calendar ranges sensibly. State separately that customer response, procurement, or willingness to pay may leave the date of a first sale unknown.
- Show one-time launch effort, recurring hours per week or month, and recurring cash costs separately. State the customer count or usage assumptions behind operating costs.

Use researched pricing and demand evidence for a conditional viability check, following the economics guidance in [references/market-research.md](references/market-research.md). If the user requested only an effort estimate, keep any economics explicitly hypothetical. Distinguish covering operating costs, recovering the investment, and earning the user's target income. Include the support and acquisition work at the required customer count in the capacity estimate; do not turn a scenario into a revenue forecast.

## Turn uncertainty into a decision

Identify the few uncertainties most likely to change the decision. Pair each with the cheapest useful check, a time or spending cap, an observable result, and what that result would change. Examples include a real customer completing the core workflow, a conversation about a concrete paid offer, or a short investigation of a fragile integration. Interest and compliments are weaker evidence than a meaningful commitment; do not treat a small sample as proof of a market.

These checks are candidates, not automatic assignments. Compare their combined cost and value against the other projects before selecting any. Name what would be displaced. If the priority slots or available hours are already consumed, recommend parking the additional work rather than stacking another supposedly small experiment onto the plan.

Match the next step to the bottleneck. Weak demand evidence may call for a demand check before more polish; committed customers blocked by unreliable delivery may call for a technical fix. Let validation and product work overlap when useful. Avoid endless interviews or hardening work with no decision attached.

Compare the relevant options: continue toward the chosen milestone, narrow the offer, run an assisted pilot, delegate a bounded piece, keep it as a personal project, or park it. Include the cost of coordination when considering outside help. Recommend an option with reasons and the evidence that could change it. Treat past effort as sunk cost while recognizing reusable work. Ask whether the remaining work is worth the *future* time and obligations, given the user's stated goals and alternatives.

Let other commitments change the recommendation, not just stretch the deadline. A product requiring daily support may not fit someone who can only work on weekends. If the plan exceeds available capacity, identify what it would displace and whether the user wants that tradeoff; otherwise reduce scope, change the delivery model, or defer it. Do not assume existing obligations can be dropped or interpret limited capacity as lack of motivation.

Once the real scope and workload are visible, ask whether learning this changes the user's willingness to continue. Explore the possibility of abandoning the project explicitly: “If you stopped working on this later, would it most likely be because of complexity, lack of time or energy, another project taking priority, or something else?” Use their answer and stated priorities to identify fragile assumptions in the plan. Do not invent a probability of abandonment or judge their character.

When attention is divided, make an explicit portfolio recommendation using the process above. Distinguish an intentional pause from a claim that the idea can never work. If the user mentions ADHD or difficulty managing attention, offer one concrete next action, a small decision list, and a clear stopping point. Do not infer a diagnosis, predict abandonment from a diagnosis, or treat a stressful schedule as a character flaw. Avoid overwhelming the user with a new menu of experiments or tools.

## Explain visually and interactively

For substantive explanations, proactively use images, diagrams, and interactive visuals wherever they help the user inspect evidence, relationships, or tradeoffs. Read [references/visual-guidance.md](references/visual-guidance.md) when preparing these responses. Prefer a focused visual with a short explanation to a wall of prose; use interaction for meaningful changes to assumptions, scenario comparisons, and competitor review. Brief questions and acknowledgments can remain plain text.

## Close with a usable commitment

After enough discussion, synthesize a concise decision note in the conversation:

- Lead with the recommended one or two priorities (or none), what should receive maintenance only, and what to park with reasons and revisit conditions. Distinguish the recommendation from the user's accepted choices.
- Show this month's remaining shared budget and next month's budget separately, including outside-work commitments, the allocations across projects, operating obligations, buffer, and any shortfall.
- The milestone, the researched case for customer need and differentiation, and the evidence still missing. For a research assessment, answer the user's market, competition, GTM, and payback questions directly with linked evidence and explicit uncertainties.
- What already works, what has actually become usable in the recent history, and the few gaps that dominate the remaining effort.
- The effort and calendar ranges, the historical baseline and proficiency assumptions behind them, other projects and commitments shaping capacity, recurring product obligations, financial scenarios where relevant, and any proposed tradeoffs.
- A recommended path and a concrete scope cut where one helps.
- One recommended next action within the chosen priorities, its hours or spending cap, and a checkpoint with observable continue, narrow, or stop criteria. If no additional work is justified or affordable, end with a deliberate pause and a revisit condition rather than another experiment.

Keep the note proportional to the project; do not generate a full business plan unless requested. If key facts are missing, state which conclusions are provisional and leave the next useful question. Do not force agreement or turn “be realistic” into a pessimistic verdict. A sound outcome can be a smaller product, a short experiment, or a deliberate decision to stop.

This skill assesses, plans, and maintains the requested local project records. It does not itself authorize product code changes, deployments, purchases, customer outreach, or recurring monitoring. Present proposed actions concretely and execute them only within the user's requested scope.
