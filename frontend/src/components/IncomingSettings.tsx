import { useEffect, useId, useRef, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { Settings, X } from "lucide-react";
import { useI18n } from "../i18n/I18nProvider";

/** Seconds between auto-inbound leads. `0` = never (default). */
export type IncomingIntervalSec = 0 | 15 | 30 | 45 | 60;

export const INCOMING_INTERVAL_OPTIONS: IncomingIntervalSec[] = [
  0, 15, 30, 45, 60,
];

interface IncomingSettingsProps {
  intervalSec: IncomingIntervalSec;
  onIntervalChange: (value: IncomingIntervalSec) => void;
  /** Side opposite the brand so it stays corner-visible while filming. */
  placement?: "start" | "end";
}

export function IncomingSettings({
  intervalSec,
  onIntervalChange,
  placement = "end",
}: IncomingSettingsProps) {
  const { t } = useI18n();
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const titleId = useId();
  const active = intervalSec > 0;

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
            className="absolute z-40 mt-2 w-[min(18rem,calc(100vw-2rem))] rounded-[var(--radius-lg)] p-3.5"
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
            <div className="flex flex-col gap-1.5">
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

            <button
              type="button"
              onClick={() => setOpen(false)}
              className="mt-3 w-full rounded-lg px-3 py-2 text-sm font-semibold text-white"
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
