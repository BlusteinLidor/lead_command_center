import { useI18n } from "../i18n/I18nProvider";
import type { Locale } from "../i18n";

export function LanguageToggle() {
  const { locale, setLocale } = useI18n();

  const btn = (code: Locale, label: string) => {
    const active = locale === code;
    return (
      <button
        type="button"
        onClick={() => setLocale(code)}
        className="rounded-md px-2.5 py-1 text-xs font-semibold transition-colors"
        style={{
          background: active ? "var(--color-primary)" : "transparent",
          color: active ? "#fff" : "var(--color-ink-muted)",
        }}
        aria-pressed={active}
      >
        {label}
      </button>
    );
  };

  return (
    <div
      className="inline-flex items-center gap-0.5 rounded-lg p-0.5"
      style={{
        background: "var(--color-surface-solid)",
        border: "1px solid var(--color-border)",
      }}
      role="group"
      aria-label="Language"
    >
      {btn("en", "EN")}
      {btn("he", "עב")}
    </div>
  );
}
