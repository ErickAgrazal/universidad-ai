// Playwright helpers for the grade-teams-lab skill.
// Pasted by the agent into `mcp__playwright__browser_run_code_unsafe`.
// Each export below is a self-contained async function — pick the one the
// current phase needs and inline it.


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 1 helper — Pick the oldest unreturned assignment in the current class
//
// Returns: { title, ref } | null
// Usage: navigate to class team → Assignments tab; then call this.
// ─────────────────────────────────────────────────────────────────────────────
async function autoPickNextAssignment(page) {
  const frame = page.locator('iframe').first().contentFrame();
  // Make sure Past due tab is selected
  await frame.getByRole('tab', { name: 'Past due' }).click().catch(() => null);
  await page.waitForTimeout(800);
  // Collect all assignment listitems in DOM order (Teams sorts oldest-first inside groups)
  const items = await frame.locator('listitem, [role="listitem"]').evaluateAll(els =>
    els.map(e => {
      const title = (e.querySelector('[role="heading"], h3, h4, .assignment-title') ||
                     e.querySelector('div'))?.textContent?.trim() || '';
      return { title };
    })
  );
  const candidates = items.filter(i => i.title && /^\d+\./.test(i.title));
  if (candidates.length === 0) return null;
  // Past due is newest-first, so the LAST candidate is the oldest
  return candidates[candidates.length - 1];
}


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 2.0 helper — Capture per-student GitHub URLs from Teams submissions
//
// For code-lab assignments (A5/A6/etc) the student pastes a GitHub URL into the
// Teams submission. Reading those URLs FIRST is more reliable than guessing the
// repo from `2026-1GS24X-<lastname>-<firstname>` heuristics — students often
// submit a separate project repo (e.g. PollClass-FSDSN) instead of the course
// repo (e.g. 2026-1GS241-Bazan-Cesar).
//
// Returns: [{ name: "LASTNAME, FIRSTNAME", urls: ["https://github.com/..."] }, ...]
//
// Usage: open the assignment's grade view first; this drives speed-grader
// navigation for each student via the "View and grade work of <name>" button.
//
// Caveats: brittle — Teams DOM changes often. If selectors break, the agent
// should fall back to per-student manual inspection. Slow (~2 s/student).
// ─────────────────────────────────────────────────────────────────────────────
async function captureSubmissionUrls(page, opts = {}) {
  const { limit, urlHostFilter = 'github.com' } = opts;
  const frame = page.locator('iframe').first().contentFrame();

  const scrollAll = (delta) => frame.locator('body').evaluate((_, d) => {
    const scrollables = Array.from(document.querySelectorAll('*')).filter(e => {
      const cs = getComputedStyle(e);
      return (cs.overflowY === 'auto' || cs.overflowY === 'scroll') && e.scrollHeight > e.clientHeight;
    });
    for (const s of scrollables) {
      if (d === 0) s.scrollTop = 0;
      else s.scrollTop += d;
    }
  }, delta);

  // Step 1 — enumerate every "View and grade work of <name>" button (one per
  // student), accounting for virtualization.
  await scrollAll(0);
  await page.waitForTimeout(400);
  const names = new Set();
  for (let i = 0; i < 20; i++) {
    const batch = await frame.locator('button[aria-label*="View and grade work of"]').evaluateAll(els =>
      els.map(e => {
        const al = e.getAttribute('aria-label') || '';
        const m = al.match(/View and grade work of\s+(.+?)\s*$/);
        return m ? m[1].trim() : null;
      }).filter(Boolean)
    );
    for (const n of batch) names.add(n);
    await scrollAll(300);
    await page.waitForTimeout(220);
  }
  const roster = [...names].sort();
  const targets = limit ? roster.slice(0, limit) : roster;

  // Step 2 — for each student, click into the speed-grader and harvest URLs.
  const out = [];
  for (const name of targets) {
    const btn = frame.locator(`button[aria-label="View and grade work of ${name}"]`).first();
    try {
      await btn.scrollIntoViewIfNeeded({ timeout: 3000 });
      await btn.click({ timeout: 5000 });
    } catch {
      out.push({ name, urls: [], error: 'click_failed' });
      continue;
    }
    await page.waitForTimeout(1300);  // speed-grader transition

    // URLs may live in: anchor hrefs, aria-labels (Teams sometimes encodes the
    // URL there), and resource-tile data attributes. Collect from all three.
    const urls = await frame.locator('body').evaluate((host) => {
      const found = new Set();
      // 1. plain anchors
      for (const a of document.querySelectorAll(`a[href*="${host}"]`)) {
        if (a.href) found.add(a.href);
      }
      // 2. aria-labels containing the host
      for (const el of document.querySelectorAll('[aria-label]')) {
        const al = el.getAttribute('aria-label') || '';
        const m = al.match(new RegExp(`https?://[^\\s)]*${host.replace('.', '\\.')}[^\\s)]*`));
        if (m) found.add(m[0]);
      }
      // 3. data-url / data-href on resource tiles
      for (const el of document.querySelectorAll('[data-url], [data-href]')) {
        const u = el.getAttribute('data-url') || el.getAttribute('data-href') || '';
        if (u.includes(host)) found.add(u);
      }
      return [...found];
    }, urlHostFilter);
    out.push({ name, urls });

    // Step 3 — back to the grade table for the next student.
    const back = frame.getByRole('button', { name: /^Back$|^Atrás$|^Volver$/i }).first();
    if (await back.isVisible().catch(() => false)) {
      await back.click().catch(() => null);
    } else {
      await page.keyboard.press('Escape').catch(() => null);
    }
    await page.waitForTimeout(700);
  }
  return out;
}


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 4.75 helper — Roster reconciliation against the grade map
//
// Input: { gradeMap: { "STUDENT_FOLDER_NAME": 90, ... } }
// Returns:
//   {
//     teams_roster: ["LASTNAME, FIRSTNAME", ...],
//     in_map_not_in_teams: [...],   // cross-class artifacts (silently skip in Phase 5)
//     in_teams_not_in_map: [...],   // ungraded but enrolled — surface to user
//     matched: [["LASTNAME, FIRSTNAME", folder_name, score], ...]
//   }
//
// Folder name = teams_to_folder.py output (LASTNAME_FIRSTNAME, accents stripped).
// ─────────────────────────────────────────────────────────────────────────────
async function reconcileRoster(page, gradeMap) {
  const frame = page.locator('iframe').first().contentFrame();
  // Enumerate every grade textbox with scroll loop (virtualization)
  await frame.locator('body').evaluate(() => {
    const ss = Array.from(document.querySelectorAll('*')).filter(e => {
      const cs = getComputedStyle(e);
      return (cs.overflowY === 'auto' || cs.overflowY === 'scroll') && e.scrollHeight > e.clientHeight;
    });
    for (const s of ss) s.scrollTop = 0;
  });
  await page.waitForTimeout(400);
  const teamsRoster = new Set();
  for (let i = 0; i < 15; i++) {
    const labels = await frame.locator('input[aria-label*="Grade, out of 100"]').evaluateAll(els =>
      els.map(e => e.getAttribute('aria-label').replace('Grade, out of 100 for ', ''))
    );
    for (const l of labels) teamsRoster.add(l);
    await frame.locator('body').evaluate(() => {
      const ss = Array.from(document.querySelectorAll('*')).filter(e => {
        const cs = getComputedStyle(e);
        return (cs.overflowY === 'auto' || cs.overflowY === 'scroll') && e.scrollHeight > e.clientHeight;
      });
      for (const s of ss) s.scrollTop += 300;
    });
    await page.waitForTimeout(250);
  }

  // Normalize teams roster → folder format (strip accents, replace ", " → "_", uppercase)
  const stripAccents = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '');
  const teamsToFolder = (label) => {
    // "LASTNAME, FIRSTNAME" → "LASTNAME_FIRSTNAME"; "CARLOS JAEN" → "CARLOS_JAEN"
    const cleaned = stripAccents(label.replace(/[.]$/, ''));
    return cleaned.replace(/,\s*/g, '_').replace(/\s+/g, '_').toUpperCase();
  };

  const folderToTeams = {};
  for (const label of teamsRoster) folderToTeams[teamsToFolder(label)] = label;

  const matched = [];
  const inMapNotInTeams = [];
  for (const [folder, score] of Object.entries(gradeMap)) {
    const key = folder.toUpperCase();
    if (folderToTeams[key]) {
      matched.push([folderToTeams[key], folder, score]);
    } else {
      inMapNotInTeams.push(folder);
    }
  }
  const matchedFolders = new Set(matched.map(m => m[1].toUpperCase()));
  const inTeamsNotInMap = [...teamsRoster].filter(l =>
    !matchedFolders.has(teamsToFolder(l))
  );

  return {
    teams_roster: [...teamsRoster].sort(),
    matched,
    in_map_not_in_teams: inMapNotInTeams,
    in_teams_not_in_map: inTeamsNotInMap,
  };
}


