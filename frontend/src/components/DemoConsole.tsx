import { useMemo, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Loader2, RotateCcw, Sparkles } from "lucide-react";
import {
  ENGLISH_CLINIC_SCENARIOS,
  HEBREW_CLINIC_SCENARIOS,
} from "../data/clinicScenarios";
import { useI18n } from "../i18n/I18nProvider";
import type { LeadWebhookPayload } from "../types/lead";

interface DemoConsoleProps {
  open: boolean;
  onReset: () => Promise<void>;
  onSimulate: (payload: LeadWebhookPayload) => Promise<unknown>;
}

export function DemoConsole({ open, onReset, onSimulate }: DemoConsoleProps) {
  const { t, locale } = useI18n();
  const [scenarioLang, setScenarioLang] = useState<"he" | "en">("he");
  const [scenarioId, setScenarioId] = useState(HEBREW_CLINIC_SCENARIOS[0].id);
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
    <AnimatePresence>
      {open && (
        <motion.aside
          initial={{ opacity: 0, y: -8, height: 0 }}
          animate={{ opacity: 1, y: 0, height: "auto" }}
          exit={{ opacity: 0, y: -8, height: 0 }}
          transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
          className="overflow-hidden"
          style={{ marginBlockEnd: "1.25rem" }}
        >
          <div
            className="rounded-[var(--radius-xl)] p-4 sm:p-5"
            style={{
              background: "var(--color-surface)",
              border: "1px solid var(--color-border-strong)",
              boxShadow: "var(--shadow-soft)",
              backdropFilter: "blur(12px)",
            }}
          >
            <h2
              className="m-0 mb-4 text-base"
              style={{
                fontFamily: "var(--font-display)",
                fontWeight: 600,
              }}
            >
              {t("demoTitle")}
            </h2>

            <div className="grid gap-4 lg:grid-cols-2">
              <div
                className="rounded-[var(--radius-md)] p-4"
                style={{
                  background: "var(--color-surface-solid)",
                  border: "1px solid var(--color-border)",
                }}
              >
                <div className="mb-1 flex items-center gap-2">
                  <RotateCcw size={16} style={{ color: "var(--color-primary)" }} />
                  <h3 className="m-0 text-sm font-semibold">{t("resetTitle")}</h3>
                </div>
                <p
                  className="m-0 mb-3 text-xs leading-relaxed"
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
                    background: "var(--color-canvas-deep)",
                    color: "var(--color-ink)",
                    border: "1px solid var(--color-border)",
                    cursor: resetting ? "wait" : "pointer",
                  }}
                >
                  {resetting && (
                    <Loader2 size={14} className="animate-spin" />
                  )}
                  {resetting ? t("resetBusy") : t("resetConfirm")}
                </button>
              </div>

              <div
                className="rounded-[var(--radius-md)] p-4"
                style={{
                  background: "var(--color-surface-solid)",
                  border: "1px solid var(--color-border)",
                }}
              >
                <div className="mb-1 flex items-center gap-2">
                  <Sparkles size={16} style={{ color: "var(--color-accent)" }} />
                  <h3 className="m-0 text-sm font-semibold">
                    {t("simulateTitle")}
                  </h3>
                </div>
                <p
                  className="m-0 mb-3 text-xs leading-relaxed"
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
                <div className="mb-3 flex gap-2">
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
                            : "var(--color-canvas)",
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
                  className="mb-3 w-full rounded-lg px-3 py-2 text-sm"
                  style={{
                    background: "var(--color-canvas)",
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
                  {simulating && (
                    <Loader2 size={14} className="animate-spin" />
                  )}
                  {simulating ? t("simulateBusy") : t("simulateSend")}
                </button>
              </div>
            </div>

            {(message || error) && (
              <p
                className="m-0 mt-3 text-sm"
                style={{
                  color: error
                    ? "var(--color-urgency-high)"
                    : "var(--color-sage)",
                }}
              >
                {error || message}
              </p>
            )}
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
