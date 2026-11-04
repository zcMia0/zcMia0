# zcMia0 · 界面信息清单（真实资料版）

> 采集时间：2026-11-04 15:40 (GMT+8)
> 数据源：`https://api.github.com/users/zcMia0`、`/users/zcMia0/repos`、`/repos/{repo}/git/trees/main?recursive=1`，以及三个原创仓库的 `README.md` / `requirements.txt` / `index.html` 原文。
> 这一版 README **不再有 `{{ }}` 占位符**，全部改由 `profile.json` 驱动；改完跑 `python build.py` 即可重建。

---

## 一、账号真实公开资料

| 字段 | 实际值 |
|------|--------|
| login | `zcMia0` |
| 主页 | https://github.com/zcMia0 |
| 头像 | https://avatars.githubusercontent.com/u/115552774?v=4 |
| 账号创建 | 2022-10-11 |
| 公开仓库 | 7（原创 3 + fork 4） |
| followers / following | 2 / 2 |
| 近一年贡献 | 10（GitHub 主页显示） |
| **display name** | **空（null）** |
| **bio** | **空（null）** |
| **location** | **空（null）** |
| **company / hireable** | **空（null）** |
| **blog** | **空字符串** |
| **twitter_username** | **空（null）** |
| **email** | **空（null）** |

⚠️ 关键事实：账号资料里除了用户名，几乎所有身份字段都是空的。所以界面里**没有编造姓名、城市、职业、邮箱或社交账号**，一律使用真实用户名 `zcMia0`。

## 二、仓库真实构成

原创 3 个（按最近推送排序）：

| 仓库 | 主语言 | 最近推送 | 文件构成（实测） | 说明来源 |
|------|--------|----------|------------------|----------|
| `enterprise-rag-workbench` | Python | 2026-11-04 | `.py` 47 / `.md` 58 / `.vue` 8 / `.ts` 6 / `.png` 9 / `docker-compose.yml` | README 标题「企业知识库 RAG Agent 工作台」、badges（FastAPI、Vue3、Milvus、PostgreSQL） |
| `three-stage-rag-kit` | Python | 2026-10-13 | `.py` 9 / `requirements.txt` / `README.md` | README 标题「电商场景三级检索增强生成工具包」；依赖：`rank-bm25`、`jieba`、`sentence-transformers`、`faiss-cpu`、`numpy` |
| `zcMia0.github.io` | HTML | 2022-11-10 | `.html` 11 / `.js` 3 / `.css` 2 / 字体 / `.svg` | `index.html` 的 `<title>Hexo</title>`；仓库 `has_pages=true` |

fork 4 个（未当作「我做过的项目」展示，只合并成一行「a few handy forks」）：
`fuzzDicts`、`eCommerce_Skills`、`hyperframes`、`rea`。

## 三、界面每个字段的取值与依据

| 板块 | 界面上的值 | 依据 | 性质 |
|------|-----------|------|------|
| 横幅 | `Hi, I'm zcMia0 👋` | `login` | 真实抓取 |
| 关于我 ① | `hi, i'm zcMia0 — i like making small, careful things.` | 用户名 + 3 个小仓库的规模 | 基于真实资料改写 |
| 关于我 ② | `lately i'm into RAG: retrieval, reranking, traceable answers.` | 两个 RAG 仓库的 README | 真实主题改写 |
| 关于我 ③ | `my first site is still online from 2022. never took it down.` | `zcMia0.github.io` 推送于 2022 且 Pages 在线 | 真实事实改写 |
| 🐾 语言 | Python / TypeScript / HTML + CSS / Vue | 三个仓库文件树：`.py`×56、`.ts`×6、`.html`×11、`.css`×2、`.vue`×8 | 真实抓取 |
| 🧸 工具 | Git + GitHub / Docker / FAISS · BM25 / FastAPI · Vue | `docker-compose.yml`、`requirements.txt`、workbench README badges | 真实抓取 |
| 🟧 项目 1 | `enterprise-rag-workbench` — 企业知识库 RAG 工作台：文档入库 → 带溯源的流式问答 | README 副标题 | 真实改写 |
| 🟩 项目 2 | `three-stage-rag-kit` — 电商三级检索：BM25 粗召回 → 向量语义 → 交叉编码器精排 | README「核心特性」 | 真实改写 |
| 🟨 项目 3 | `zcMia0.github.io` — 用 Hexo 搭的小小个人站点，从 2022 年挂到现在 | `<title>Hexo</title>` + 推送时间 + Pages | 真实改写 |
| 🟪 项目 4 | `a few handy forks` — fuzz 字典、逆向工具、agent 框架 | 4 个 fork 的真实名称 | 真实、已明确标注是 fork |
| 🍡 now · eating | `something sweet` | 无对应公开数据 | **软萌玩笑文案，可改** |
| 🍡 now · learning | `retrieval + reranking` | 两个 RAG 仓库主题 | 真实主题 |
| 🍡 now · building | `enterprise-rag-workbench` | 2026-11-04 有 4 个新 commit，是最近活跃仓库 | 真实抓取 |
| 底部图标 | GitHub + Blog（`https://zcMia0.github.io`） | `html_url`、Pages 在线 | 真实抓取 |
| 统计卡片 | 3 张奶油色卡片 | `username=zcMia0` | 真实用户名 |

