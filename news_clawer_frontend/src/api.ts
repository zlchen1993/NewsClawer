// 后端接口封装（开发时经 Vite 代理到 :8000）

export interface PlatformInfo {
  platform: string;
  latest_date: string | null;
  count: number;
}

export interface NewsBrief {
  id: number;
  platform: string;
  news_id: string;
  title: string;
  url: string;
  rank: number | null;
  hot_value: string | null;
  cover_image: string | null;
  author: string | null;
  publish_time: string | null;
}

export interface NewsDetail extends NewsBrief {
  article_url: string | null;
  content: string | null;
  images: string[];
  crawl_time: string | null;
}

export interface NewsListResponse {
  platform: string;
  date: string | null;
  total: number;
  page: number;
  page_size: number;
  items: NewsBrief[];
}

async function getJSON<T>(url: string): Promise<T> {
  const resp = await fetch(url, { headers: { Accept: "application/json" } });
  if (!resp.ok) {
    throw new Error(`请求失败 ${resp.status}`);
  }
  return resp.json() as Promise<T>;
}

export function getPlatforms(): Promise<PlatformInfo[]> {
  return getJSON<PlatformInfo[]>("/api/platforms");
}

export function getNews(
  platform: string,
  opts: { sort?: "rank" | "hot"; pageSize?: number } = {}
): Promise<NewsListResponse> {
  const params = new URLSearchParams({
    platform,
    sort: opts.sort ?? "rank",
    page_size: String(opts.pageSize ?? 100),
  });
  return getJSON<NewsListResponse>(`/api/news?${params.toString()}`);
}

export function getNewsDetail(id: number): Promise<NewsDetail> {
  return getJSON<NewsDetail>(`/api/news/${id}`);
}

export interface CrawlAccepted {
  status: string;
  platforms: string[];
}

// 触发后台爬取：不传 platform = 全部平台。返回 202，数据稍后就绪。
export function triggerCrawl(platform?: string): Promise<CrawlAccepted> {
  return fetch("/api/crawl", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(platform ? { platform } : {}),
  }).then((r) => {
    if (!r.ok) throw new Error(`触发失败 ${r.status}`);
    return r.json() as Promise<CrawlAccepted>;
  });
}
