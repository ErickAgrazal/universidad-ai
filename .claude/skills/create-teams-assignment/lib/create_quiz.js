// Reusable Playwright snippets for creating a Microsoft Forms quiz inside a Teams classroom assignment.
// The Forms quiz MUST be opened from Teams' Create→New quiz→Add quiz flow so it associates with the class.
// Opening forms.office.com directly creates an orphan quiz that cannot be reattached.

// ─────────────────────────────────────────────────────────────────────────────
// STEP 0 — Critical insight: collapsed-question editor
// ─────────────────────────────────────────────────────────────────────────────
// Only the currently focused/expanded question shows option textboxes & points input.
// Other questions render as compact buttons (`button[aria-label^="N. Question title ..."]`).
// → All option/correct/points selectors are LOCAL to the focused question.
// → To re-edit a past question, click `button[aria-label^="${n}. Question title"]` first.


// ─────────────────────────────────────────────────────────────────────────────
// STEP 1 — Open associated Forms quiz from Teams assignment
// ─────────────────────────────────────────────────────────────────────────────
async function openAssociatedQuiz(page, className) {
  await page.goto('https://teams.microsoft.com/v2/');
  await page.waitForTimeout(4000);
  await page.getByRole('button', { name: /Teams/ }).first().click().catch(() => null);
  await page.waitForTimeout(2000);
  await page.getByText(className).first().click();
  await page.waitForTimeout(3000);
  await page.getByRole('treeitem', { name: 'Assignments' }).click();
  await page.waitForTimeout(4000);

  const teamsFrame = page.locator('iframe').first().contentFrame();
  await teamsFrame.getByRole('button', { name: 'Create' }).click();
  await page.waitForTimeout(1500);
  await teamsFrame.locator('[role="menuitem"]').filter({ hasText: /quiz/i }).click();
  await page.waitForTimeout(5000);
  // Click "Add quiz" to create a NEW associated quiz (not pick existing)
  await teamsFrame.getByRole('button', { name: 'Add quiz' }).click();
  await page.waitForTimeout(7000);
  // Forms is now in a nested frame; URL contains assignmentsnewquiz=True
}


// ─────────────────────────────────────────────────────────────────────────────
// STEP 2 — Initial setup: close Copilot panel + set title
// ─────────────────────────────────────────────────────────────────────────────
async function initQuizTitle(page, title) {
  const formsFrame = page.frames().find(f => f.url().includes('forms.office.com'));
  // Close the "Draft with Copilot" panel if shown (avoids AI auto-generation)
  await formsFrame.locator('button[aria-label="Close"]').click().catch(() => null);
  await page.waitForTimeout(2000);
  // Click on the description placeholder to focus the form (reveals the title editor)
  await formsFrame.getByText('Add a subtitle or description').click({ force: true }).catch(() => null);
  await page.waitForTimeout(1500);
  const titleEl = formsFrame.locator('div[aria-label="Form title"][contenteditable="true"]');
  await titleEl.click();
  await page.waitForTimeout(400);
  await page.keyboard.press('ControlOrMeta+A');
  await page.waitForTimeout(80);
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(80);
  await page.keyboard.type(title, { delay: 5 });
  await page.waitForTimeout(600);
}


// ─────────────────────────────────────────────────────────────────────────────
// STEP 3 — Add first question via "Quick start with"
// ─────────────────────────────────────────────────────────────────────────────
async function addFirstQuestion(page, type = 'Choice') {
  const formsFrame = page.frames().find(f => f.url().includes('forms.office.com'));
  await formsFrame.locator('button[aria-label="Quick start with"]').click();
  await page.waitForTimeout(1500);
  await formsFrame.locator(`button[aria-label="${type}"]`).click();
  await page.waitForTimeout(3000);
  // Cancel any auto-Copilot review that might appear
  await formsFrame.locator('button[aria-label="Stop"]').click().catch(() => null);
  await page.waitForTimeout(800);
}


// ─────────────────────────────────────────────────────────────────────────────
// STEP 4 — Helper: clear contenteditable and type fresh text
// ─────────────────────────────────────────────────────────────────────────────
async function clearAndType(page, el, text) {
  await el.click();
  await page.waitForTimeout(180);
  await page.keyboard.press('ControlOrMeta+A');
  await page.waitForTimeout(80);
  await page.keyboard.press('Backspace');
  await page.waitForTimeout(80);
  await page.keyboard.type(text, { delay: 1 });
  await page.waitForTimeout(220);
}


