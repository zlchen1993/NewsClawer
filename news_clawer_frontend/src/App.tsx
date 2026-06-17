import { useCallback, useEffect, useState } from "react";
import { getPlatforms, type PlatformInfo } from "./api";
import { Header } from "./components/Header";
import { PlatformCard } from "./components/PlatformCard";
import { DetailDrawer } from "./components/DetailDrawer";
import { useTheme } from "./useTheme";

export default function App() {
  const [theme, toggleTheme] = useTheme();
  const [platforms, setPlatforms] = useState<PlatformInfo[]>([]);
  const [state, setState] = useState<"loading" | "ok" | "error">("loading");
  const [openId, setOpenId] = useState<number | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

  const load = useCallback(() => {
    setState("loading");
    getPlatforms()
      .then((p) => {
        setPlatforms(p);
        setState("ok");
      })
      .catch(() => setState("error"));
  }, []);

  useEffect(load, [load]);

  const refresh = () => {
    load();
    setReloadKey((k) => k + 1);
  };

  const latestDate =
    platforms
      .map((p) => p.latest_date)
      .filter((d): d is string => !!d)
      .sort()
      .pop() ?? null;

  return (
    <div className="app">
      <div className="grain" aria-hidden />
      <Header theme={theme} onToggleTheme={toggleTheme} onRefresh={refresh} date={latestDate} />
      <main className="board">
        {state === "loading" && <p className="board-hint">加载中…</p>}
        {state === "error" && (
          <p className="board-hint err">
            无法连接后端，请确认服务已启动（:8000）。
            <button className="btn" onClick={refresh}>
              重试
            </button>
          </p>
        )}
        {state === "ok" && platforms.length === 0 && (
          <p className="board-hint">暂无平台数据，先跑一次爬取吧。</p>
        )}
        {state === "ok" && platforms.length > 0 && (
          <div className="grid">
            {platforms.map((p, i) => (
              <PlatformCard
                key={p.platform}
                platform={p.platform}
                count={p.count}
                index={i}
                onOpen={setOpenId}
                reloadKey={reloadKey}
              />
            ))}
          </div>
        )}
      </main>
      <footer className="foot">NewsClawer · 多平台热点聚合</footer>
      <DetailDrawer id={openId} onClose={() => setOpenId(null)} />
    </div>
  );
}
