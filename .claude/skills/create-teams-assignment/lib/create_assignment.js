// Reusable Playwright snippets for creating a Teams classroom assignment.
// Pasted into `mcp__playwright__browser_run_code_unsafe`.
// Each phase is a self-contained async function; compose as needed.


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 1 — Navigate to a class team's Assignments tab
// ─────────────────────────────────────────────────────────────────────────────
async function navigateToAssignments(page, className) {
  await page.goto('https://teams.microsoft.com/v2/');
  await page.waitForTimeout(5000);
  await page.getByRole('button', { name: 'Teams (⌃ ⇧ 3)' }).click().catch(() => null);
  await page.waitForTimeout(2500);
  await page.getByText(className).first().click();
  await page.waitForTimeout(3000);
  await page.getByRole('treeitem', { name: 'Assignments' }).click();
  await page.waitForTimeout(3000);
}


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 2 — Open the New assignment form
// ─────────────────────────────────────────────────────────────────────────────
async function openNewAssignmentForm(page) {
  const frame = page.locator('iframe').first().contentFrame();
  await frame.getByRole('button', { name: 'Create assignment' }).click();
  await page.waitForTimeout(1500);
  await frame.locator('[role="menuitem"]:has-text("New assignment")').click();
  await page.waitForTimeout(5000);
}


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 3 — Fill the basic fields (title + instructions)
// ─────────────────────────────────────────────────────────────────────────────
async function fillBasicFields(page, title, instructions) {
  const frame = page.locator('iframe').first().contentFrame();
  await frame.locator('input[placeholder="Enter title"]').fill(title);
  await page.waitForTimeout(400);
  await frame.locator('div[aria-label="Enter instructions"]').click();
  await page.waitForTimeout(300);
  await page.keyboard.type(instructions, { delay: 1 });
  await page.waitForTimeout(500);
}


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 4 — Add a multi-criterion weighted rubric
//
// rubric = {
//   title: "Parcial2-StartupFullStack",
//   description: "Rúbrica de evaluación: 5 criterios × 20% = 100 puntos.",
//   scale: "Excelente, Bueno, Normal, Deficiente",     // comma-separated
//   criteria: ["Funcionalidad", "Arquitectura", ...],  // N criteria
//   cells: [c1L1, c1L2, c1L3, c1L4, c2L1, ..., cNL4],  // row-major
//   weights: [20, 20, 20, 20, 20],                      // sum=100
// }
// ─────────────────────────────────────────────────────────────────────────────
async function attachRubric(page, rubric) {
  const frame = page.locator('iframe').first().contentFrame();

  // 4.0 Open the rubric flow
  await frame.locator('button[aria-label="Add rubric"]').click();
  await page.waitForTimeout(2500);
  await frame.locator('button[aria-label^="Create rubric from scratch"]').click();
  await page.waitForTimeout(3500);

  // 4.A Title + description
  await frame.locator('input[placeholder="Enter a title"]').fill(rubric.title);
  await page.waitForTimeout(300);
  await frame.locator('span[aria-label="Enter your rubric description"]').click();
  await page.waitForTimeout(200);
  await page.keyboard.type(rubric.description, { delay: 2 });
  await page.waitForTimeout(400);
  await frame.locator('button:has-text("Next")').first().click();
  await page.waitForTimeout(3000);

  // 4.B Scale + criteria
  await frame.locator('input[placeholder="Excellent, Good, Fair, Poor"]').fill(rubric.scale);
  await page.waitForTimeout(300);
  await frame.locator('input[placeholder="Enter criteria"]').fill(rubric.criteria[0]);
  await page.waitForTimeout(300);
  for (let i = 1; i < rubric.criteria.length; i++) {
    await frame.locator('button:has-text("New criteria")').click();
    await page.waitForTimeout(450);
    const ins = frame.locator('input[placeholder="Enter criteria"]');
    const n = await ins.count();
    await ins.nth(n - 1).fill(rubric.criteria[i]);
    await page.waitForTimeout(200);
  }
  await frame.locator('button:has-text("Next")').first().click();
  await page.waitForTimeout(4000);

  // 4.C Fill the matrix cells (row-major)
  const ta = frame.locator('textarea[aria-label="Criteria"]');
  for (let i = 0; i < rubric.cells.length; i++) {
    await ta.nth(i).fill(rubric.cells[i]);
    await page.waitForTimeout(80);
  }

  // 4.D Enable points + fill per-criterion weights
  await frame.locator('input#pointsToggle').click({ force: true });
  await page.waitForTimeout(1500);
  const weights = frame.locator('input[aria-label="Weight"]');
  for (let i = 0; i < rubric.weights.length; i++) {
    await weights.nth(i).fill(String(rubric.weights[i]));
    await page.waitForTimeout(120);
  }

  // 4.E Attach back to the assignment — careful: TWO "Attach" buttons exist
  const allAttach = frame.locator('button').filter({ hasText: /^Attach$/ });
  const count = await allAttach.count();
  let rubricAttach = null;
  for (let i = 0; i < count; i++) {
    const aria = await allAttach.nth(i).getAttribute('aria-label');
    if (!aria) { rubricAttach = allAttach.nth(i); break; }
  }
  if (!rubricAttach) throw new Error('Rubric Attach button not found');
  await rubricAttach.scrollIntoViewIfNeeded({ timeout: 5000 });
  await page.waitForTimeout(500);
  await rubricAttach.click({ force: true });
  await page.waitForTimeout(5000);
}


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 5 — Save as draft
// ─────────────────────────────────────────────────────────────────────────────
async function saveAsDraft(page) {
  const frame = page.locator('iframe').first().contentFrame();
  await frame.locator('button[data-test="save-draft"]').scrollIntoViewIfNeeded({ timeout: 5000 });
  await page.waitForTimeout(500);
  await frame.locator('button[data-test="save-draft"]').click({ force: true });
  await page.waitForTimeout(5000);
  // Detect success
  const alerts = await frame.locator('[role="alert"]').evaluateAll(els =>
    els.map(e => (e.textContent||'').trim()).filter(t => /draft|borrador/i.test(t)).slice(0, 3));
  return alerts;
}


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 6 — Verify draft appears in Drafts tab
// ─────────────────────────────────────────────────────────────────────────────
async function verifyDraft(page, classId, expectedTitle) {
  const frame = page.locator('iframe').first().contentFrame();
  await page.locator('iframe').first().evaluate((iframe, cid) => {
    iframe.contentWindow.location.href = `https://assignments.edu.cloud.microsoft/classes/${cid}/list`;
  }, classId);
  await page.waitForTimeout(4000);
  await frame.getByRole('tab', { name: 'Drafts' }).click().catch(() => null);
  await page.waitForTimeout(1500);
  const drafts = await frame.locator('group, [role="listitem"]').evaluateAll(els =>
    els.map(e => e.textContent?.trim() || '').filter(Boolean).slice(0, 20));
  return {
    found: drafts.some(d => d.includes(expectedTitle)),
    all_drafts: drafts.filter(d => /^\d\./.test(d)),
  };
}


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 5b — Publish (Assign) with a specific due date
//
// dueDate format: { day: 22, month: "May", year: 2026 }   // English month names
// Opens an existing draft, sets the date via calendar click, clicks Assign.
// ─────────────────────────────────────────────────────────────────────────────
async function publishAssignment(page, titleSubstring, dueDate) {
  const frame = page.locator('iframe').first().contentFrame();
  await frame.getByRole('tab', { name: 'Drafts' }).click();
  await page.waitForTimeout(1500);
  await frame.getByText(titleSubstring).first().click();
  await page.waitForTimeout(4500);
  // Date picker: click input, then click the day cell
  await frame.locator('input[aria-label^="Select a due date"]').click();
  await page.waitForTimeout(1500);
  const aria = `${dueDate.day}, ${dueDate.month}, ${dueDate.year}`;
  await frame.locator(`button[aria-label="${aria}"]`).click();
  await page.waitForTimeout(800);
  // Assign — exact-text match to disambiguate from "Edit assignment timeline"
  const assignBtns = frame.locator('button').filter({ hasText: /^Assign$/ });
  await assignBtns.first().scrollIntoViewIfNeeded({ timeout: 5000 });
  await page.waitForTimeout(500);
  await assignBtns.first().click({ force: true });
  await page.waitForTimeout(5000);
  // Verify in Upcoming
  await frame.getByRole('tab', { name: 'Upcoming' }).click().catch(() => null);
  await page.waitForTimeout(1500);
  const upcoming = await frame.locator('group, [role="listitem"]').evaluateAll(els =>
    els.map(e => e.textContent?.trim() || '').filter(t => /^\d\./.test(t)).slice(0, 10));
  return { published: upcoming.some(t => t.includes(titleSubstring)), upcoming };
}


// ─────────────────────────────────────────────────────────────────────────────
// Orchestrator — create assignment in one class
// ─────────────────────────────────────────────────────────────────────────────
async function createAssignment(page, opts) {
  // opts = { className, classId, title, instructions, rubric?, saveAsDraft = true }
  await navigateToAssignments(page, opts.className);
  await openNewAssignmentForm(page);
  await fillBasicFields(page, opts.title, opts.instructions);
  if (opts.rubric) await attachRubric(page, opts.rubric);
  if (opts.saveAsDraft !== false) await saveAsDraft(page);
  return await verifyDraft(page, opts.classId, opts.title);
}