// ─────────────────────────────────────────────────────────────────────────────
// PHASE 5/5.5 — Audit log capture
//
// After Phase 5 (grade fills) and Phase 5.5 (feedbacks), capture what's actually
// in Teams for the offline audit log. Returns:
//   [{ name, score, has_feedback }, ...]
// Save this to submissions/<asignacion>/AUDIT.json with a timestamp.
// ─────────────────────────────────────────────────────────────────────────────
async function captureAuditSnapshot(page) {
  const frame = page.locator('iframe').first().contentFrame();
  await frame.locator('body').evaluate(() => {
    const ss = Array.from(document.querySelectorAll('*')).filter(e => {
      const cs = getComputedStyle(e);
      return (cs.overflowY === 'auto' || cs.overflowY === 'scroll') && e.scrollHeight > e.clientHeight;
    });
    for (const s of ss) s.scrollTop = 0;
  });
  await page.waitForTimeout(400);
  const seen = new Map();
  for (let i = 0; i < 15; i++) {
    const rows = await frame.locator('input[aria-label*="Grade, out of 100"]').evaluateAll(els =>
      els.map(e => {
        const label = e.getAttribute('aria-label').replace('Grade, out of 100 for ', '');
        // Find sibling feedback toggle within ~12 ancestors
        let n = e;
        let feedbackState = 'unknown';
        for (let d = 0; d < 15; d++) {
          n = n.parentElement;
          if (!n) break;
          const tog = n.querySelector('button[aria-label*="Toggle feedback for"]');
          if (tog) {
            const al = tog.getAttribute('aria-label') || '';
            feedbackState = al.includes('Feedback given') ? 'given' :
                            al.includes('Feedback not given') ? 'none' : 'unknown';
            break;
          }
        }
        return { name: label, score: e.value, has_feedback: feedbackState === 'given' };
      })
    );
    for (const r of rows) seen.set(r.name, r);
    await frame.locator('body').evaluate(() => {
      const ss = Array.from(document.querySelectorAll('*')).filter(e => {
        const cs = getComputedStyle(e);
        return (cs.overflowY === 'auto' || cs.overflowY === 'scroll') && e.scrollHeight > e.clientHeight;
      });
      for (const s of ss) s.scrollTop += 300;
    });
    await page.waitForTimeout(250);
  }
  return [...seen.values()];
}