// ─────────────────────────────────────────────────────────────────────────────
// STEP 5 — Fill a multiple-choice question (the current/focused one)
//
// q = { q: "title", options: [...], correct: [idx,...], multi: bool }
// pointsValue = "3" (string)
// ─────────────────────────────────────────────────────────────────────────────
async function fillCurrentMCQuestion(page, qNum, q, pointsValue = '3') {
  const formsFrame = page.frames().find(f => f.url().includes('forms.office.com'));

  // Title — aria includes "Question title N Input your question title here"
  const qTitle = formsFrame.locator(`div[role="textbox"][aria-label^="Question title ${qNum}"]`);
  await clearAndType(page, qTitle, q.q);

  // Toggle Multiple answers BEFORE filling options/correct (switches the correct UI mode)
  if (q.multi) {
    await formsFrame.locator('[role="switch"][aria-label="Multiple answers"]').click();
    await page.waitForTimeout(400);
  }

  // Add option count: Forms starts with 2 placeholder options. Add more as needed.
  for (let i = 2; i < q.options.length; i++) {
    await formsFrame.locator('button[aria-label="Add option"]').click();
    await page.waitForTimeout(500);
  }

  // Fill options. ONLY the focused question's options are visible — use local indices.
  // GOTCHA: After "Add option", the new option's textbox is pre-filled with "Option N" — must clear before typing.
  const opts = formsFrame.locator('div[role="textbox"][aria-label^="Choice Option Text"]');
  for (let i = 0; i < q.options.length; i++) {
    await clearAndType(page, opts.nth(i), q.options[i]);
  }

  // Mark correct answer(s). Correct buttons are also local to current question.
  const correctBtns = formsFrame.locator('button[aria-label="Correct answer"]');
  for (const ci of q.correct) {
    await correctBtns.nth(ci).click();
    await page.waitForTimeout(250);
  }

  // Points — input is local to current question (one visible at a time)
  const pointsInput = formsFrame.locator('input[aria-label="Points"]');
  await pointsInput.click({ clickCount: 3 });
  await page.waitForTimeout(120);
  await page.keyboard.type(pointsValue);
  await page.waitForTimeout(300);
}


// ─────────────────────────────────────────────────────────────────────────────
// STEP 6 — Fill a Text (long-answer) development question
// ─────────────────────────────────────────────────────────────────────────────
async function fillCurrentTextQuestion(page, qNum, q, pointsValue = '10') {
  const formsFrame = page.frames().find(f => f.url().includes('forms.office.com'));
  const qTitle = formsFrame.locator(`div[role="textbox"][aria-label^="Question title ${qNum}"]`);
  await clearAndType(page, qTitle, q.q);
  // Toggle Long answer if available (multi-line)
  const longAnswerSwitch = formsFrame.locator('[role="switch"][aria-label="Long answer"]');
  if (await longAnswerSwitch.count() > 0) {
    await longAnswerSwitch.click();
    await page.waitForTimeout(400);
  }
  const pointsInput = formsFrame.locator('input[aria-label="Points"]');
  await pointsInput.click({ clickCount: 3 });
  await page.waitForTimeout(120);
  await page.keyboard.type(pointsValue);
  await page.waitForTimeout(300);
}


// ─────────────────────────────────────────────────────────────────────────────
// STEP 7 — Add a new question (Choice or Text) — opens type picker each time
// ─────────────────────────────────────────────────────────────────────────────
async function addNewQuestion(page, type = 'Choice') {
  const formsFrame = page.frames().find(f => f.url().includes('forms.office.com'));
  await formsFrame.locator('button[aria-label="Add new question"]').click();
  await page.waitForTimeout(1200);
  await formsFrame.locator(`button[aria-label="${type}"]`).click();
  await page.waitForTimeout(2200);
}


// ─────────────────────────────────────────────────────────────────────────────
// STEP 8 — Set quiz duration via Settings panel
// ─────────────────────────────────────────────────────────────────────────────
async function setQuizDuration(page, minutes) {
  const formsFrame = page.frames().find(f => f.url().includes('forms.office.com'));
  await formsFrame.locator('button[aria-label="Settings"]').click();
  await page.waitForTimeout(2000);
  await formsFrame.getByText('Set time duration').click();
  await page.waitForTimeout(1500);
  const durInput = formsFrame.locator('input[aria-label^="Set time duration"]');
  await durInput.click({ clickCount: 3 });
  await page.waitForTimeout(150);
  await page.keyboard.type(String(minutes));
  await page.waitForTimeout(400);
  await page.keyboard.press('Tab');
  await page.waitForTimeout(500);
  await formsFrame.locator('button[aria-label="Settings Close"]').click().catch(() => null);
  await page.waitForTimeout(1500);
}


// ─────────────────────────────────────────────────────────────────────────────
// STEP 9 — Return to Teams: click "Done" → assignment editor opens
// ─────────────────────────────────────────────────────────────────────────────
async function returnToAssignmentEditor(page) {
  const teamsFrame = page.locator('iframe').first().contentFrame();
  await teamsFrame.getByRole('button', { name: 'Done' }).click();
  await page.waitForTimeout(7000);
  // Now you're on the assignment editor with the quiz auto-attached.
  // Title field is pre-filled with the quiz title — overwrite as needed.
}


