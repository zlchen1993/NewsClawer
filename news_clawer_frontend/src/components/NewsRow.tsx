import type { NewsBrief } from "../api";

function formatHot(raw: string | null): string | null {
  if (!raw) return null;
  const n = Number(raw);
  if (!Number.isFinite(n)) return raw;
  if (n >= 1_0000_0000) return (n / 1_0000_0000).toFixed(1) + "亿";
  if (n >= 1_0000) return (n / 1_0000).toFixed(1) + "万";
  return String(n);
}

export function NewsRow({ item, onOpen }: { item: NewsBrief; onOpen: (id: number) => void }) {
  const rank = item.rank ?? 0;
  const top = rank >= 1 && rank <= 3 ? `top top-${rank}` : "";
  const hot = formatHot(item.hot_value);
  return (
    <button className="row" onClick={() => onOpen(item.id)} title={item.title}>
      <span className={`rank ${top}`}>{rank || "·"}</span>
      <span className="row-title">{item.title}</span>
      {hot && <span className="row-hot">{hot}</span>}
    </button>
  );
}
