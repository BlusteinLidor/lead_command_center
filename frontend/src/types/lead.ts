export type LeadStage = "New" | "Contacted" | "Qualified" | "Closed";
export type Urgency = "Low" | "Med" | "High";

export const LEAD_STAGES: LeadStage[] = [
  "New",
  "Contacted",
  "Qualified",
  "Closed",
];

export interface Lead {
  id: number;
  created_at: string;
  source: string | null;
  channel: string | null;
  contact_name: string | null;
  contact_email: string | null;
  contact_phone: string | null;
  message_body: string;
  score: number;
  summary: string;
  urgency: Urgency | string;
  detected_intent: string;
  stage: LeadStage | string;
  /** Bilingual fields — UI locale selects EN or HE for display. */
  contact_name_en?: string | null;
  contact_name_he?: string | null;
  message_body_en?: string | null;
  message_body_he?: string | null;
  summary_en?: string | null;
  summary_he?: string | null;
  detected_intent_en?: string | null;
  detected_intent_he?: string | null;
}

export interface LeadWebhookPayload {
  message?: string;
  body?: string;
  source?: string;
  channel?: string;
  name?: string;
  email?: string;
  phone?: string;
}

export type UrgencyFilter = "all" | "High";
export type ChannelFilter = "all" | string;

/** Text fields that switch with EN/HE UI locale. */
export interface LocalizedLeadText {
  contact_name: string | null;
  message_body: string;
  summary: string;
  detected_intent: string;
}

function firstNonEmpty(
  ...values: Array<string | null | undefined>
): string | null {
  for (const v of values) {
    if (v != null && String(v).trim() !== "") return v;
  }
  return null;
}

export function localizeLeadText(
  lead: Lead,
  locale: "en" | "he",
): LocalizedLeadText {
  if (locale === "he") {
    return {
      contact_name: firstNonEmpty(
        lead.contact_name_he,
        lead.contact_name_en,
        lead.contact_name,
      ),
      message_body:
        firstNonEmpty(
          lead.message_body_he,
          lead.message_body_en,
          lead.message_body,
        ) ?? "",
      summary:
        firstNonEmpty(lead.summary_he, lead.summary_en, lead.summary) ?? "",
      detected_intent:
        firstNonEmpty(
          lead.detected_intent_he,
          lead.detected_intent_en,
          lead.detected_intent,
        ) ?? "",
    };
  }
  return {
    contact_name: firstNonEmpty(
      lead.contact_name_en,
      lead.contact_name_he,
      lead.contact_name,
    ),
    message_body:
      firstNonEmpty(
        lead.message_body_en,
        lead.message_body_he,
        lead.message_body,
      ) ?? "",
    summary:
      firstNonEmpty(lead.summary_en, lead.summary_he, lead.summary) ?? "",
    detected_intent:
      firstNonEmpty(
        lead.detected_intent_en,
        lead.detected_intent_he,
        lead.detected_intent,
      ) ?? "",
  };
}
