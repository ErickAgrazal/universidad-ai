---
name: create-teams-assignment
description: Create a new assignment in Microsoft Teams (Classroom Assignments) via Playwright. Supports title, instructions, points, due date, and an attached criteria rubric with scale + weighted criteria. Saves as draft for teacher review or publishes directly. Use when the user asks to add/create/draft an assignment in a Teams class, optionally generating the rubric from a description.
---

# Create a Teams Classroom Assignment

End-to-end workflow to create a new assignment in a Microsoft Teams class — including title, instructions, points, due date, and a multi-criterion weighted rubric — entirely through the Playwright MCP. Built from the A7 ("Parcial #2: MVP Startup Full Stack") creation session in May 2026.

## When to invoke

- User asks "crea la asignación X" / "add a new assignment for Y" / "draft this for my Teams class"
- User provides: a title, an instructions blob, optionally a rubric (5-criterion × 4-level is the dominant pattern)
- User confirms which class team(s) the assignment belongs to (the skill always asks ONCE if not specified)

## Prerequisites

- User is signed into Teams in the active Playwright browser context
- Playwright MCP server available (`mcp__playwright__*`)
- The class team exists and the user has Educator/Owner permission

## Inputs the skill needs (ask once, then run autonomous)

Before starting, confirm:

1. **Title** — full assignment name (e.g. "7. Parcial #2: MVP de Aplicación Startup Full Stack en Grupo"). Pattern observed: `<N>. <Type>: <Topic>` where Type ∈ {Laboratorio, Investigación, Presentación Grupal, Informe Escrito Grupal, Suite de pruebas, Parcial}.
2. **Instructions** — multi-paragraph description. Plain text typed into a contenteditable editor (no rich markdown rendered, but bullets via `-`/`1.` look fine).
3. **Points** — usually 100. The skill enables the per-criterion weights toggle so each rubric criterion contributes a percentage.
4. **Rubric** — optional but recommended:
   - **Scale** — comma-separated levels, e.g. `Excelente, Bueno, Normal, Deficiente` (4 levels is the local convention)
   - **Criteria** — list of N criterion names (5 × 20% is the dominant pattern)
   - **Cells** — N × scale_count descriptions, one per (criterion, level) cell
   - **Weights** — N weights summing to 100 (typically 20 each for 5 criteria)
5. **Due date / time** — defaults to "tomorrow 11:59 PM". The teacher adjusts in the form before publishing.
6. **Class teams** — one or more. The skill loops over each, creating the same assignment as a draft per class.
7. **Final action** — `save as draft` (default — teacher reviews before publishing) or `assign now` (publishes immediately).

## Autonomy contract

The skill is autonomous from inputs to draft. It does NOT click "Assign" (publish) unless explicitly told. Always saves as draft first so the teacher can:
- Verify the rendered description
- Adjust due date / time
- Attach additional files (e.g. PDF rubric reference)
- Add or fine-tune the AI guidelines

## Workflow (single class — repeat per class team)

### Phase 1 — Navigate to Assignments

```js
// Click into the class team
await page.getByText('<CLASS_TEAM_NAME>').first().click();
// Then click Assignments treeitem
await page.getByRole('treeitem', { name: 'Assignments' }).click();
// Wait for the assignments iframe to fully load
await page.waitForTimeout(3000);
```

### Phase 2 — Open the "New assignment" form

```js
const frame = page.locator('iframe').first().contentFrame();
// Click "Create assignment" (opens a menu)
await frame.getByRole('button', { name: 'Create assignment' }).click();
await page.waitForTimeout(1500);
// Click "New assignment" menu item (other options: New quiz, From existing, Learning Accelerators)
await frame.locator('[role="menuitem"]:has-text("New assignment")').click();
await page.waitForTimeout(5000);
```

### Phase 3 — Fill the basic fields

```js
// Title — plain input
await frame.locator('input[placeholder="Enter title"]').fill(title);

// Instructions — contenteditable div, NOT a textarea
await frame.locator('div[aria-label="Enter instructions"]').click();
await page.keyboard.type(instructions, { delay: 1 });

// Points — there's a "Points" checkbox toggle for per-criterion grading. For
// rubric-based assignments, leave it unchecked here; we'll enable it INSIDE the
// rubric editor (where it controls per-criterion weights).
```

