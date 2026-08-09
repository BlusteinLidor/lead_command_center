import type { Lead } from "../types/lead";
import { useI18n } from "../i18n/I18nProvider";

interface KpiStripProps {
  leads: Lead[];
}

function KpiCard({
  label,
  value,
  accent,
}: {
  label: string;
  value: string | number;
  accent?: boolean;
}) {
  return (
    <div
      className="min-w-0 flex-1 rounded-[var(--radius-lg)] px-4 py-3"
      style={{
        background: "var(--color-surface)",
        border: "1px solid var(--color-border)",
        backdropFilter: "blur(10px)",
        boxShadow: "var(--shadow-soft)",
      }}
    >
      <div
        className="text-[11px] font-medium uppercase tracking-wider"
        style={{ color: "var(--color-ink-muted)" }}
      >
        {label}
      </div>
      <div
        className="mt-1 text-2xl font-semibold tabular-nums tracking-tight"
        style={{
          fontFamily: "var(--font-display)",
          color: accent ? "var(--color-urgency-high)" : "var(--color-ink)",
        }}
      >
        {value}
      </div>
    </div>
  );
}

export function KpiStrip({ leads }: KpiStripProps) {
  const { t } = useI18n();
  const total = leads.length;
  const high = leads.filter((l) => l.urgency === "High").length;
  const avg =
    total === 0
      ? 0
      : Math.round(leads.reduce((s, l) => s + (l.score || 0), 0) / total);
  const openNew = leads.filter((l) => l.stage === "New").length;

  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      <KpiCard label={t("kpiTotal")} value={total} />
      <KpiCard label={t("kpiHigh")} value={high} accent={high > 0} />
      <KpiCard label={t("kpiAvgScore")} value={avg} />
      <KpiCard label={t("kpiNew")} value={openNew} />
    </div>
  );
}
