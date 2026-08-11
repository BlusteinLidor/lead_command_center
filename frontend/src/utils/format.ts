export function initials(name: string | null | undefined): string {
  if (!name?.trim()) return "?";
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

/**
 * Parse API timestamps. SQLite-backed values may omit timezone; those are UTC.
 * Without this, browsers treat naive ISO as local and skew by the local offset
 * (e.g. Israel UTC+3 → looks ~3 hours old right after create).
 */
export function parseApiDate(iso: string): number {
  const raw = (iso || "").trim();
  if (!raw) return NaN;
  const hasZone = /[zZ]$|[+-]\d{2}:?\d{2}$/.test(raw);
  const normalized = hasZone
    ? raw
    : raw.includes("T")
      ? `${raw}Z`
      : `${raw.replace(" ", "T")}Z`;
  return new Date(normalized).getTime();
}

export function relativeTime(
  iso: string,
  _locale: "en" | "he",
  labels: {
    justNow: string;
    minutesAgo: (n: number) => string;
    hoursAgo: (n: number) => string;
    daysAgo: (n: number) => string;
  },
): string {
  const then = parseApiDate(iso);
  if (Number.isNaN(then)) return "";
  // Clamp future skew (clock drift) to "just now"
  const diffMs = Math.max(0, Date.now() - then);
  const seconds = Math.floor(diffMs / 1000);
  if (seconds < 45) return labels.justNow;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return labels.minutesAgo(minutes);
  const hours = Math.floor(minutes / 60);
  if (hours < 48) return labels.hoursAgo(hours);
  const days = Math.floor(hours / 24);
  return labels.daysAgo(days);
}

const CHANNEL_EN: Record<string, string> = {
  whatsapp: "WhatsApp",
  webform: "Web",
  facebook: "Facebook",
  phone: "Phone",
  email: "Email",
  instagram: "Instagram",
  chat: "Chat",
  contact: "Form",
  lead_ad: "Ad",
  callback_request: "Callback",
  inbound: "Inbound",
  reply: "Reply",
  dm: "DM",
  front_desk: "Desk",
};

const CHANNEL_HE: Record<string, string> = {
  whatsapp: "וואטסאפ",
  webform: "אתר",
  facebook: "פייסבוק",
  phone: "טלפון",
  email: "אימייל",
  instagram: "אינסטגרם",
  chat: "צ'אט",
  contact: "טופס",
  lead_ad: "מודעה",
  callback_request: "חזרה",
  inbound: "נכנס",
  reply: "תשובה",
  dm: "הודעה",
  front_desk: "קבלה",
};

export function formatChannel(
  source: string | null,
  channel: string | null,
  locale: "en" | "he" = "en",
): string {
  const s = (source || channel || "inbound").toLowerCase();
  const map = locale === "he" ? CHANNEL_HE : CHANNEL_EN;
  return map[s] ?? (source || channel || "—");
}
