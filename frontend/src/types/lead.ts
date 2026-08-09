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
