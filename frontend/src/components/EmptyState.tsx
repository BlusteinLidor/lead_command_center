import { useI18n } from "../i18n/I18nProvider";

export function EmptyState() {
  const { t } = useI18n();
  return (
    <div
      className="rounded-[var(--radius-xl)] px-6 py-16 text-center"
      style={{
        background: "var(--color-surface)",
        border: "1px dashed var(--color-border-strong)",
      }}
    >
      <p
        className="m-0 text-lg"
        style={{
          fontFamily: "var(--font-display)",
          fontWeight: 600,
          color: "var(--color-ink)",
        }}
      >
        {t("emptyBoard")}
      </p>
      <p
        className="m-0 mt-2 text-sm"
        style={{ color: "var(--color-ink-muted)" }}
      >
        {t("emptyBoardHint")}
      </p>
    </div>
  );
}

export function BoardSkeleton() {
  return (
    <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <div
          key={i}
          className="h-72 animate-pulse rounded-[var(--radius-xl)]"
          style={{ background: "var(--color-canvas-deep)" }}
        />
      ))}
    </div>
  );
}

export function ErrorBanner({
  message,
  onRetry,
}: {
  message: string;
  onRetry: () => void;
}) {
  const { t } = useI18n();
  return (
    <div
      className="mb-4 rounded-[var(--radius-md)] px-4 py-3"
      style={{
        background: "var(--color-urgency-high-bg)",
        border: "1px solid color-mix(in srgb, var(--color-urgency-high) 30%, transparent)",
      }}
    >
      <p
        className="m-0 text-sm font-semibold"
        style={{ color: "var(--color-urgency-high)" }}
      >
        {t("errorTitle")}
      </p>
      <p
        className="m-0 mt-1 text-xs"
        style={{ color: "var(--color-ink-muted)" }}
      >
        {message || t("errorHint")}
      </p>
      <button
        type="button"
        onClick={onRetry}
        className="mt-2 rounded-md px-2.5 py-1 text-xs font-semibold"
        style={{
          background: "var(--color-surface-solid)",
          border: "1px solid var(--color-border)",
          cursor: "pointer",
        }}
      >
        {t("retry")}
      </button>
    </div>
  );
}
