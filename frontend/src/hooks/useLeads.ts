import { useCallback, useEffect, useState } from "react";
import {
  fetchLeads,
  resetDemo,
  simulateLead,
  updateLeadStage,
} from "../api/client";
import type { Lead, LeadStage, LeadWebhookPayload } from "../types/lead";

export function useLeads() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updatingId, setUpdatingId] = useState<number | null>(null);
  const [highlightId, setHighlightId] = useState<number | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchLeads();
      setLeads(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const changeStage = useCallback(async (id: number, stage: LeadStage) => {
    setUpdatingId(id);
    setError(null);
    try {
      const updated = await updateLeadStage(id, stage);
      setLeads((prev) =>
        prev.map((l) => (l.id === id ? updated : l)),
      );
      setHighlightId(id);
      window.setTimeout(() => setHighlightId(null), 1800);
      return updated;
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    } finally {
      setUpdatingId(null);
    }
  }, []);

  const runReset = useCallback(async () => {
    setError(null);
    try {
      await resetDemo();
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    }
  }, [load]);

  const runSimulate = useCallback(async (payload: LeadWebhookPayload) => {
    setError(null);
    try {
      const created = await simulateLead(payload);
      setLeads((prev) => [created, ...prev.filter((l) => l.id !== created.id)]);
      setHighlightId(created.id);
      window.setTimeout(() => setHighlightId(null), 2200);
      return created;
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    }
  }, []);

  return {
    leads,
    loading,
    error,
    setError,
    updatingId,
    highlightId,
    load,
    changeStage,
    runReset,
    runSimulate,
  };
}
