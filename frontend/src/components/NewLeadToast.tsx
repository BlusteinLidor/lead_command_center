import { AnimatePresence, motion } from "motion/react";
import type { Lead } from "../types/lead";
import { localizeLeadText } from "../types/lead";
import { useI18n } from "../i18n/I18nProvider";
import { formatChannel } from "../utils/format";
import { urgencyLabel } from "../i18n";

interface NewLeadToastProps {
  lead: Lead | null;
  onDismiss: () => void;
  onOpen: (lead: Lead) => void;
}

export function NewLeadToast({ lead, onDismiss, onOpen }: NewLeadToastProps) {
  const { t, locale } = useI18n();
  const text = lead ? localizeLeadText(lead, locale) : null;
  const name = text?.contact_name?.trim() || t("noName");
  const isHigh = lead?.urgency === "High";

  return (
    <AnimatePresence>
      {lead && (
        <motion.div
          key={lead.id}
          className="pointer-events-none fixed inset-x-0 bottom-0 z-40 flex justify-center px-4"
          style={{ paddingBottom: "max(1.25rem, env(safe-area-inset-bottom))" }}
          initial={{ opacity: 0, y: 28 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 16, transition: { duration: 0.28 } }}
          transition={{ type: "spring", stiffness: 380, damping: 28 }}
        >
          <div
            className="pointer-events-auto flex max-w-[min(420px,100%)] items-stretch overflow-hidden rounded-[var(--radius-lg)]"
            style={{
              background:
                "color-mix(in srgb, var(--color-surface-solid) 92%, transparent)",
              border: "1px solid var(--color-border-strong)",
              boxShadow:
                "0 1px 2px rgba(28, 36, 34, 0.05), 0 12px 36px rgba(28, 36, 34, 0.12)",
              backdropFilter: "blur(12px)",
            }}
          >
            <button
              type="button"
              onClick={() => onOpen(lead)}
              className="group flex min-w-0 flex-1 items-center gap-3 px-3.5 py-2.5 text-start"
              style={{
                background: "transparent",
                border: "none",
                cursor: "pointer",
              }}
              aria-label={t("toastNewLeadAria", { name })}
            >
              <span
                className="relative flex h-9 w-9 shrink-0 items-center justify-center rounded-full"
                style={{
                  background: isHigh
                    ? "var(--color-urgency-high-bg)"
                    : "var(--color-sage-soft)",
                }}
                aria-hidden
              >
                <span
                  className="new-lead-pulse absolute inset-0 rounded-full"
                  style={{
                    background: isHigh
                      ? "var(--color-urgency-high)"
                      : "var(--color-sage)",
                  }}
                />
                <span
                  className="relative h-2 w-2 rounded-full"
                  style={{
                    background: isHigh
                      ? "var(--color-urgency-high)"
                      : "var(--color-sage)",
                    boxShadow: `0 0 0 3px ${
                      isHigh
                        ? "var(--color-urgency-high-bg)"
                        : "var(--color-sage-soft)"
                    }`,
                  }}
                />
              </span>

              <span className="min-w-0 flex-1">
                <span
                  className="block text-[11px] font-semibold uppercase tracking-[0.06em]"
                  style={{ color: "var(--color-ink-faint)" }}
                >
                  {t("toastNewLead")}
                </span>
                <span
                  className="mt-0.5 block truncate text-sm font-semibold"
                  style={{ color: "var(--color-ink)" }}
                >
                  {name}
                </span>
                <span
                  className="mt-0.5 block truncate text-[11px]"
                  style={{ color: "var(--color-ink-muted)" }}
                >
                  {urgencyLabel(locale, String(lead.urgency))}
                  {" · "}
                  {formatChannel(lead.source, lead.channel, locale)}
                </span>
              </span>

              <span
                className="shrink-0 text-xs font-medium"
                style={{ color: "var(--color-primary)", opacity: 0.9 }}
              >
                {t("toastView")}
              </span>
            </button>

            <button
              type="button"
              onClick={onDismiss}
              className="flex w-9 shrink-0 items-center justify-center self-stretch text-base leading-none"
              style={{
                background: "transparent",
                border: "none",
                borderInlineStart: "1px solid var(--color-border)",
                color: "var(--color-ink-faint)",
                cursor: "pointer",
              }}
              aria-label={t("drawerClose")}
            >
              ×
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
