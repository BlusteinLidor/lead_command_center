# Portfolio handoff — lead-command-center

Use this file when wiring the case study on the main website
(`BlusteinLidor/port_website` → `lib/i18n/en.ts` / `lib/i18n/he.ts`).

The demo is a self-contained React SPA + FastAPI service (Docker on Render).
Board + triage work without OpenAI; the inbound AI simulator is optional.

## Pre-flight

| Check | Status |
|-------|--------|
| Intended live demo URL | https://lead-command-center.onrender.com |
| Current host status | Render free service is **suspended** — restore/redeploy before linking live |
| `GET /health` | `{ "status": "ok" }` |
| Seeded board | Fictional **Almond Family Clinic** / מרפאת שקד — no real PII |
| Auth | None (public demo, sample data only) |
| OpenAI | Optional. Kanban + stage changes work without it |
| Repo | https://github.com/BlusteinLidor/lead_command_center · branch `master` |

**Website work required:** paste case-study copy, set `href` to the live URL once Render is up, optional video poster. No backend or secret changes on the portfolio site.

**Do not ship the case-study CTA until the Render service is live.** First load on the free tier can take ~30–60s after idle sleep.

---

## Case study fields (paste)

Paste into the portfolio `lib/i18n/he.ts` / `lib/i18n/en.ts` `work.caseStudies`
(replace a placeholder study such as `automation-dashboard`).

`CaseStudy` shape on the site: `id`, `title`, `problem`, `solution`, `result`, `tech` (string), `href`, `hrefLabel`.

```text
id: lead-command-center
demoUrl: https://lead-command-center.onrender.com
title_en: Lead Command Center
title_he: מרכז פיקוד לידים
problem_en: Leads arrive scattered across WhatsApp, forms, and email — follow-ups get missed in spreadsheets.
problem_he: לידים מגיעים מפוזרים בוואטסאפ, טפסים ומייל — מעקב נופל בין גיליונות.
solution_en: One ops board that ingests leads, scores and summarizes with AI, and lets you triage by stage.
solution_he: לוח תפעול אחד שקולט לידים, מדרג ומסכם עם AI, ומאפשר לנהל שלב בצינור המכירות.
result_en: Single source of truth — hot leads are visible immediately and staged in under a minute.
result_he: מקור אמת אחד — לידים חמים נראים מיד ועוברים שלב בפחות מדקה.
tech: FastAPI, React, TypeScript, Vite, Tailwind CSS, SQLite, OpenAI
hrefLabel_en: Try it live
hrefLabel_he: נסו בשידור חי
videoUrl:
poster:
```

### Suggested EN object (matches `CaseStudy`)

```ts
{
  id: "lead-command-center",
  title: "Lead Command Center",
  problem:
    "Leads arrive scattered across WhatsApp, forms, and email — follow-ups get missed in spreadsheets.",
  solution:
    "One ops board that ingests leads, scores and summarizes with AI, and lets you triage by stage.",
  result:
    "Single source of truth — hot leads are visible immediately and staged in under a minute.",
  tech: "FastAPI, React, TypeScript, Vite, Tailwind CSS, SQLite, OpenAI",
  href: "https://lead-command-center.onrender.com",
  hrefLabel: "Try it live",
}
```

### Suggested HE object (matches `CaseStudy`)

```ts
{
  id: "lead-command-center",
  title: "מרכז פיקוד לידים",
  problem:
    "לידים מגיעים מפוזרים בוואטסאפ, טפסים ומייל — מעקב נופל בין גיליונות.",
  solution:
    "לוח תפעול אחד שקולט לידים, מדרג ומסכם עם AI, ומאפשר לנהל שלב בצינור המכירות.",
  result:
    "מקור אמת אחד — לידים חמים נראים מיד ועוברים שלב בפחות מדקה.",
  tech: "FastAPI, React, TypeScript, Vite, Tailwind CSS, SQLite, OpenAI",
  href: "https://lead-command-center.onrender.com",
  hrefLabel: "נסו בשידור חי",
}
```

---

## Integration notes for the website

1. **Link out** to the Render URL (new tab). Do **not** iframe the demo; the SPA already has full UI chrome (brand, language toggle, settings).
2. **CTA copy:** `Try it live` / `נסו בשידור חי` (or site-default “Live demo”).
3. **Cold start:** free Render sleeps after idle. Surrounding copy can say “live demo” — first paint may take up to a minute.
4. **Language:** EN/HE toggle with full RTL in Hebrew. Default locale is English unless the visitor previously chose Hebrew (`localStorage` key `lcc-locale`).
5. **Do not** put `OPENAI_API_KEY` in the website repo; the demo owns that secret on Render (optional — board works without it).
6. **Video (optional):** record the visitor path below. Seed theme is a fictional clinic, not a real client.

---

## Ops (demo only — not the website)

| Item | Detail |
|------|--------|
| Deploy | Render Blueprint from [`render.yaml`](render.yaml) · Docker · healthcheck `GET /health` |
| Service name | `lead-command-center` |
| Secret | Optional `OPENAI_API_KEY` for **Demo tools → Simulate inbound lead with AI** |
| Data | SQLite is ephemeral on free hosts — re-seeds on cold start |
| Reset | UI **Settings → Reset demo data** (`POST /demo/reset`) |
| Live inbound (no AI) | Settings → incoming frequency, or `POST /demo/incoming` |
| Stack docs | [DEMO.md](DEMO.md) · [README.md](README.md) |

---

## Quick visitor path (for QA or video, &lt;60s)

1. Open the live URL — seeded clinic leads appear immediately.
2. Read brand **Lead Command Center** / **מרכז פיקוד לידים** and clinic **Almond Family Clinic** / **מרפאת שקד**.
3. Spot **High urgency** KPI and open a hot lead card.
4. In the drawer, change **stage** (e.g. New → Contacted / Qualified).
5. Confirm the Kanban column and KPIs update.
6. Optional: EN/HE language toggle (full RTL in Hebrew).
7. Optional: Settings (gear) → incoming frequency (default **Never**); new cards appear live in **New**.
8. Optional: Settings → Reset demo data.
9. Optional: Settings → Simulate inbound lead with AI (needs `OPENAI_API_KEY` on the host).
