# iKnow — AI 产品经理内容引擎

## 项目概述
面向中国互联网产品经理的 AI 内容引擎。自动采集 7 路信息源，通过 LLM 生成 5 个 PM 专属栏目的深度内容，并改写为 6 个平台的发布版本。

## 技术栈
- **后端**: FastAPI (admin/server.py), 端口 8800
- **前端**: SPA 仪表盘 (admin/static/index.html), Tailwind CSS CDN + 原生 JS
- **数据库**: SQLite (admin/iknow.db), 通过 admin/data.py 操作
- **AI**: OpenAI 兼容 API (当前用 DeepSeek)
- **部署**: Render (render.yaml)

## 目录结构
```
admin/
├── server.py          # FastAPI 后端 (16 个 API 路由 + SSE)
├── data.py            # SQLite 数据层
├── model_config.json  # 业务→模型映射配置
├── model_registry.json # 可用模型注册表
└── static/
    └── index.html     # 前端 SPA (仪表盘/流水线/内容管理/归档 4 Tab)

src/
├── pipeline.py         # 主流水线 (采集→路由→生成→多平台)
├── config.py           # 全局配置
├── model_resolver.py   # 模型解析器
├── scrapers/           # 7 路数据采集
│   ├── woshipm_scraper.py   # 🆕 人人都是产品经理 RSS
│   ├── github_scraper.py    # GitHub AI 仓库
│   ├── arxiv_scraper.py     # arXiv 论文
│   ├── hn_scraper.py        # Hacker News
│   ├── juejin_scraper.py    # 掘金 AI 文章
│   ├── v2ex_scraper.py      # V2EX 热帖
│   └── news_scraper.py      # 36kr/机器之心 (可能反爬失效)
├── generators/
│   ├── pm_prompts.py        # PM 专属 5 栏目 Prompt
│   └── content_generator.py # LLM 调用封装
├── adapters/
│   └── multi_platform.py    # 6 平台版本改写
└── images/                  # FLUX 图片生成
```

## 5 个 PM 栏目
| 栏目 key | 名称 | 定位 |
|---|---|---|
| ai_product_radar | AI产品经理岗位雷达 | 大厂AI PM岗位变化、技能需求 |
| ai_product_signal | 本周AI产品信号 | 新技术/产品对PM的影响 |
| pm_toolbox | PM AI 提效工具箱 | 可复制的Prompt/工作流/模板 |
| ai_product_deepdive | AI产品深度拆解 | 深度拆解一个AI产品 |
| pm_practice_notes | 产品实战笔记 | 精选PM实战经验萃取 |

## 多平台版本
微信公众号 / 即刻 / 小红书 / 知乎 / 脉脉 / 微信群

## API 路由
```
GET  /api/stats            - 仪表盘统计
POST /api/pipeline/run     - 启动流水线
GET  /api/pipeline/stream  - SSE 实时进度
GET  /api/contents         - 内容列表
PUT  /api/contents/{id}    - 编辑内容
GET  /api/archive/{date}   - 按日期归档
GET  /api/config           - 模型配置
```

## 环境变量 (.env)
```
LLM_API_KEY=sk-xxx        # DeepSeek API Key
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
REPLICATE_API_TOKEN=r8_xxx # FLUX 图片生成
ZHIPU_API_KEY=xxx          # 智谱 GLM (备用)
```

## 运行方式
```bash
# 本地
python3 -m uvicorn admin.server:app --host 0.0.0.0 --port 8800

# 生产 (Render)
uvicorn admin.server:app --host 0.0.0.0 --port $PORT
```

## GitHub & 部署
- **Repo**: https://github.com/flowerof001/iknow
- **Render**: https://iknow-pm-engine.onrender.com
- **Render Dashboard**: https://dashboard.render.com

## 已生成内容 (2026-06-24)
- Run #2 成功，5 篇共 16,952 字
- 输出目录: output/2026-06-24/

## 待办 / 可优化项
1. **[高]** Render 需配置 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL 环境变量才能生成
2. **[中]** news_scraper (36kr/机器之心) 可能因反爬失效，需检查或替换
3. **[中]** 前端 Markdown 预览可改用 marked.js 获得更好的表格/代码渲染
4. **[低]** 添加定时任务 (cron) 自动每日运行流水线
5. **[低]** ProductHunt 被 Cloudflare 防护，当前无法抓取
6. **[低]** V2EX 的 "ai" 节点不存在 (404)，已 fallback 到 programmer/create 节点
7. **[低]** 前端 Markdown 表格渲染比较简陋，可升级
8. **[想法]** 增加内容发布到飞书/微信的自动化
9. **[想法]** 增加用户反馈/评分机制来优化 Prompt
