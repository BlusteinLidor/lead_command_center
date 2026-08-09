import { LayoutGroup } from "motion/react";
import type { Lead } from "../types/lead";
import { LEAD_STAGES } from "../types/lead";
import { useI18n } from "../i18n/I18nProvider";
import { stageLabel } from "../i18n";
import { LeadCard } from "./LeadCard";

interface PipelineBoardProps {
  leads: Lead[];
  selectedId: number | null;
  highlightId: number | null;
  onSelect: (lead: Lead) => void;
}

export function PipelineBoard({
  leads,
  selectedId,
  highlightId,
  onSelect,
}: PipelineBoardProps) {
  const { t, locale } = useI18n();

  return (
    <LayoutGroup>
      <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-4">
        {LEAD_STAGES.map((stage) => {
          const columnLeads = leads
            .filter((l) => l.stage === stage)
            .sort((a, b) => {
              const urg = (u: string) =>
                u === "High" ? 0 : u === "Med" ? 1 : 2;
              const u = urg(a.urgency) - urg(b.urgency);
              if (u !== 0) return u;
              return b.score - a.score;
            });

          return (
            <section
              key={stage}
              className="flex min-h-[280px] flex-col rounded-[var(--radius-xl)]"
              style={{
                background: "rgba(255, 251, 246, 0.45)",
                border: "1px solid var(--color-border)",
              }}
            >
              <div
                className="flex items-center justify-between gap-2 px-3 py-3"
                style={{ borderBottom: "1px solid var(--color-border)" }}
              >
                <h2
                  className="m-0 text-sm font-semibold"
                  style={{ color: "var(--color-ink)" }}
                >
                  {stageLabel(locale, stage)}
                </h2>
                <span
                  className="inline-flex h-6 min-w-6 items-center justify-center rounded-full px-1.5 text-xs font-semibold tabular-nums"
                  style={{
                    background: "var(--color-primary-soft)",
                    color: "var(--color-primary)",
                  }}
                >
                  {columnLeads.length}
                </span>
              </div>
              <div className="flex flex-1 flex-col gap-2.5 overflow-y-auto p-2.5">
                {columnLeads.length === 0 ? (
                  <p
                    className="m-0 px-1 py-6 text-center text-xs"
                    style={{ color: "var(--color-ink-faint)" }}
                  >
                    {t("emptyColumn")}
                  </p>
                ) : (
                  columnLeads.map((lead) => (
                    <LeadCard
                      key={lead.id}
                      lead={lead}
                      selected={selectedId === lead.id}
                      highlight={highlightId === lead.id}
                      onClick={() => onSelect(lead)}
                    />
                  ))
                )}
              </div>
            </section>
          );
        })}
      </div>
    </LayoutGroup>
  );
}
