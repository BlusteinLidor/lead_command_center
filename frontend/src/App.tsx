import { useMemo, useState } from "react";
import type { Lead, LeadStage, UrgencyFilter } from "./types/lead";
import { useIncomingTicker, useLeads } from "./hooks/useLeads";
import { useI18n } from "./i18n/I18nProvider";
import { TopBar } from "./components/TopBar";
import type { IncomingIntervalSec } from "./components/IncomingSettings";
import { KpiStrip } from "./components/KpiStrip";
import { PipelineBoard } from "./components/PipelineBoard";
import { LeadDrawer } from "./components/LeadDrawer";
import {
  BoardSkeleton,
  EmptyState,
  ErrorBanner,
} from "./components/EmptyState";
import { formatChannel } from "./utils/format";

export default function App() {
  const { t, locale } = useI18n();
  const {
    leads,
    loading,
    error,
    updatingId,
    highlightId,
    load,
    changeStage,
    runReset,
    runSimulate,
    runIncoming,
  } = useLeads();

  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [urgencyFilter, setUrgencyFilter] = useState<UrgencyFilter>("all");
  const [channelFilter, setChannelFilter] = useState<string>("all");
  const [incomingIntervalSec, setIncomingIntervalSec] =
    useState<IncomingIntervalSec>(0);

  useIncomingTicker(incomingIntervalSec, runIncoming);

  const channels = useMemo(() => {
    const set = new Set<string>();
    for (const l of leads) {
      const key = (l.source || l.channel || "").toLowerCase();
      if (key) set.add(key);
    }
    return Array.from(set).sort();
  }, [leads]);

  const filtered = useMemo(() => {
    return leads.filter((l) => {
      if (urgencyFilter === "High" && l.urgency !== "High") return false;
      if (channelFilter !== "all") {
        const key = (l.source || l.channel || "").toLowerCase();
        if (key !== channelFilter) return false;
      }
      return true;
    });
  }, [leads, urgencyFilter, channelFilter]);

  const selectedLead: Lead | null =
    leads.find((l) => l.id === selectedId) ?? null;

  const handleSelect = (lead: Lead) => setSelectedId(lead.id);

  const handleStageChange = async (stage: LeadStage) => {
    if (!selectedLead) return;
    try {
      await changeStage(selectedLead.id, stage);
    } catch {
      /* error surfaced via useLeads */
    }
  };

  return (
    <div
      className="app-grain"
      style={{
        minHeight: "100vh",
        background: `
          radial-gradient(1200px 600px at 10% -10%, rgba(15, 92, 92, 0.12), transparent 55%),
          radial-gradient(900px 500px at 90% 0%, rgba(196, 120, 42, 0.1), transparent 50%),
          linear-gradient(165deg, var(--color-canvas) 0%, var(--color-canvas-deep) 100%)
        `,
      }}
    >
      <div
        className="app-shell mx-auto w-full max-w-[1440px]"
        style={{ padding: "var(--space-page)" }}
      >
        <TopBar
          incomingIntervalSec={incomingIntervalSec}
          onIncomingIntervalChange={setIncomingIntervalSec}
          onReset={runReset}
          onSimulate={runSimulate}
        />

        {error && !loading && (
          <ErrorBanner message={error} onRetry={() => void load()} />
        )}

        {!loading && leads.length > 0 && (
          <>
            <div style={{ marginBlockEnd: "1rem" }}>
              <KpiStrip leads={leads} />
            </div>

            <div
              className="mb-3 flex flex-wrap items-center gap-2"
              style={{ marginBlockEnd: "0.85rem" }}
            >
              <FilterChip
                active={urgencyFilter === "all"}
                onClick={() => setUrgencyFilter("all")}
                label={t("filterAll")}
              />
              <FilterChip
                active={urgencyFilter === "High"}
                onClick={() => setUrgencyFilter("High")}
                label={t("filterHigh")}
              />
              {channels.map((ch) => (
                <FilterChip
                  key={ch}
                  active={channelFilter === ch}
                  onClick={() =>
                    setChannelFilter((prev) => (prev === ch ? "all" : ch))
                  }
                  label={formatChannel(ch, null, locale)}
                />
              ))}
            </div>
          </>
        )}

        {loading ? (
          <BoardSkeleton />
        ) : leads.length === 0 ? (
          <EmptyState />
        ) : (
          <PipelineBoard
            leads={filtered}
            selectedId={selectedId}
            highlightId={highlightId}
            onSelect={handleSelect}
          />
        )}

        <LeadDrawer
          lead={selectedLead}
          open={selectedId !== null && !!selectedLead}
          updating={updatingId === selectedId}
          onClose={() => setSelectedId(null)}
          onStageChange={(stage) => void handleStageChange(stage)}
        />
      </div>
    </div>
  );
}

function FilterChip({
  active,
  onClick,
  label,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="rounded-full px-3 py-1 text-xs font-semibold transition-colors"
      style={{
        background: active ? "var(--color-primary)" : "var(--color-surface-solid)",
        color: active ? "#fff" : "var(--color-ink-muted)",
        border: `1px solid ${active ? "var(--color-primary)" : "var(--color-border)"}`,
        cursor: "pointer",
      }}
    >
      {label}
    </button>
  );
}