// ─────────────────────────────────────────────────────────────────────────────
// STEP 10 — Schedule the assignment in the future
// ─────────────────────────────────────────────────────────────────────────────
async function scheduleAssignment(page, opts) {
  // opts = { day: 20, month: "May", year: 2026, postTime: "8:00 PM", dueTime: "8:30 PM" }
  const teamsFrame = page.locator('iframe').first().contentFrame();
  await teamsFrame.locator('button[aria-label="Edit assignment timeline"]').click();
  await page.waitForTimeout(2500);
  // Enable schedule switch (input role=switch, may show value="on" already but field disabled — click to truly enable)
  await teamsFrame.locator('input[aria-label="Schedule the assignment in the future"]').click({ force: true });
  await page.waitForTimeout(1000);

  const dayAria = `${opts.day}, ${opts.month}, ${opts.year}`;
  // Assign date
  await teamsFrame.locator('input[aria-label="Select an assign date"]').click();
  await page.waitForTimeout(1500);
  await teamsFrame.locator(`button[aria-label="${dayAria}"]`).click();
  await page.waitForTimeout(800);
  // Post time
  const postTime = teamsFrame.locator('input[aria-label="Post time"]');
  await postTime.click({ clickCount: 3 });
  await page.waitForTimeout(150);
  await page.keyboard.type(opts.postTime);
  await page.waitForTimeout(400);
  await page.keyboard.press('Tab');
  await page.waitForTimeout(500);
  // Due date — use data-test selector to avoid strict-mode collision with outer due-date
  await teamsFrame.locator('[data-test="timeline-due-date"]').click();
  await page.waitForTimeout(1500);
  await teamsFrame.locator(`button[aria-label="${dayAria}"]`).click();
  await page.waitForTimeout(800);
  // Due time — same precaution
  await teamsFrame.locator('[data-test="timeline-due-time"]').click({ clickCount: 3 });
  await page.waitForTimeout(150);
  await page.keyboard.type(opts.dueTime);
  await page.waitForTimeout(400);
  await page.keyboard.press('Tab');
  await page.waitForTimeout(500);
  // Close timeline dialog
  await teamsFrame.locator('button[aria-label="Done. Go back to the assignment editor"]').click();
  await page.waitForTimeout(2500);
}


// ─────────────────────────────────────────────────────────────────────────────
// STEP 11 — Publish (when post date is future, button label is "Schedule" not "Assign")
// ─────────────────────────────────────────────────────────────────────────────
async function publishScheduledAssignment(page) {
  const teamsFrame = page.locator('iframe').first().contentFrame();
  const schedBtn = teamsFrame.locator('button').filter({ hasText: /^Schedule$/ });
  const cnt = await schedBtn.count();
  for (let i = 0; i < cnt; i++) {
    if (await schedBtn.nth(i).isVisible().catch(() => false)) {
      await schedBtn.nth(i).scrollIntoViewIfNeeded({ timeout: 5000 });
      await page.waitForTimeout(500);
      await schedBtn.nth(i).click({ force: true });
      await page.waitForTimeout(8000);
      break;
    }
  }
}


// ─────────────────────────────────────────────────────────────────────────────
// ORCHESTRATOR — full flow for one class
// ─────────────────────────────────────────────────────────────────────────────
async function createQuizAssignment(page, quizData, scheduleOpts) {
  // quizData = { className, title, mc: [...], dev: [...], duration }
  // scheduleOpts = { day, month, year, postTime, dueTime }
  await openAssociatedQuiz(page, quizData.className);
  await initQuizTitle(page, quizData.title);
  // First question
  await addFirstQuestion(page, 'Choice');
  await fillCurrentMCQuestion(page, 1, quizData.mc[0], '3');
  // Remaining MC
  for (let i = 1; i < quizData.mc.length; i++) {
    await addNewQuestion(page, 'Choice');
    await fillCurrentMCQuestion(page, i + 1, quizData.mc[i], '3');
  }
  // Dev questions
  const offset = quizData.mc.length;
  for (let i = 0; i < quizData.dev.length; i++) {
    await addNewQuestion(page, 'Text');
    await fillCurrentTextQuestion(page, offset + i + 1, quizData.dev[i], '10');
  }
  await setQuizDuration(page, quizData.duration);
  await returnToAssignmentEditor(page);
  await scheduleAssignment(page, scheduleOpts);
  await publishScheduledAssignment(page);
}

// EXPORTS (when used as a module)
// module.exports = { createQuizAssignment, ... };
