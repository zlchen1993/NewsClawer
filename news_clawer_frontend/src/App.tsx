import { useCallback, useEffect, useState } from "react";
import { getPlatforms, triggerCrawl, type PlatformInfo } from "./api";
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
  const [updating, setUpdating] = useState(false);

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

  const refresh = useCallback(() => {
    load();
    setReloadKey((k) => k + 1);
  }, [load]);

  // 触发后台爬取全部平台，因爬取异步，分几次轮询刷新看板
  const update = useCallback(async () => {
    if (updating) return;
    setUpdating(true);
    try {
      await triggerCrawl();
      // 爬取异步，等约 12 秒后自动刷新一次看板
      await new Promise((r) => setTimeout(r, 12000));
      refresh();
    } catch (e) {
      console.error(e);
    } finally {
      setUpdating(false);
    }
  }, [updating, refresh]);

  const latestDate =
    platforms
      .map((p) => p.latest_date)
      .filter((d): d is string => !!d)
      .sort()
      .pop() ?? null;

  return (
    <div className="app">
      <div className="grain" aria-hidden />
      <Header
        theme={theme}
        onToggleTheme={toggleTheme}
        onRefresh={refresh}
        onUpdate={update}
        updating={updating}
        date={latestDate}
      />
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