**Other available fields on the form (skip unless requested):**
- "Add learning objective", "Add detail", "Add steps", "Add hint" — pedagogical metadata
- "Attach" (id `learningZone`) — file/link attachment menu
- "Add tag", "Add standards" — categorization
- "Set student AI guidelines" — chooses an AI use policy level
- "Edit assignment timeline" — date/time picker (default = tomorrow 11:59 PM)

### Phase 4 — Add a rubric (optional but typical)

```js
// 1. Open the rubric flow
await frame.locator('button[aria-label="Add rubric"]').click();
await page.waitForTimeout(2500);

// 2. Choose "Create rubric from scratch"
// Other options shown:
//   - "Create rubric using AI" (auto-generates from the assignment description)
//   - "Or upload existing rubric"
await frame.locator('button[aria-label^="Create rubric from scratch"]').click();
await page.waitForTimeout(3500);
```

#### Rubric step A — title + description

```js
await frame.locator('input[placeholder="Enter a title"]').fill('<RUBRIC_NAME>');
await frame.locator('span[aria-label="Enter your rubric description"]').click();
await page.keyboard.type('<RUBRIC_DESCRIPTION>', { delay: 2 });
await frame.locator('button:has-text("Next")').first().click();
await page.waitForTimeout(3000);
```

#### Rubric step B — scale + criteria

The form shows ONE input for the scale (placeholder `Excellent, Good, Fair, Poor`) and ONE input for the first criterion. Type the scale as a comma-separated list; then click "New criteria" once per additional criterion and fill each.

```js
// Scale (4-level local convention)
await frame.locator('input[placeholder="Excellent, Good, Fair, Poor"]')
  .fill('Excelente, Bueno, Normal, Deficiente');

// First criterion goes into the visible input
await frame.locator('input[placeholder="Enter criteria"]').fill(criteria[0]);

// Subsequent criteria: click "New criteria" and fill the LAST input each time
for (let i = 1; i < criteria.length; i++) {
  await frame.locator('button:has-text("New criteria")').click();
  await page.waitForTimeout(450);
  const ins = frame.locator('input[placeholder="Enter criteria"]');
  const n = await ins.count();
  await ins.nth(n - 1).fill(criteria[i]);
  await page.waitForTimeout(200);
}

// Advance to the cell matrix
await frame.locator('button:has-text("Next")').first().click();
await page.waitForTimeout(4000);
```

#### Rubric step C — fill the cell matrix

After step B, the form expands into an N × scale_count matrix of `textarea[aria-label="Criteria"]` cells in DOM order: row by row, left to right. For 5 criteria × 4 levels, you get 20 textareas indexed 0-19.

```js
// cells array: 20 strings in row-major order
//   index 0-3:  row 1, columns Excelente / Bueno / Normal / Deficiente
//   index 4-7:  row 2, …
//   index 16-19: row 5
const ta = frame.locator('textarea[aria-label="Criteria"]');
for (let i = 0; i < cells.length; i++) {
  await ta.nth(i).fill(cells[i]);
  await page.waitForTimeout(80);
}
```

#### Rubric step D — enable points + per-criterion weights

The "Points" element on this screen is a **toggle switch** (`input#pointsToggle`, type=checkbox role=switch), NOT a numeric input. Clicking it ON exposes per-criterion `Weight` inputs.

```js
await frame.locator('input#pointsToggle').click({ force: true });
await page.waitForTimeout(1500);

// One Weight input per criterion appears
const weights = frame.locator('input[aria-label="Weight"]');
for (let i = 0; i < criteria.length; i++) {
  await weights.nth(i).fill('20');   // 5 criteria × 20 = 100
  await page.waitForTimeout(120);
}
```

#### Rubric step E — attach back to the assignment

There are TWO buttons with text "Attach" visible on this page:
- `button[aria-label="Open Attach menu"]` — the assignment form's file-attach menu (top of the form)
- `button` with empty aria-label and visible text "Attach" — the **rubric attach** action (only in the rubric editor)

Pick the second one:

```js
const allAttach = frame.locator('button').filter({ hasText: /^Attach$/ });
const n = await allAttach.count();
let rubricBtn = null;
for (let i = 0; i < n; i++) {
  const el = allAttach.nth(i);
  if (!(await el.getAttribute('aria-label'))) { rubricBtn = el; break; }
}
await rubricBtn.scrollIntoViewIfNeeded();
await rubricBtn.click({ force: true });
await page.waitForTimeout(5000);
```

