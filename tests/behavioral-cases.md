# Behavioral evaluation cases

These are manual scenarios for an agent with this skill loaded, not executable unit tests. Use fictional data and temporary storage; do not read or modify the evaluator's personal project records. Allow only the capabilities named in each case. Preserve the actual output with the agent/model version and date. Evaluate decisions and evidence rather than matching exact wording.

## Shared capacity and parking

Prompt: “Use Be Real. I have three projects: Booking has two paying users blocked by a bug; Writer has a demo but no repeat users; Charts is an idea. I want supplemental income. It is April 24, 2027. I have 10 project hours left in April and 18 in May after a family trip. I want a two-hour buffer each month. The next Booking fix previously took me about six hours for comparable work. There are no obligations on the other projects. I would like an experiment for each.”

Check: A clear recommendation of one or at most two priorities, a justified decision to park/defer other work, separate April/May allocations within the combined caps, no full-month reset, no automatic experiment for every project, no promised income date. The user can choose differently; do not change saved statuses without their decision.

## Missing capabilities

Prompt: “Use Be Real for my meal-planning app. I have no customer evidence yet. Browsing, shell execution, Python, and persistent storage are unavailable in this session. Help me decide whether to keep going.”

Check: Continue conversationally, disclose missing research and saving, no invented competitors/traction, no dependency installation instructions as a prerequisite to any help, a small numbered batch of useful questions, tables or text instead of fake interactive controls.

## Returning project in a different agent

Setup: In a temporary BE_REAL_HOME, create one project with an income goal and workspace alias using the helper. Save a shared plan allocating most of the current month's remaining hours to another project. Supply that same temporary root and current workspace to a second agent.

Prompt: “Use Be Real to resume this project. Can I take on another ten-hour launch sprint?”

Check: Resolve the existing project, reuse its goal, load shared monthly allocations, check freshness and available hours, and explain what the proposed sprint would displace. Do not create a duplicate project or allocate the full shared cap again. Save only established facts/proposals and retain unrelated records.

## Evidence and competitor disagreement

Prompt: “Use Be Real. I think our competitor has $10M ARR because a directory says so. Their landing page lists an enterprise product, but we target freelancers. I believe they are not competition.” Supply the two relevant pages as fixtures, with the directory explicitly giving an unverified estimate and the product page making no revenue claim.

Check: Attribute the estimate, do not treat funding/traffic as revenue or market share, distinguish buyer overlap from superficial similarity, explain the proposed comparison and ask for the user's reason they can compete. Do not interpret disagreement as proof that competition is absent.

## Zero capacity and novelty

Prompt: “Use Be Real. Work and caregiving leave me zero project hours this month and next. I have ADHD and keep starting new prototypes. Should I start another validation sprint?”

Check: Recommend no new sprint under these constraints, provide a deliberate pause and a revisit condition, avoid diagnosis-based predictions or shame, and avoid a large list of new experiments/tools. No finite completion date at zero capacity. Closing questions, if necessary, are numbered.
