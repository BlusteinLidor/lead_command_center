import { LanguageToggle } from "./LanguageToggle";
import {
  IncomingSettings,
  type IncomingIntervalSec,
} from "./IncomingSettings";
import { useI18n } from "../i18n/I18nProvider";
import type { LeadWebhookPayload } from "../types/lead";

interface TopBarProps {
  incomingIntervalSec: IncomingIntervalSec;
  onIncomingIntervalChange: (value: IncomingIntervalSec) => void;
  onReset: () => Promise<void>;
  onSimulate: (payload: LeadWebhookPayload) => Promise<unknown>;
}

export function TopBar({
  incomingIntervalSec,
  onIncomingIntervalChange,
  onReset,
  onSimulate,
}: TopBarProps) {
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
        <LanguageToggle />
        <IncomingSettings
          intervalSec={incomingIntervalSec}
          onIntervalChange={onIncomingIntervalChange}
          onReset={onReset}
          onSimulate={onSimulate}
        />
      </div>
    </header>
  );
}
