export function initials(name: string | null | undefined): string {
  if (!name?.trim()) return "?";
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

export function relativeTime(
  iso: string,
  _locale: "en" | "he",
  labels: {
    justNow: string;
    hoursAgo: (n: number) => string;
    daysAgo: (n: number) => string;
  },
): string {
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return "";
  const hours = Math.max(0, Math.floor((Date.now() - then) / 3_600_000));
  if (hours < 1) return labels.justNow;
  if (hours < 48) return labels.hoursAgo(hours);
  const days = Math.floor(hours / 24);
  return labels.daysAgo(days);
}

export function formatChannel(source: string | null, channel: string | null): string {
  const s = (source || channel || "inbound").toLowerCase();
  const map: Record<string, string> = {
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
  return map[s] ?? (source || channel || "—");
}
