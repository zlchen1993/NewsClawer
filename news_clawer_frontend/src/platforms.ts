// 平台 key → 展示名/图标/标记。后端只给 key，这里做中文名、网站图标与配色点缀映射。

interface PlatformMeta {
  name: string;
  glyph: string; // 图标加载失败时的兜底角标
  icon?: string; // 网站图标（public 路径）
  hue: number; // 卡头点缀色相
}

const META: Record<string, PlatformMeta> = {
  toutiao: { name: "今日头条", glyph: "头", icon: "/icons/toutiao.ico", hue: 8 },
  tencent: { name: "腾讯新闻", glyph: "腾", icon: "/icons/tencent.ico", hue: 210 },
  pengpai: { name: "澎湃新闻", glyph: "澎", icon: "/icons/pengpai.ico", hue: 18 },
  weibo: { name: "新浪微博", glyph: "微", icon: "/icons/weibo.ico", hue: 30 },
  sina: { name: "新浪新闻", glyph: "新", icon: "/icons/sina.ico", hue: 2 },
  linuxdo: { name: "LINUX DO", glyph: "L", icon: "/icons/linuxdo.svg", hue: 45 },
};

export function platformMeta(key: string): PlatformMeta {
  return META[key] ?? { name: key, glyph: key.slice(0, 1).toUpperCase(), hue: 32 };
}
