import type { Theme } from "../useTheme";

interface Props {
  theme: Theme;
  onToggleTheme: () => void;
  onRefresh: () => void;
  date: string | null;
}

export function Header({ theme, onToggleTheme, onRefresh, date }: Props) {
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
        <button className="btn" onClick={onRefresh} title="刷新">
          ↻ 刷新
        </button>
        <button className="btn icon" onClick={onToggleTheme} title="切换主题">
          {theme === "light" ? "🌙" : "☀︎"}
        </button>
      </div>
    </header>
  );
}
