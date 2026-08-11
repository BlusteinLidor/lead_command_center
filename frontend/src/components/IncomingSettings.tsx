import { useEffect, useId, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { Loader2, RotateCcw, Settings, Sparkles, X } from "lucide-react";
import {
  ENGLISH_CLINIC_SCENARIOS,
  HEBREW_CLINIC_SCENARIOS,
} from "../data/clinicScenarios";
import { useI18n } from "../i18n/I18nProvider";
import type { LeadWebhookPayload } from "../types/lead";

/** Seconds between auto-inbound leads. `0` = never (default). */
export type IncomingIntervalSec = 0 | 15 | 30 | 45 | 60;

export const INCOMING_INTERVAL_OPTIONS: IncomingIntervalSec[] = [
  0, 15, 30, 45, 60,
];

interface IncomingSettingsProps {
  intervalSec: IncomingIntervalSec;
  onIntervalChange: (value: IncomingIntervalSec) => void;
  onReset: () => Promise<void>;
  onSimulate: (payload: LeadWebhookPayload) => Promise<unknown>;
  /** Side opposite the brand so it stays corner-visible while filming. */
  placement?: "start" | "end";
}

export function IncomingSettings({
  intervalSec,
  onIntervalChange,
  onReset,
  onSimulate,
  placement = "end",
}: IncomingSettingsProps) {
  const { t, locale } = useI18n();
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const titleId = useId();
  const active = intervalSec > 0;

  // Default & stay aligned with UI language so simulated leads match EN/HE.
  const [scenarioLang, setScenarioLang] = useState<"he" | "en">(locale);
  const [scenarioId, setScenarioId] = useState(
    () =>
      (locale === "he" ? HEBREW_CLINIC_SCENARIOS : ENGLISH_CLINIC_SCENARIOS)[0]
        .id,
  );
  const [resetting, setResetting] = useState(false);
  const [simulating, setSimulating] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const scenarios = useMemo(
    () =>
      scenarioLang === "he" ? HEBREW_CLINIC_SCENARIOS : ENGLISH_CLINIC_SCENARIOS,
    [scenarioLang],
  );

  const activeScenario =
    scenarios.find((s) => s.id === scenarioId) ?? scenarios[0];

  useEffect(() => {
    setScenarioLang(locale);
    const list =
      locale === "he" ? HEBREW_CLINIC_SCENARIOS : ENGLISH_CLINIC_SCENARIOS;
    setScenarioId(list[0].id);
  }, [locale]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    const onPointer = (e: MouseEvent) => {
      if (!rootRef.current?.contains(e.target as Node)) setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    window.addEventListener("mousedown", onPointer);
    return () => {
      window.removeEventListener("keydown", onKey);
      window.removeEventListener("mousedown", onPointer);
    };
  }, [open]);

  const labelFor = (sec: IncomingIntervalSec) => {
    if (sec === 0) return t("incomingNever");
    return t("incomingEvery", { n: sec });
  };

  const handleLangChange = (lang: "he" | "en") => {
    setScenarioLang(lang);
    const list =
      lang === "he" ? HEBREW_CLINIC_SCENARIOS : ENGLISH_CLINIC_SCENARIOS;
    setScenarioId(list[0].id);
  };

  const handleReset = async () => {
    setResetting(true);
    setError(null);
    setMessage(null);
    try {
      await onReset();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setResetting(false);
    }
  };

  const handleSimulate = async () => {
    if (!activeScenario) return;
    setSimulating(true);
    setError(null);
    setMessage(null);
    try {
      await onSimulate(activeScenario.payload);
      setMessage(t("simulateSuccess"));
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div
      ref={rootRef}
      className="relative"
      style={{
        marginInlineStart: placement === "end" ? undefined : 0,
      }}
    >
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-haspopup="dialog"
        aria-label={t("settingsOpen")}
        title={t("settingsOpen")}
        className="relative inline-flex h-9 w-9 items-center justify-center rounded-lg transition-colors"
        style={{
          background: open
            ? "var(--color-primary)"
            : "var(--color-surface-solid)",
          color: open ? "#fff" : "var(--color-ink)",
          border: "1px solid var(--color-border-strong)",
          cursor: "pointer",
        }}
      >
        <Settings size={16} strokeWidth={2.25} />
        {active && (
          <span
            className="absolute end-1 top-1 h-1.5 w-1.5 rounded-full"
            style={{ background: open ? "#F4EFE6" : "var(--color-accent)" }}
            aria-hidden
          />
        )}
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            role="dialog"
            aria-modal="false"
            aria-labelledby={titleId}
            initial={{ opacity: 0, y: -6, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -6, scale: 0.98 }}
            transition={{ duration: 0.18, ease: [0.22, 1, 0.36, 1] }}
            className="absolute z-40 mt-2 max-h-[min(36rem,calc(100vh-6rem))] w-[min(22rem,calc(100vw-2rem))] overflow-y-auto rounded-[var(--radius-lg)] p-3.5"
            style={{
              insetInlineEnd: 0,
              background: "var(--color-surface-solid)",
              border: "1px solid var(--color-border-strong)",
              boxShadow: "var(--shadow-soft)",
            }}
          >
            <div className="mb-2 flex items-start justify-between gap-2">
              <div>
                <h2
                  id={titleId}
                  className="m-0 text-sm font-semibold"
                  style={{
                    fontFamily: "var(--font-display)",
                    color: "var(--color-ink)",
                  }}
                >
                  {t("settingsTitle")}
                </h2>
                <p
                  className="m-0 mt-1 text-xs leading-relaxed"
                  style={{ color: "var(--color-ink-muted)" }}
                >
                  {t("incomingDesc")}
                </p>
              </div>
              <button
                type="button"
                onClick={() => setOpen(false)}
                aria-label={t("settingsDone")}
                className="inline-flex h-7 w-7 shrink-0 items-center justify-center rounded-md"
                style={{
                  background: "transparent",
                  border: "none",
                  color: "var(--color-ink-muted)",
                  cursor: "pointer",
                }}
              >
                <X size={14} />
              </button>
            </div>

            <p
              className="m-0 mb-2 text-[11px] font-medium uppercase tracking-wider"
              style={{ color: "var(--color-ink-muted)" }}
            >
              {t("incomingFrequency")}
            </p>
            <div className="mb-4 flex flex-col gap-1.5">
              {INCOMING_INTERVAL_OPTIONS.map((sec) => {
                const selected = intervalSec === sec;
                return (
                  <button
                    key={sec}
                    type="button"
                    onClick={() => onIntervalChange(sec)}
                    className="rounded-lg px-3 py-2 text-start text-sm font-medium transition-colors"
                    style={{
                      background: selected
                        ? "var(--color-primary-soft)"
                        : "var(--color-canvas)",
                      color: selected
                        ? "var(--color-primary)"
                        : "var(--color-ink)",
                      border: `1px solid ${
                        selected
                          ? "var(--color-primary-mid)"
                          : "var(--color-border)"
                      }`,
                      cursor: "pointer",
                    }}
                  >
                    {labelFor(sec)}
                  </button>
                );
              })}
            </div>

            <div
              className="mb-3 rounded-[var(--radius-md)] p-3"
              style={{
                background: "var(--color-canvas)",
                border: "1px solid var(--color-border)",
              }}
            >
              <div className="mb-1 flex items-center gap-2">
                <RotateCcw size={14} style={{ color: "var(--color-primary)" }} />
                <h3 className="m-0 text-sm font-semibold">{t("resetTitle")}</h3>
              </div>
              <p
                className="m-0 mb-2.5 text-xs leading-relaxed"
                style={{ color: "var(--color-ink-muted)" }}
              >
                {t("resetDesc")}
              </p>
              <button
                type="button"
                onClick={() => void handleReset()}
                disabled={resetting}
                className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-semibold disabled:opacity-60"
                style={{
                  background: "var(--color-surface-solid)",
                  color: "var(--color-ink)",
                  border: "1px solid var(--color-border)",
                  cursor: resetting ? "wait" : "pointer",
                }}
              >
                {resetting && <Loader2 size={14} className="animate-spin" />}
                {resetting ? t("resetBusy") : t("resetConfirm")}
              </button>
            </div>

            <div
              className="mb-3 rounded-[var(--radius-md)] p-3"
              style={{
                background: "var(--color-canvas)",
                border: "1px solid var(--color-border)",
              }}
            >
              <div className="mb-1 flex items-center gap-2">
                <Sparkles size={14} style={{ color: "var(--color-accent)" }} />
                <h3 className="m-0 text-sm font-semibold">
                  {t("simulateTitle")}
                </h3>
              </div>
              <p
                className="m-0 mb-2.5 text-xs leading-relaxed"
                style={{ color: "var(--color-ink-muted)" }}
              >
                {t("simulateDesc")}
              </p>

              <label
                className="mb-1 block text-[11px] font-medium uppercase tracking-wider"
                style={{ color: "var(--color-ink-muted)" }}
              >
                {t("simulateLang")}
              </label>
              <div className="mb-2.5 flex gap-2">
                {(["he", "en"] as const).map((lang) => (
                  <button
                    key={lang}
                    type="button"
                    onClick={() => handleLangChange(lang)}
                    className="rounded-md px-2.5 py-1 text-xs font-semibold"
                    style={{
                      background:
                        scenarioLang === lang
                          ? "var(--color-primary)"
                          : "var(--color-surface-solid)",
                      color:
                        scenarioLang === lang ? "#fff" : "var(--color-ink)",
                      border: "1px solid var(--color-border)",
                      cursor: "pointer",
                    }}
                  >
                    {lang === "he" ? "עברית" : "English"}
                  </button>
                ))}
              </div>

              <label
                className="mb-1 block text-[11px] font-medium uppercase tracking-wider"
                style={{ color: "var(--color-ink-muted)" }}
              >
                {t("simulatePick")}
              </label>
              <select
                value={activeScenario?.id}
                onChange={(e) => setScenarioId(e.target.value)}
                className="mb-2.5 w-full rounded-lg px-3 py-2 text-sm"
                style={{
                  background: "var(--color-surface-solid)",
                  border: "1px solid var(--color-border)",
                  color: "var(--color-ink)",
                }}
              >
                {scenarios.map((s) => (
                  <option key={s.id} value={s.id}>
                    {locale === "he" ? s.labelHe : s.labelEn}
                  </option>
                ))}
              </select>

              <button
                type="button"
                onClick={() => void handleSimulate()}
                disabled={simulating}
                className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-semibold text-white disabled:opacity-70"
                style={{
                  background: "var(--color-primary)",
                  border: "none",
                  cursor: simulating ? "wait" : "pointer",
                }}
              >
                {simulating && <Loader2 size={14} className="animate-spin" />}
                {simulating ? t("simulateBusy") : t("simulateSend")}
              </button>
            </div>

            {(message || error) && (
              <p
                className="m-0 mb-3 text-sm"
                style={{
                  color: error
                    ? "var(--color-urgency-high)"
                    : "var(--color-sage)",
                }}
              >
                {error || message}
              </p>
            )}

            <button
              type="button"
              onClick={() => setOpen(false)}
              className="w-full rounded-lg px-3 py-2 text-sm font-semibold text-white"
              style={{
                background: "var(--color-primary)",
                border: "none",
                cursor: "pointer",
              }}
            >
              {t("settingsDone")}
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
