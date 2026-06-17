import { useEffect, useState } from "react";
import { getNews, type NewsBrief } from "../api";
import { platformMeta } from "../platforms";
import { NewsRow } from "./NewsRow";

interface Props {
  platform: string;
  count: number;
  index: number;
  onOpen: (id: number) => void;
  reloadKey: number;
}

export function PlatformCard({ platform, count, index, onOpen, reloadKey }: Props) {
  const meta = platformMeta(platform);
  const [items, setItems] = useState<NewsBrief[]>([]);
  const [state, setState] = useState<"loading" | "ok" | "error">("loading");
  const [iconOk, setIconOk] = useState(Boolean(meta.icon));

  useEffect(() => {
    let alive = true;
    setState("loading");
    getNews(platform, { sort: "rank", pageSize: 100 })
      .then((r) => {
        if (!alive) return;
        setItems(r.items);
        setState("ok");
      })
      .catch(() => alive && setState("error"));
    return () => {
      alive = false;
    };
  }, [platform, reloadKey]);

  return (
    <section
      className="card"
      style={{ "--hue": meta.hue, animationDelay: `${index * 70}ms` } as React.CSSProperties}
    >
      <header className="card-head">
        <span className="card-glyph">
          {iconOk && meta.icon ? (
            <img
              className="card-icon"
              src={meta.icon}
              alt={meta.name}
              onError={() => setIconOk(false)}
            />
          ) : (
            meta.glyph
          )}
        </span>
        <h2 className="card-name">{meta.name}</h2>
        <span className="card-count">{state === "ok" ? items.length : count}</span>
      </header>
      <div className="card-list">
        {state === "loading" && <p className="card-hint">加载中…</p>}
        {state === "error" && <p className="card-hint err">加载失败</p>}
        {state === "ok" && items.length === 0 && <p className="card-hint">暂无数据</p>}
        {state === "ok" &&
          items.map((it) => <NewsRow key={it.id} item={it} onOpen={onOpen} />)}
      </div>
    </section>
  );
}
