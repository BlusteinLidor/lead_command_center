import type { Urgency } from "../types/lead";
import { useI18n } from "../i18n/I18nProvider";
import { urgencyLabel } from "../i18n";

export function UrgencyBadge({ urgency }: { urgency: Urgency | string }) {
  const { locale } = useI18n();
  const key = (urgency || "Low").toString();
  const styles =
    key === "High"
      ? {
          bg: "var(--color-urgency-high-bg)",
          color: "var(--color-urgency-high)",
        }
      : key === "Med"
        ? {
            bg: "var(--color-urgency-med-bg)",
            color: "var(--color-urgency-med)",
          }
        : {
            bg: "var(--color-urgency-low-bg)",
            color: "var(--color-urgency-low)",
          };

  return (
    <span
      className="inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-semibold tracking-wide uppercase"
      style={{ background: styles.bg, color: styles.color }}
    >
      {urgencyLabel(locale, key)}
    </span>
  );
}