After this you're back on the assignment form with the rubric attached (shown as a clickable card under the "Add rubric" placeholder).

### Phase 5 — Save as draft

```js
await frame.locator('button[data-test="save-draft"]').scrollIntoViewIfNeeded();
await frame.locator('button[data-test="save-draft"]').click({ force: true });
await page.waitForTimeout(5000);
```

The form does NOT navigate away on its own. The success signal is a small "Draft 1 of 1" alert inside the page (use `frame.locator('[role="alert"]').textContent()` to detect it).

### Phase 5b — Publish (Assign) — when ready to push to students

After review, the teacher (or skill on user's command) publishes by setting the date and clicking Assign:

```js
// Open the draft from the Drafts tab
await frame.getByRole('tab', { name: 'Drafts' }).click();
await frame.getByText(titleSubstring).first().click();
await page.waitForTimeout(4500);

// Set due date via the calendar (typing into the input does NOT work — must click the calendar cell)
await frame.locator('input[aria-label^="Select a due date"]').click();
await page.waitForTimeout(1500);
// aria-label format: "DD, Month, YYYY" — e.g. "22, May, 2026"
await frame.locator(`button[aria-label="${dd}, ${monthName}, ${yyyy}"]`).click();
await page.waitForTimeout(800);

// Click Assign — disambiguate from "Edit assignment timeline" button by exact text match
const assignBtns = frame.locator('button').filter({ hasText: /^Assign$/ });
await assignBtns.first().scrollIntoViewIfNeeded();
await assignBtns.first().click({ force: true });
await page.waitForTimeout(5000);
```

Success signal: the assignment moves from Drafts tab to Upcoming tab, and the URL returns to `/list`.

### Phase 5c — Publish directly from the New-assignment form with a custom due TIME

You do NOT need the save-draft → reopen → Assign round-trip to publish. The New-assignment form (Phase 3) already carries the due date AND a due **time** field, both editable in place, then Assign. Use this when the user gives a specific due date/time up front (validated 2026-06-19, A12 in both 241 & 242, due 11:00 PM):

```js
// Due DATE — click the input to open the calendar, then click the day cell.
// On the form the input is data-test="due-date" (NOT the legacy aria-label selector).
await frame.locator('input[data-test="due-date"]').click();
await page.waitForTimeout(1500);
await frame.locator(`button[aria-label="${dd}, ${monthName}, ${yyyy}"]`).click(); // e.g. "24, June, 2026"
await page.waitForTimeout(1000);

// Due TIME — input[data-test="due-time"] (default "11:59 PM"). Clear, type, pick the option.
const t = frame.locator('input[data-test="due-time"]');
await t.click(); await t.fill(''); await t.type('11:00 PM', { delay: 40 });
await page.waitForTimeout(1000);
const opt = frame.getByRole('option', { name: /^11:00 PM$/ });
if (await opt.count()) await opt.first().click(); else await page.keyboard.press('Enter');

// Assign (exact-text match; verify date+time inputValue() before clicking)
await frame.locator('button').filter({ hasText: /^Assign$/ }).first().click({ force: true });
```

Note the selector difference: on the **form**, the due-date input is `input[data-test="due-date"]`; when reopening a **draft** (Phase 5b) it's `input[aria-label^="Select a due date"]`. Both open the same calendar; the day-cell `button[aria-label="DD, MonthName, YYYY"]` is identical (English month names).

### Phase 7 — Edit a LIVE (already-published) assignment's timeline (e.g. extend the close/late date)

To change an existing assignment's **close date** (the late-submission cutoff) WITHOUT touching the due/delivery date — e.g. "reopen A10 for late turn-ins until Sunday" (validated 2026-06-19, A10 in both classes: due stayed Jun 12, close moved Jun 13 → Jun 21):

```js
// 1. Open the assignment from its tab (Past due / Ready to grade / Upcoming), then:
await frame.getByRole('button', { name: 'More options' }).first().click();
await page.waitForTimeout(1800);
await frame.locator('[role="menuitem"]:has-text("Edit assignment")').first().click();
await page.waitForTimeout(5000);

// 2. GOTCHA: a "Tips / Align to standards" popup card often steals focus on the edit screen.
//    Dismiss it or the timeline button click is swallowed.
const ml = frame.getByText('Maybe later', { exact: true });
if (await ml.count()) await ml.first().click({ force: true });
await page.waitForTimeout(1200);

// 3. Open the timeline dialog. It exposes 5 inputs, all data-test scoped:
//    timeline-due-date / timeline-due-time / timeline-close-date / timeline-close-time
//    + a checkbox "Close all submissions at the close date" (leave ON).
await frame.getByRole('button', { name: 'Edit assignment timeline' }).click({ force: true });
await page.waitForTimeout(3000);
const dlg = frame.getByRole('dialog').filter({ hasText: 'Edit assignment timeline' }).first();

// 4. Change ONLY the close date via the calendar (leave due-date untouched so existing
//    submissions stay marked late). Same day-cell aria-label format.
await dlg.locator('input[data-test="timeline-close-date"]').click();
await page.waitForTimeout(1500);
await frame.locator(`button[aria-label="${dd}, ${monthName}, ${yyyy}"]`).click(); // e.g. "21, June, 2026"
await page.waitForTimeout(1000);

// 5. Confirm dialog (Done) then save the assignment (Update — NOT "Assign", it's already live).
await dlg.locator('button').filter({ hasText: /^Done$/ }).first().click({ force: true });
await page.waitForTimeout(2500);
await frame.locator('button').filter({ hasText: /^Update$/ }).first().click({ force: true });
await page.waitForTimeout(6000);
// Verify on the detail header: "Due June 12, 2026 11:59 PM • Closes June 21, 2026 11:59 PM"
```

Notes:
- Editing the timeline does **not** re-notify students (no new assignment notification fires) — tell the teacher to message students that the late window reopened.
- Submission counts / grades are preserved through the edit.
- Repeat per class team; rubric/timeline are per-team, not propagated.

### Phase 6 — Verify in Drafts tab

```js
await page.locator('iframe').first().evaluate((iframe) => {
  iframe.contentWindow.location.href = `https://assignments.edu.cloud.microsoft/classes/${CLASS_ID}/list`;
});
await page.waitForTimeout(4000);
await frame.getByRole('tab', { name: 'Drafts' }).click();
await page.waitForTimeout(1500);
// The new draft should appear in the Drafts list with the title you provided
```

## Across multiple class teams

Loop Phases 1-6 once per class. The rubric must be re-created per class (Teams class rubrics don't propagate across teams). Keep the rubric definition (scale + criteria + cells + weights) in a single JS array and reuse it; only the navigation step changes.

## Gotchas (learned from A7 creation session)

| Gotcha | Symptom | Fix |
|---|---|---|
| `Create assignment` is a menu trigger, not a direct action | Clicking it opens a dropdown with options (New assignment / New quiz / From existing / Learning Accelerators); the form doesn't appear | Click `button:has-text("Create assignment")`, wait 1.5s, then click `[role="menuitem"]:has-text("New assignment")`. |
| Instructions is a contenteditable `div`, not a textarea | `.fill()` on it silently fails or types nothing | Use `await editor.click()` then `await page.keyboard.type(text, {delay: 1})` |
| `input[aria-label="Points"]` on the assignment form is a toggle, not a value | `fill('100')` throws "Input of type checkbox cannot be filled" | Skip it on the form. Enable points INSIDE the rubric editor via `input#pointsToggle`, where it exposes per-criterion `Weight` inputs |
| Two buttons share the visible text "Attach" | The first match (assignment form's `Open Attach menu`) is invisible (scrolled off-screen) and clicking it times out | Filter `button:has-text(/^Attach$/)` to the one with empty aria-label; that's the rubric Attach. Always `scrollIntoViewIfNeeded()` before clicking it |
| Save-as-draft has no redirect/confirmation | The button click succeeds but the URL stays the same and the form stays open | Detect success via the `[role="alert"]` toast saying "Draft 1 of 1". Then navigate manually to `.../classes/<cid>/list` and check the Drafts tab |
| Rubric criteria input only shows ONE field on step B | Looks like the rubric only supports one criterion | Click `button:has-text("New criteria")` once per additional criterion; the new input is the LAST in the DOM order |
| Rubric scale takes a comma-separated string, not 4 separate inputs | The placeholder `Excellent, Good, Fair, Poor` is misleading — looks like an example value but it's the actual format expected | Fill with `Excelente, Bueno, Normal, Deficiente` (or any 2-6 comma-separated levels) |
| Rubric matrix cells fill in DOM-order, not visual-grid-order | If the visual layout suggests columns first, you might fill row-by-column instead of row-by-row | DOM order IS row-major (row 1 cols 1-4, row 2 cols 1-4, …). `textarea[aria-label="Criteria"].nth(i)` where `i = row*scale_count + col` |
| Weights must sum to 100, otherwise save fails silently | After fill, save-as-draft completes but the rubric appears without weights when reopened | Always set 5 × 20 (or N × (100/N)) and verify with `await weights.allInnerValues()` before clicking Attach |
| Pre-existing drafts persist | If the teacher previously started the same assignment, both drafts coexist in the Drafts tab | After saving the new one, list all Drafts and surface the names to the user; they pick which to delete |
| Date picker input ignores typed text | Typing "Fri, May 22, 2026" into `input[aria-label^="Select a due date"]` + Enter does NOT update the date (input value reverts) | Click the input to OPEN the calendar dropdown, then click the day cell: `button[aria-label="DD, MonthName, YYYY"]` (e.g. `"22, May, 2026"`). The aria-label format is locale-stable English month names regardless of the user's interface language |
| Two "Assign-named" buttons coexist on a draft | "Edit assignment timeline" button (top) and the actual "Assign" submit button (bottom-right). `:has-text("Assign")` matches both | Use exact-text filter: `button.filter({ hasText: /^Assign$/ })`. The first match is the submit button. Always `scrollIntoViewIfNeeded()` before clicking |
| Assign click silently fails if date picker is still open | The calendar dropdown overlay can swallow the click event | After picking the date, wait ~800ms for the calendar to close before clicking Assign |

## Style conventions (matched against existing class assignments)

- Title pattern: `<N>. <Type>: <Topic>` — e.g. "5. Laboratorio: PollClass — Desarrollo Agéntico Full Stack"
- Instructions: open with a one-sentence purpose, then sectioned with `Stack técnico requerido:`, `Entregables:`, `Demo en clase:` (or similar)
- Bullet markers: `-` for plain lists, `1.` for ordered (renders correctly in Teams' editor)
- Rubric default: 5 criteria × 20% weight × 4-level scale (Excelente/Bueno/Normal/Deficiente)
- Default Points field on form: leave blank (rubric handles weighted scoring via its own per-criterion weights)
- Save action: always Save-as-draft first; the teacher publishes manually

## Helper files

- `lib/create_assignment.js` — Reusable Playwright snippets for each phase, designed to be pasted into `mcp__playwright__browser_run_code_unsafe`. Each phase as an async function so the agent can compose them as needed.
- `lib/parcial_2_example.json` — Concrete rubric data structure example from the A7 session (scale + criteria + cells + weights).

## Closing checklist (agent verifies before handoff)

- [ ] Draft created in every requested class team (verify via Drafts tab)
- [ ] Title matches user's input exactly (no Whisper/transcript-style mangling)
- [ ] Instructions show the bullet/list structure intended (re-open the draft and skim)
- [ ] Rubric attached: rubric card visible under "Add rubric" in the draft view
- [ ] Rubric weights sum to 100 (`weights.allInnerValues().reduce((s,v)=>s+Number(v),0) === 100`)
- [ ] Due date set per user request OR flagged as "default tomorrow 11:59 PM, please adjust"
- [ ] Agent reports back with: class teams updated, draft URL(s) or "in Drafts tab", and any pre-existing duplicate draft names found
- [ ] Agent does NOT click Assign/Publish unless explicitly told

---

## Forms quiz assignments (Microsoft Forms inside Teams)

For quiz-type assignments (multiple choice + development questions), use `lib/create_quiz.js`. **Critical:** the Forms quiz MUST be opened via Teams → Create → New quiz → **Add quiz** so it associates with the class. Opening `forms.office.com` directly creates an orphan quiz that cannot be reattached. (Failed orphan during 2026-05-18 session; user corrected: "El forms tienes que abrirlo desde la creación de la asignación en teams, para que se asocie".)

### Forms editor gotchas

1. **Collapsed-question editor**: only the focused question shows option textboxes & points input. Other questions render as compact buttons (`button[aria-label^="N. Question title ..."]`). All `nth()` selectors for options/correct/points are **local to the current question** — do not try to track cumulative indices across questions.
2. **Added options have pre-filled text "Option N"**: after clicking `Add option`, the new option's textbox is not empty — it contains "Option 3" or "Option 4". Must `ControlOrMeta+A` + `Backspace` before typing, or text becomes "Option 3Docker Compose".
3. **Question title placeholder is also literal text "Question"**: same clear-before-typing rule applies, else first character of question becomes "Question¿Cuál...".
4. **Toggle Multiple answers BEFORE marking correct answers**: switches the UI mode (radio → checkbox) which resets prior correct-marks.
5. **"Add new question" opens a TYPE PICKER**, not auto-Choice. After the first question, you must click `button[aria-label="Choice"]` (or `Text`) each time.
6. **Title editor visibility**: the title `div[contenteditable="true"][aria-label="Form title"]` is only present when the form header is focused. Click the description placeholder text first to defocus any active question.
7. **Copilot "Draft with Copilot" panel** opens by default. Close with `button[aria-label="Close"]`. Otherwise it tries to auto-generate questions from your prompt and produces "I have 5 suggestions" banners.
8. **Quiz duration**: not in question editor — under Settings (gear icon) → toggle "Set time duration" → input minutes.
9. **Done button to attach**: top-right "Done" button (NOT inside Forms frame — it's in the Teams iframe wrapper) is what attaches the quiz to the assignment and brings you back to the assignment editor. After that, set title (overwrites Forms title), instructions, dates.

### Schedule for future post

When `Schedule the assignment in the future` switch is on:
- The bottom-right button changes from "Assign" to "Schedule"
- Use `data-test="timeline-due-date"` / `timeline-due-time` selectors to avoid strict-mode collision with the outer (legacy) due-date inputs
- Close timeline dialog with `button[aria-label="Done. Go back to the assignment editor"]`

### Validated pattern (2026-05-18, A8 Parcial Teórico)

20 MC (3 pts each, some multi-answer) + 2 Text (10 pts each, long answer) = 80 pts, 20-min timer, scheduled for future date. Worked in both classes (1GS241 + 1GS242). See `lib/create_quiz.js`.

### Re-editing an existing question

When user gives feedback on a specific question after the quiz is built (e.g. "Q21 has too many sub-questions"), click `button[aria-label^="N. Question title ..."]` to refocus that question — it expands back into edit mode. The currently-edited question collapses. Then use `clearAndType` on `div[role="textbox"][aria-label^="Question title N"]`.

### Re-opening Forms from a draft/edited assignment

After "Done" returns you to the assignment editor, the quiz appears as an attachment. To re-edit:
- Click `button[aria-label^="Attachment <quiz title> (<class name>)"]` — re-opens Forms in the nested frame.
- The top-right button now reads **"Close"** instead of "Done" (different flow: `teamsFrame.locator('button').filter({ hasText: /^Close$/ })`).
- Edit, then click Close to return to the assignment editor with changes saved.

### Quiz design principles (user-validated 2026-05-18)

1. **Dev questions = ONE concept each**, not bundled. User correction: "parecen 3 preguntas en 1. Debería ser solo 1." Each `dev` item should test a single analytical skill, not chain 3 prompts with "Luego... Finalmente...".
2. **MC distribution across all groups**: if 12 A4 groups exist, aim for at least 1 MC per group's topic. Use a `_topics_covered` array in the JSON to track coverage and audit gaps.
3. **Timer window**: for a `duration` of N minutes, set `dueTime = postTime + (N + 10) min`. Gives a 10-min late-arrival buffer without enabling re-attempts. For N=20: post 8:00 PM → due 8:30 PM.

### `quizN.json` schema as idempotent source-of-truth

Save quiz spec to `class<N>_quiz.json` BEFORE running the Playwright flow. The schema:

```json
{
  "_class": "1GS241",
  "_schedule": "Wed May 20, 2026 — 8:00 PM Panama time",
  "_duration_min": 20,
  "_scoring": {"mc_each": 3, "dev_each": 10, "total": 80},
  "_topics_covered": ["topic1", "topic2", ...],
  "mc": [
    { "n": 1, "topic": "...", "q": "...", "options": ["a","b","c","d"], "correct": [1], "multi": false },
    ...
  ],
  "dev": [
    { "n": 21, "points": 10, "q": "..." },
    ...
  ]
}
```

Benefits:
- **Auditable**: user can review questions + correct answers before the flow runs.
- **Idempotent re-runs**: if a question needs fixing, edit JSON + re-run only that section.
- **Diff-friendly**: changes in correct answers or wording show cleanly in git.
- **Reusable**: same schema for both classes; just swap topic content per class's A4 groups.
