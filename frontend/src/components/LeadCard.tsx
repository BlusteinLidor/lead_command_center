import { motion } from "motion/react";
import type { Lead } from "../types/lead";
import { localizeLeadText } from "../types/lead";
import { useI18n } from "../i18n/I18nProvider";
import { formatChannel, initials, relativeTime } from "../utils/format";
import { ScoreRing } from "./ScoreRing";
import { UrgencyBadge } from "./UrgencyBadge";

interface LeadCardProps {
  lead: Lead;
  selected: boolean;
  highlight: boolean;
  onClick: () => void;
}

export function LeadCard({
  lead,
  selected,
  highlight,
  onClick,
}: LeadCardProps) {
  const { t, locale } = useI18n();
  const text = localizeLeadText(lead, locale);
  const name = text.contact_name?.trim() || t("noName");
  const isHigh = lead.urgency === "High";
  const ago = relativeTime(lead.created_at, locale, {
    justNow: t("justNow"),
    minutesAgo: (n) => t("minutesAgo", { n }),
    hoursAgo: (n) => t("hoursAgo", { n }),
    daysAgo: (n) => t("daysAgo", { n }),
  });

  return (
    <motion.button
      type="button"
      id={`lead-${lead.id}`}
      layout
      layoutId={`lead-card-${lead.id}`}
      initial={highlight ? { opacity: 0, y: -12, scale: 0.96 } : false}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ type: "spring", stiffness: 420, damping: 32 }}
      onClick={onClick}
      className="w-full cursor-pointer scroll-mt-4 rounded-[var(--radius-md)] p-3 text-start transition-shadow"
      style={{
        background: selected
          ? "var(--color-primary-soft)"
          : "var(--color-surface-solid)",
        border: `1px solid ${
          isHigh
            ? "color-mix(in srgb, var(--color-urgency-high) 45%, var(--color-border))"
            : selected
              ? "var(--color-primary-mid)"
              : "var(--color-border)"
        }`,
        boxShadow: highlight
          ? "0 0 0 2px color-mix(in srgb, var(--color-primary) 35%, transparent)"
          : isHigh
            ? "0 4px 14px rgba(196, 90, 58, 0.1)"
            : "none",
      }}
    >
      <div className="flex items-start gap-2.5">
        <div
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-xs font-semibold"
          style={{
            background: "var(--color-canvas-deep)",
            color: "var(--color-primary)",
          }}
        >
          {initials(text.contact_name)}
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0">
              <div
                className="truncate text-sm font-semibold"
                style={{ color: "var(--color-ink)" }}
              >
                {name}
              </div>
              <div
                className="mt-0.5 flex flex-wrap items-center gap-1.5 text-[11px]"
                style={{ color: "var(--color-ink-faint)" }}
              >
                <span
                  className="rounded-md px-1.5 py-0.5 font-medium"
                  style={{
                    background: "var(--color-canvas)",
                    color: "var(--color-ink-muted)",
                  }}
                >
                  {formatChannel(lead.source, lead.channel, locale)}
                </span>
                <span>{ago}</span>
              </div>
            </div>
            <ScoreRing score={lead.score} size={36} />
          </div>
          <div className="mt-2">
            <UrgencyBadge urgency={lead.urgency} />
          </div>
          <p
            className="bidi-auto mt-2 line-clamp-2 text-xs leading-relaxed"
            style={{ color: "var(--color-ink-muted)", margin: 0 }}
          >
            {text.summary}
          </p>
        </div>
      </div>
    </motion.button>
  );
}
