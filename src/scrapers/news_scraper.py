"""AI 行业新闻爬虫 — RSS 聚合"""
from typing import Optional
import requests
import xml.etree.ElementTree as ET
import re
import html


class NewsScraper:
    """通过 RSS 聚合 AI 行业新闻"""

    # 少数派 RSS + AI 关键词过滤
    SSPAI_FEED = "https://sspai.com/feed"
    AI_KEYWORDS = [
        "AI", "人工智能", "大模型", "ChatGPT", "Claude", "GPT", "LLM",
        "机器学习", "深度学习", "Agent", "智能体", "AIGC", "Prompt",
        "Copilot", "Cursor", "Codex", "OpenAI", "DeepSeek", "Gemini",
        "RAG", "MCP", "多模态", "自动驾驶", "机器人", "具身智能",
        "Diffusion", "Sora", "Transformer", "神经网络", "大语言模型",
        "AI Agent", "Vibe Coding", "AI 编程", "AI 工具",
    ]

    def __init__(self, proxy: Optional[str] = None):
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        })
        if proxy:
            self.session.proxies = {"https": proxy}

    def _clean_html(self, text: str) -> str:
        clean = re.sub(r'<[^>]+>', '', text)
        clean = html.unescape(clean)
        return clean.strip()[:400]

    def _is_ai_related(self, title: str, desc: str) -> bool:
        # 标题包含 AI 关键词 → 直接命中
        if any(kw.lower() in title.lower() for kw in self.AI_KEYWORDS):
            return True
        # 标题包含科技/产品关键词 + 摘要包含 AI 关键词 → 命中
        tech_keywords = ["AI", "Meta", "Google", "Apple", "OpenAI", "微软", "腾讯",
                        "字节", "阿里", "模型", "智能", "代码", "编程", "开发",
                        "Copilot", "Agent", "机器人", "自动"]
        if any(kw.lower() in title.lower() for kw in tech_keywords):
            clean = self._clean_html(desc)[:300]
            return any(kw.lower() in clean.lower() for kw in self.AI_KEYWORDS)
        return False

    def fetch_sspai(self) -> list[dict]:
        """从少数派 RSS 抓取 AI 相关内容"""
        try:
            resp = self.session.get(self.SSPAI_FEED, timeout=15)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
        except Exception as e:
            print(f"[少数派] RSS 失败: {e}")
            return []

        items = root.findall(".//item")
        results = []

        for item in items[:30]:
            title_el = item.find("title")
            link_el = item.find("link")
            desc_el = item.find("description")
            pubdate_el = item.find("pubDate")
            creator_el = item.find("{http://purl.org/dc/elements/1.1/}creator")

            title = title_el.text.strip() if title_el is not None and title_el.text else ""
            link = link_el.text.strip() if link_el is not None and link_el.text else ""
            raw_desc = desc_el.text if desc_el is not None else ""

            if not title:
                continue

            summary = self._clean_html(raw_desc)

            if not self._is_ai_related(title, raw_desc):
                continue

            results.append({
                "title": title[:200],
                "summary": summary,
                "url": link,
                "author": creator_el.text if creator_el is not None else "",
                "published": pubdate_el.text if pubdate_el is not None else "",
                "source": "sspai",
            })

        return results

    def fetch_all(self) -> list[dict]:
        articles = self.fetch_sspai()
        print(f"[新闻] 少数派 AI: {len(articles)} 篇")
        return articles

    def fetch_36kr(self) -> list[dict]:
        print("[36kr] JS 渲染页面，已不可用")
        return []

    def fetch_jiqizhixin(self) -> list[dict]:
        print("[机器之心] RSS 已失效")
        return []


if __name__ == "__main__":
    s = NewsScraper()
    articles = s.fetch_all()
    print(f"\n获取 {len(articles)} 篇 AI 相关新闻")
    print("-" * 60)
    for a in articles[:10]:
        print(f"  [{a['source']}] {a['title'][:60]}")
        print(f"         {a['summary'][:80]}...")
        print()
