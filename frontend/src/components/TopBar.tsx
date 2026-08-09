import { FlaskConical } from "lucide-react";
import { LanguageToggle } from "./LanguageToggle";
import { useI18n } from "../i18n/I18nProvider";

interface TopBarProps {
  demoOpen: boolean;
  onToggleDemo: () => void;
}

export function TopBar({ demoOpen, onToggleDemo }: TopBarProps) {
  const { t } = useI18n();

  return (
    <header
      className="flex flex-wrap items-center justify-between gap-3"
      style={{ marginBlockEnd: "1.25rem" }}
    >
      <div className="flex min-w-0 items-center gap-3">
        <div
          className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl"
          style={{
            background: "var(--color-primary)",
            color: "#F4EFE6",
            fontFamily: "var(--font-display)",
            fontWeight: 600,
            fontSize: 18,
          }}
          aria-hidden
        >
          LC
        </div>
        <div className="min-w-0">
          <h1
            className="m-0 truncate text-[1.35rem] leading-tight tracking-tight sm:text-[1.55rem]"
            style={{
              fontFamily: "var(--font-display)",
              fontWeight: 600,
              color: "var(--color-ink)",
            }}
          >
            {t("brand")}
          </h1>
          <p
            className="m-0 mt-0.5 text-sm"
            style={{ color: "var(--color-ink-muted)" }}
          >
            {t("clinic")}
          </p>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <span
          className="rounded-full px-2.5 py-1 text-[11px] font-medium"
          style={{
            background: "var(--color-primary-soft)",
            color: "var(--color-primary)",
            border: "1px solid var(--color-primary-mid)",
          }}
        >
          {t("demoChip")}
        </span>
        <LanguageToggle />
        <button
          type="button"
          onClick={onToggleDemo}
          className="inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors"
          style={{
            background: demoOpen
              ? "var(--color-primary)"
              : "var(--color-surface-solid)",
            color: demoOpen ? "#fff" : "var(--color-ink)",
            border: "1px solid var(--color-border-strong)",
            cursor: "pointer",
          }}
        >
          <FlaskConical size={14} strokeWidth={2.25} />
          {demoOpen ? t("demoClose") : t("demoOpen")}
        </button>
      </div>
    </header>
  );
}
