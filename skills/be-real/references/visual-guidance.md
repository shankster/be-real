# Visual conversations

Make Be Real assessments easy to explore visually. Proactively choose images, diagrams, or an interactive view for substantive findings instead of waiting for a separate request. Use the smallest useful visual for the current decision; do not build an elaborate dashboard before the user has supplied meaningful inputs.

## Match the visual to the question

| Question | Useful visual or interaction |
| --- | --- |
| Which projects fit this month and next month? | Two separately labeled monthly allocation charts or one compact table covering the remaining current month and the following month. Show the shared cap, all project allocations, buffer, unallocated time or shortfall, and outside-work commitments that shaped each cap. Highlight the one or two proposed priorities and explicitly list parked work. |
| What progress are we actually making? | A timeline of accepted workflows over the last few months, with partial work and design revisions distinguished from completed functionality. Separate historical evidence from forecast ranges; do not treat unequal features as equal units of progress. |
| Which work needs learning or help? | A task-by-task proficiency comparison linked to actual experience, showing learning or feedback work alongside delivery tasks without invented skill scores. |
| What makes the remaining work hard? | A dependency diagram showing the path from the current prototype to the chosen milestone, including investigations and external waits. |
| Are these really competitors? | A linked comparison with real product images or screenshots where useful, reasons for inclusion, differences, and a way to record agreement, disagreement, or uncertainty. |
| What would make the project worthwhile? | A scenario explorer for available hours, price, customer acquisition, retention, and operating costs, showing their effects on calendar time and financial outcomes. Use only the inputs relevant to this product. |
| Should I continue, narrow, or park it? | A short decision tree tied to evidence, available capacity, priority among projects, and the user's stated reasons for possibly stopping. |

Choose one or a few views that resolve the current question rather than producing every example. Use evidence-bearing images, such as inspected competitor screenshots or workflow illustrations, when they clarify a concrete difference. Label an illustration as such; a generated image or invented screenshot must never stand in for product evidence.

## Build and present

Use the host's supported presentation capabilities. A Markdown table is the portable default; use Mermaid for compact flows only when supported, interactive artifacts when available, and standard plotting tools for exportable figures. No named visualization plugin is required. Use an image-generation capability for an illustration only when a bitmap serves the explanation. If the preferred capability is unavailable, provide a supported static visual or a concise table and explanation; do not claim interactivity that is absent. These are presentation choices, not reasons to publish a website or modify the user's product.

Keep researched inputs, assumptions, sources, dates, units, and uncertainty visible. Prefer qualitative relationships or an explicitly hypothetical example when data is missing. Do not invent market shares, competitor scores, precise timelines, or an abandonment-risk gauge to fill a chart. Avoid positioning maps whose axes imply measurements the research did not establish.

When visualizing competitor traction, keep source links and evidence labels beside the figures. Compare the same metrics, periods, and company or product scope, and mark missing data as unknown rather than plotting zero. Use a market-share chart only with a defensible common denominator; do not mix funding, revenue, and estimated traffic into one ranking.

Interactions must change the relevant calculations or comparison, not just decorate the answer. Check that outputs update consistently, units match, and boundary cases are honest: zero available hours gives no finite completion time; losses or insufficient growth can mean no payback within the horizon. Show overallocated time explicitly. A user's scenario adjustment is exploration, not proof of demand or a commitment to that plan.

Never show a fresh full-month allowance for a month already in progress, or carry this month's capacity into next month without evidence. Interactive allocations must share one cap per month: increasing one project's hours consumes capacity available to the others. Flag a third proposed priority or a budget shortfall rather than silently expanding the available hours. Keep the initial view focused on the recommendation; interaction should clarify the tradeoff, not create another overwhelming menu of possible projects.

For competitor review, keep each candidate's rationale and source accessible. Record the user's review only after an explicit response or submission; a default selection is not agreement. Incorporate feedback into the assessment rather than leaving it inside a disconnected widget. Where a visual cannot send feedback to the conversation, ask for the response in chat and explain that limitation.

Make controls labeled and keyboard accessible, keep essential information available without hovering, and pair color with text or shapes. Verify the rendered view and key interactions when the environment supports it; state any material verification limitation. Keep the conclusion and next question concise, with enough text to remain understandable if the visual is unavailable.
