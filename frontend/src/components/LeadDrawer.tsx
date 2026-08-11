import type { ReactNode } from "react";
import { AnimatePresence, motion } from "motion/react";
import { X, Mail, Phone } from "lucide-react";
import type { Lead, LeadStage } from "../types/lead";
import { LEAD_STAGES, localizeLeadText } from "../types/lead";
import { useI18n } from "../i18n/I18nProvider";
import { stageLabel } from "../i18n";
import { formatChannel } from "../utils/format";
import { ScoreRing } from "./ScoreRing";
import { UrgencyBadge } from "./UrgencyBadge";

interface LeadDrawerProps {
  lead: Lead | null;
  open: boolean;
  updating: boolean;
  onClose: () => void;
  onStageChange: (stage: LeadStage) => void;
}

export function LeadDrawer({
  lead,
  open,
  updating,
  onClose,
  onStageChange,
}: LeadDrawerProps) {
  const { t, locale, dir } = useI18n();
  const text = lead ? localizeLeadText(lead, locale) : null;

  return (
    <AnimatePresence>
      {open && lead && text && (
        <>
          <motion.div
            className="fixed inset-0 z-40"
            style={{ background: "rgba(28, 36, 34, 0.28)" }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            aria-hidden
          />
          <motion.aside
            role="dialog"
            aria-modal="true"
            aria-label={t("contact")}
            className="fixed inset-y-0 z-50 flex w-full max-w-md flex-col shadow-[var(--shadow-drawer)] sm:max-w-[420px]"
            style={{
              [dir === "rtl" ? "left" : "right"]: 0,
              background: "var(--color-surface-solid)",
              borderInlineStart: "1px solid var(--color-border)",
            }}
            initial={{ x: dir === "rtl" ? "-100%" : "100%" }}
            animate={{ x: 0 }}
            exit={{ x: dir === "rtl" ? "-100%" : "100%" }}
            transition={{ type: "spring", stiffness: 380, damping: 36 }}
          >
            <div
              className="flex items-start justify-between gap-3 px-5 py-4"
              style={{ borderBottom: "1px solid var(--color-border)" }}
            >
              <div className="min-w-0">
                <h2
                  className="m-0 truncate text-lg"
                  style={{
                    fontFamily: "var(--font-display)",
                    fontWeight: 600,
                  }}
                >
                  {text.contact_name?.trim() || t("noName")}
                </h2>
                <div className="mt-1.5 flex flex-wrap items-center gap-2">
                  <UrgencyBadge urgency={lead.urgency} />
                  <span
                    className="text-xs"
                    style={{ color: "var(--color-ink-faint)" }}
                  >
                    {formatChannel(lead.source, lead.channel, locale)}
                  </span>
                </div>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="rounded-lg p-2"
                style={{
                  color: "var(--color-ink-muted)",
                  background: "var(--color-canvas)",
                  border: "none",
                  cursor: "pointer",
                }}
                aria-label={t("drawerClose")}
              >
                <X size={18} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto px-5 py-5">
              <div className="mb-5 flex items-center gap-4">
                <ScoreRing
                  score={lead.score}
                  size={72}
                  animate
                  label={t("score")}
                />
                <div>
                  <div
                    className="text-xs font-medium uppercase tracking-wider"
                    style={{ color: "var(--color-ink-muted)" }}
                  >
                    {t("score")}
                  </div>
                  <div
                    className="text-sm"
                    style={{ color: "var(--color-ink-faint)" }}
                  >
                    {t("intent")}:{" "}
                    <span
                      className="bidi-auto"
                      style={{ color: "var(--color-ink)" }}
                    >
                      {text.detected_intent}
                    </span>
                  </div>
                </div>
              </div>

              <Section title={t("contact")}>
                <MetaRow
                  icon={<Mail size={14} />}
                  label={t("email")}
                  value={lead.contact_email || t("noEmail")}
                />
                <MetaRow
                  icon={<Phone size={14} />}
                  label={t("phone")}
                  value={lead.contact_phone || t("noPhone")}
                />
                <MetaRow
                  label={t("source")}
                  value={formatChannel(lead.source, null, locale)}
                />
                <MetaRow
                  label={t("channel")}
                  value={formatChannel(null, lead.channel, locale)}
                />
              </Section>

              <Section title={t("aiSummary")}>
                <p
                  className="bidi-auto m-0 text-sm leading-relaxed"
                  style={{ color: "var(--color-ink)" }}
                >
                  {text.summary}
                </p>
              </Section>

              <Section title={t("message")}>
                <p
                  className="bidi-auto m-0 text-sm leading-relaxed"
                  style={{
                    color: "var(--color-ink-muted)",
                    whiteSpace: "pre-wrap",
                  }}
                >
                  {text.message_body}
                </p>
              </Section>

              <Section title={t("moveTo")}>
                <div className="grid grid-cols-2 gap-2">
                  {LEAD_STAGES.map((stage) => {
                    const active = lead.stage === stage;
                    return (
                      <button
                        key={stage}
                        type="button"
                        disabled={updating || active}
                        onClick={() => onStageChange(stage)}
                        className="rounded-[var(--radius-sm)] px-3 py-2.5 text-sm font-semibold transition-colors disabled:opacity-60"
                        style={{
                          background: active
                            ? "var(--color-primary)"
                            : "var(--color-canvas)",
                          color: active ? "#fff" : "var(--color-ink)",
                          border: "1px solid var(--color-border)",
                          cursor: active || updating ? "default" : "pointer",
                        }}
                      >
                        {stageLabel(locale, stage)}
                      </button>
                    );
                  })}
                </div>
              </Section>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <section className="mb-5">
      <h3
        className="m-0 mb-2 text-[11px] font-semibold uppercase tracking-wider"
        style={{ color: "var(--color-ink-muted)" }}
      >
        {title}
      </h3>
      <div
        className="rounded-[var(--radius-md)] p-3"
        style={{
          background: "var(--color-canvas)",
          border: "1px solid var(--color-border)",
        }}
      >
        {children}
      </div>
    </section>
  );
}

function MetaRow({
  icon,
  label,
  value,
}: {
  icon?: ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center gap-2 py-1.5 text-sm">
      {icon && (
        <span style={{ color: "var(--color-ink-faint)" }}>{icon}</span>
      )}
      <span style={{ color: "var(--color-ink-muted)", minWidth: 72 }}>
        {label}
      </span>
      <span
        className="bidi-auto font-medium"
        style={{ color: "var(--color-ink)" }}
      >
        {value}
      </span>
    </div>
  );
}
