import { useEffect, useState } from "react";
import { getNewsDetail, type NewsDetail } from "../api";
import { platformMeta } from "../platforms";

export function DetailDrawer({ id, onClose }: { id: number | null; onClose: () => void }) {
  const [detail, setDetail] = useState<NewsDetail | null>(null);
  const [state, setState] = useState<"loading" | "ok" | "error">("loading");

  useEffect(() => {
    if (id == null) return;
    let alive = true;
    setState("loading");
    setDetail(null);
    getNewsDetail(id)
      .then((d) => {
        if (!alive) return;
        setDetail(d);
        setState("ok");
      })
      .catch(() => alive && setState("error"));
    return () => {
      alive = false;
    };
  }, [id]);

  // Esc 关闭
  useEffect(() => {
    if (id == null) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [id, onClose]);

  if (id == null) return null;

  const paragraphs = (detail?.content ?? "")
    .split("\n")
    .map((s) => s.trim())
    .filter(Boolean);
  const link = detail?.article_url || detail?.url;

  return (
    <div className="drawer-root" onClick={onClose}>
      <aside className="drawer" onClick={(e) => e.stopPropagation()}>
        <button className="drawer-close" onClick={onClose} title="关闭">
          ✕
        </button>
        {state === "loading" && <p className="card-hint">加载中…</p>}
        {state === "error" && <p className="card-hint err">加载失败</p>}
        {state === "ok" && detail && (
          <article className="detail">
            <div className="detail-tag">{platformMeta(detail.platform).name}</div>
            <h2 className="detail-title">{detail.title}</h2>
            <div className="detail-meta">
              {detail.author && <span>{detail.author}</span>}
              {detail.publish_time && <span>{detail.publish_time}</span>}
            </div>
            {paragraphs.length > 0 ? (
              <div className="detail-body">
                {paragraphs.map((p, i) => (
                  <p key={i}>{p}</p>
                ))}
              </div>
            ) : (
              <p className="card-hint">暂无正文，请查看原文</p>
            )}
            {detail.images.length > 0 && (
              <div className="detail-imgs">
                {detail.images.map((src, i) => (
                  <img key={i} src={src} alt="" loading="lazy" referrerPolicy="no-referrer" />
                ))}
              </div>
            )}
            {link && (
              <a className="btn primary detail-link" href={link} target="_blank" rel="noreferrer">
                查看原文 ↗
              </a>
            )}
          </article>
        )}
      </aside>
    </div>
  );
}
