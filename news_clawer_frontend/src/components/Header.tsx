import type { Theme } from "../useTheme";

interface Props {
  theme: Theme;
  onToggleTheme: () => void;
  onRefresh: () => void;
  onUpdate: () => void;
  updating: boolean;
  date: string | null;
}

export function Header({ theme, onToggleTheme, onRefresh, onUpdate, updating, date }: Props) {
  return (
    <header className="topbar">
      <div className="brand">
        <span className="brand-mark">热</span>
        <div className="brand-text">
          <h1>今日热榜</h1>
          {date && <p className="brand-sub">更新于 {date}</p>}
        </div>
      </div>
      <div className="actions">
        <button className="btn primary" onClick={onUpdate} disabled={updating} title="抓取各平台最新数据">
          <span className={updating ? "spin" : ""}>⟳</span> {updating ? "更新中…" : "更新数据"}
        </button>
        <button className="btn" onClick={onRefresh} disabled={updating} title="重新拉取">
          刷新
        </button>
        <button className="btn icon" onClick={onToggleTheme} title="切换主题">
          {theme === "light" ? "🌙" : "☀︎"}
        </button>
      </div>
    </header>
  );
}