## 四、刻意留白的地方（不编造）

- **X / Twitter 图标**：`twitter_username` 为 null → 未生成图标，避免指向错误账号。
- **Email 图标**：`email` 为 null → 未生成图标，避免 `mailto:` 指向不存在的地址。
- **display name / location / bio / company**：均为 null → 界面不写姓名、城市、职业。
- 补上这些资料后，在 `profile.json` 的 `social` 数组里加一项（图标文件 `ico-x.svg` / `ico-mail.svg` 已备好），重跑 `build.py` 即可出现。

## 五、统计卡片链接（基于真实用户名）

```
https://github-readme-stats.vercel.app/api?username=zcMia0&show_icons=true&hide_border=false&border_radius=24&include_all_commits=true&disable_animations=true&locale=en&custom_title=my%20little%20stats&title_color=B5838D&text_color=6B5A4F&icon_color=D98FA3&bg_color=FFF8F0&border_color=FFD6E0
https://github-readme-stats.vercel.app/api/top-langs/?username=zcMia0&layout=compact&langs_count=6&card_width=320&hide_border=false&border_radius=24&disable_animations=true&locale=en&custom_title=things%20i%20speak&title_color=B5838D&text_color=6B5A4F&bg_color=FFF8F0&border_color=FFD6E0
https://streak-stats.demolab.com/?user=zcMia0&hide_border=true&border_radius=24&background=FFF8F0&border=FFD6E0&stroke=F3E4D2&ring=FFD6E0&fire=E8A0B4&currStreakNum=B5838D&sideNums=6B5A4F&currStreakLabel=B5838D&sideLabels=6B5A4F&dates=A9988A&disable_animations=true&mode=daily&type=svg
```

均为 `bg_color=FFF8F0` / `border_color=FFD6E0` / `border_radius=24` 的奶油主题（非默认紫），全部关闭动画、静态渲染。

## 六、怎么改

1. 编辑 `profile.json`（唯一数据源）。
2. 本目录执行 `python build.py`，会重建 `README.md`、`assets/*.svg`、`preview.html`。
3. 换主角：`python build.py --shiba` / `--cat`；换成自己的图：`python build.py --mascot assets/mascot.png`（自动内嵌为 data URI）。
4. 推到 `zcMia0/zcMia0` 仓库的 `main` 分支，个人主页即生效。

---

## 七、上传结果（已完成并线上验收）

| 项目 | 结果 |
|------|------|
| 目标仓库 | https://github.com/zcMia0/zcMia0 —— 新建，公开 |
| 生效页面 | https://github.com/zcMia0 |
| 分支 | `main` |
| 推送方式 | `git push` 被网关切断（`Empty reply from server`），改用 GitHub REST API 整树推送 |
| 文件数 | 21（含 16 个静态 SVG） |
| tree SHA 验收 | 推送脚本每次自动比对，本地与远程文件树逐字节一致（**通过**） |
| 远程提交 | `main` 分支由 REST API 整树提交，前面有一个 `init: add .gitignore` 引导提交 |
| 线上验收 | README 与本地逐字一致（5678 字符）；主页 HTML 已渲染出 `enterprise-rag-workbench`、`little things i made`、`thanks for stopping by` |

远程比本地多一个 `init: add .gitignore` 引导提交（空仓库的 Git Data API 需要先有首个 commit），因此两边的 commit SHA 不同，但**文件树逐字节一致**，主页内容不受影响。

后续想改内容：编辑 `profile.json` → `python build.py` → `git add -A && git commit` → 跑本地 `_gh/push_via_api.py`（令牌只经 `GH_TOKEN` 环境变量传入，脚本会基于远程当前 tip 重新整树提交）。该脚本留在本地工作区，未上传进仓库。
