import { motion } from "motion/react";

interface ScoreRingProps {
  score: number;
  size?: number;
  animate?: boolean;
  label?: string;
}

export function ScoreRing({
  score,
  size = 44,
  animate = false,
  label,
}: ScoreRingProps) {
  const stroke = size >= 64 ? 5 : 3.5;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const clamped = Math.max(0, Math.min(100, score));
  const offset = c - (clamped / 100) * c;
  const color =
    clamped >= 80
      ? "var(--color-urgency-high)"
      : clamped >= 55
        ? "var(--color-urgency-med)"
        : "var(--color-urgency-low)";

  return (
    <div
      className="relative inline-flex items-center justify-center"
      style={{ width: size, height: size }}
      title={label ?? `Score ${score}`}
    >
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="var(--color-border-strong)"
          strokeWidth={stroke}
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          initial={animate ? { strokeDashoffset: c } : { strokeDashoffset: offset }}
          animate={{ strokeDashoffset: offset }}
          transition={
            animate
              ? { duration: 0.85, ease: [0.22, 1, 0.36, 1] }
              : { duration: 0.35 }
          }
        />
      </svg>
      <span
        className="absolute font-semibold tabular-nums"
        style={{
          fontSize: size >= 64 ? 18 : 11,
          color: "var(--color-ink)",
        }}
      >
        {clamped}
      </span>
    </div>
  );
}
