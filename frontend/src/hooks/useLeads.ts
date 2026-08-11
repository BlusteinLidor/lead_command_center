import { useCallback, useEffect, useRef, useState } from "react";
import {
  fetchLeads,
  pushIncomingLead,
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
  const [toastLead, setToastLead] = useState<Lead | null>(null);
  const highlightTimerRef = useRef<number | null>(null);
  const toastTimerRef = useRef<number | null>(null);

  const flashHighlight = useCallback((id: number, ms = 2200) => {
    if (highlightTimerRef.current != null) {
      window.clearTimeout(highlightTimerRef.current);
    }
    setHighlightId(id);
    highlightTimerRef.current = window.setTimeout(() => {
      setHighlightId((cur) => (cur === id ? null : cur));
      highlightTimerRef.current = null;
    }, ms);
  }, []);

  const dismissToast = useCallback(() => {
    if (toastTimerRef.current != null) {
      window.clearTimeout(toastTimerRef.current);
      toastTimerRef.current = null;
    }
    setToastLead(null);
  }, []);

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
      flashHighlight(id, 1800);
      return updated;
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    } finally {
      setUpdatingId(null);
    }
  }, [flashHighlight]);

  const runReset = useCallback(async () => {
    setError(null);
    dismissToast();
    try {
      await resetDemo();
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    }
  }, [load, dismissToast]);

  const prependLead = useCallback(
    (created: Lead) => {
      setLeads((prev) => [created, ...prev.filter((l) => l.id !== created.id)]);
      flashHighlight(created.id, 2200);
      setToastLead(created);
      if (toastTimerRef.current != null) {
        window.clearTimeout(toastTimerRef.current);
      }
      // Long enough to catch on video; short enough not to clutter the board.
      toastTimerRef.current = window.setTimeout(() => {
        setToastLead((cur) => (cur?.id === created.id ? null : cur));
        toastTimerRef.current = null;
      }, 5600);
    },
    [flashHighlight],
  );

  const runSimulate = useCallback(
    async (payload: LeadWebhookPayload) => {
      setError(null);
      try {
        const created = await simulateLead(payload);
        prependLead(created);
        return created;
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e));
        throw e;
      }
    },
    [prependLead],
  );

  const runIncoming = useCallback(async () => {
    setError(null);
    try {
      const created = await pushIncomingLead();
      prependLead(created);
      return created;
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    }
  }, [prependLead]);

  return {
    leads,
    loading,
    error,
    setError,
    updatingId,
    highlightId,
    toastLead,
    flashHighlight,
    dismissToast,
    load,
    changeStage,
    runReset,
    runSimulate,
    runIncoming,
  };
}

/** Fire `onTick` on an interval; `0` disables. First tick soon after enable, then every N s. */
export function useIncomingTicker(
  intervalSec: number,
  onTick: () => Promise<unknown>,
) {
  const onTickRef = useRef(onTick);
  onTickRef.current = onTick;
  const busyRef = useRef(false);

  useEffect(() => {
    if (!intervalSec || intervalSec <= 0) return;
    const ms = intervalSec * 1000;
    // First lead arrives soon so recording does not wait a full period.
    const firstMs = Math.min(2500, ms);

    const run = () => {
      if (busyRef.current) return;
      busyRef.current = true;
      void onTickRef
        .current()
        .catch(() => {
          /* error surfaced by useLeads */
        })
        .finally(() => {
          busyRef.current = false;
        });
    };

    let intervalId: number | undefined;
    const firstId = window.setTimeout(() => {
      run();
      intervalId = window.setInterval(run, ms);
    }, firstMs);

    return () => {
      window.clearTimeout(firstId);
      if (intervalId !== undefined) window.clearInterval(intervalId);
    };
  }, [intervalSec]);
}
