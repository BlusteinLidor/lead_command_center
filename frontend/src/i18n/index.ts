export type Locale = "en" | "he";

export type TranslationKey = keyof typeof en;

const en = {
  brand: "Lead Command Center",
  clinic: "Almond Family Clinic",
  demoChip: "Demo · sample data",
  kpiTotal: "Total leads",
  kpiHigh: "High urgency",
  kpiAvgScore: "Avg score",
  kpiNew: "New",
  filterAll: "All",
  filterHigh: "High urgency",
  stageNew: "New",
  stageContacted: "Contacted",
  stageQualified: "Qualified",
  stageClosed: "Closed",
  emptyColumn: "No leads",
  emptyBoard: "No leads yet",
  emptyBoardHint: "Reset demo data to restore the sample set.",
  loading: "Loading leads…",
  errorTitle: "Could not load leads",
  errorHint: "Start the API: uvicorn main:app --reload --port 8000",
  retry: "Retry",
  drawerClose: "Close",
  contact: "Contact",
  message: "Message",
  aiSummary: "AI summary",
  intent: "Intent",
  source: "Source",
  channel: "Channel",
  stage: "Stage",
  moveTo: "Move to stage",
  updating: "Updating…",
  score: "Score",
  urgency: "Urgency",
  urgencyHigh: "High",
  urgencyMed: "Med",
  urgencyLow: "Low",
  demoTitle: "Demo console",
  demoOpen: "Demo tools",
  demoClose: "Hide demo tools",
  resetTitle: "Reset demo data",
  resetDesc: "Wipe all leads and restore the clinic sample set.",
  resetConfirm: "Reset now",
  resetBusy: "Resetting…",
  simulateTitle: "Simulate inbound lead",
  simulateDesc:
    "Posts to the webhook and runs AI scoring. Requires OPENAI_API_KEY on the API.",
  simulateLang: "Scenario language",
  simulatePick: "Scenario",
  simulateSend: "Send test lead",
  simulateBusy: "Analyzing with AI…",
  simulateSuccess: "Lead added to New",
  settingsOpen: "Settings",
  settingsTitle: "Demo settings",
  settingsDone: "Done",
  incomingFrequency: "Incoming leads",
  incomingDesc:
    "Auto-add a new fictional lead on a timer so viewers see live intake while you record.",
  incomingNever: "Never",
  incomingEvery: "Every {n}s",
  noName: "Unknown contact",
  justNow: "Just now",
  hoursAgo: "{n}h ago",
  daysAgo: "{n}d ago",
  email: "Email",
  phone: "Phone",
  noEmail: "—",
  noPhone: "—",
} as const;

const he: Record<TranslationKey, string> = {
  brand: "מרכז פיקוד לידים",
  clinic: "מרפאת שקד",
  demoChip: "דמו · נתוני דוגמה",
  kpiTotal: "סה״כ לידים",
  kpiHigh: "דחיפות גבוהה",
  kpiAvgScore: "ציון ממוצע",
  kpiNew: "חדש",
  filterAll: "הכל",
  filterHigh: "דחיפות גבוהה",
  stageNew: "חדש",
  stageContacted: "נוצר קשר",
  stageQualified: "מוכשר",
  stageClosed: "סגור",
  emptyColumn: "אין לידים",
  emptyBoard: "אין לידים עדיין",
  emptyBoardHint: "אפס נתוני דמו כדי לשחזר את סט הדוגמה.",
  loading: "טוען לידים…",
  errorTitle: "לא ניתן לטעון לידים",
  errorHint: "הפעל את ה-API: uvicorn main:app --reload --port 8000",
  retry: "נסה שוב",
  drawerClose: "סגור",
  contact: "איש קשר",
  message: "הודעה",
  aiSummary: "סיכום AI",
  intent: "כוונה",
  source: "מקור",
  channel: "ערוץ",
  stage: "שלב",
  moveTo: "העבר לשלב",
  updating: "מעדכן…",
  score: "ציון",
  urgency: "דחיפות",
  urgencyHigh: "גבוהה",
  urgencyMed: "בינונית",
  urgencyLow: "נמוכה",
  demoTitle: "קונסולת דמו",
  demoOpen: "כלי דמו",
  demoClose: "הסתר כלי דמו",
  resetTitle: "איפוס נתוני דמו",
  resetDesc: "מחק את כל הלידים ושחזר את סט הדוגמה של המרפאה.",
  resetConfirm: "אפס עכשיו",
  resetBusy: "מאפס…",
  simulateTitle: "סימולציית ליד נכנס",
  simulateDesc:
    "שולח לוובהוק ומריץ ניקוד AI. דורש OPENAI_API_KEY בשרת.",
  simulateLang: "שפת התסריט",
  simulatePick: "תסריט",
  simulateSend: "שלח ליד בדיקה",
  simulateBusy: "מנתח עם AI…",
  simulateSuccess: "הליד נוסף לחדש",
  settingsOpen: "הגדרות",
  settingsTitle: "הגדרות דמו",
  settingsDone: "סיום",
  incomingFrequency: "לידים נכנסים",
  incomingDesc:
    "הוספת ליד בדיוני אוטומטית לפי טיימר — כדי שהצופים יראו קליטה חיה בצילום.",
  incomingNever: "לעולם לא",
  incomingEvery: "כל {n} שנ׳",
  noName: "איש קשר לא ידוע",
  justNow: "עכשיו",
  hoursAgo: "לפני {n} שע׳",
  daysAgo: "לפני {n} ימים",
  email: "אימייל",
  phone: "טלפון",
  noEmail: "—",
  noPhone: "—",
};

export const translations = { en, he } as const;

export function t(
  locale: Locale,
  key: TranslationKey,
  vars?: Record<string, string | number>,
): string {
  let s: string = translations[locale][key] ?? translations.en[key];
  if (vars) {
    for (const [k, v] of Object.entries(vars)) {
      s = s.replace(`{${k}}`, String(v));
    }
  }
  return s;
}

export function stageLabel(locale: Locale, stage: string): string {
  switch (stage) {
    case "New":
      return t(locale, "stageNew");
    case "Contacted":
      return t(locale, "stageContacted");
    case "Qualified":
      return t(locale, "stageQualified");
    case "Closed":
      return t(locale, "stageClosed");
    default:
      return stage;
  }
}

export function urgencyLabel(locale: Locale, urgency: string): string {
  switch (urgency) {
    case "High":
      return t(locale, "urgencyHigh");
    case "Med":
      return t(locale, "urgencyMed");
    case "Low":
      return t(locale, "urgencyLow");
    default:
      return urgency;
  }
}
