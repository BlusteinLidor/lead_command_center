import type { Lead, LeadStage, LeadWebhookPayload } from "../types/lead";

/**
 * Dev: Vite proxies `/api/*` → FastAPI.
 * Prod: same-origin paths when FastAPI serves the SPA (empty base).
 */
const API_BASE =
  import.meta.env.VITE_API_BASE ??
  (import.meta.env.DEV ? "/api" : "");

async function parseError(res: Response): Promise<string> {
  try {
    const data = (await res.json()) as { detail?: string | unknown };
    if (typeof data.detail === "string") return data.detail;
    return JSON.stringify(data.detail ?? data);
  } catch {
    return res.statusText || `HTTP ${res.status}`;
  }
}

export async function fetchLeads(): Promise<Lead[]> {
  const res = await fetch(`${API_BASE}/leads`);
  if (!res.ok) throw new Error(await parseError(res));
  return res.json() as Promise<Lead[]>;
}

export async function updateLeadStage(
  id: number,
  stage: LeadStage,
): Promise<Lead> {
  const res = await fetch(`${API_BASE}/leads/${id}/stage`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ stage }),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json() as Promise<Lead>;
}

export async function simulateLead(
  payload: LeadWebhookPayload,
): Promise<Lead> {
  const res = await fetch(`${API_BASE}/webhook/lead`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json() as Promise<Lead>;
}

export async function resetDemo(): Promise<{ ok: boolean; seeded: number }> {
  const res = await fetch(`${API_BASE}/demo/reset`, { method: "POST" });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json() as Promise<{ ok: boolean; seeded: number }>;
}

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/health`);
    return res.ok;
  } catch {
    return false;
  }
}
