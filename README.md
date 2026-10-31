# 四福音书-20261031-v1.0.0-GROKstudy

> 主题：四福音书（马太 · 马可 · 路加 · 约翰）深读 ｜ 时间：2026-10-31（Asia/Taipei） ｜ 版本号：v1.0.0 ｜ GROKstudy

以欧陆改革宗 / 正统立场（圣经神学 + 圣约神学）深读四福音书的简体中文学习网站：先看全本圣经大图景，再进入每卷书的成书因果（为何写）、内容（写了什么）、应用（如何活出），配以时间线、故事线、巴勒斯坦地图与耶路撒冷受难周示意图、文化 / 地域背景、对观福音比较、记忆口诀、翻转卡、填空与测验。

## 🔗 部署链接

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/four-gospels-GROKstudy/ |
| Surge | https://four-gospels-20261031-v1-grokstudy.surge.sh |
| Netlify | https://four-gospels-20261031-v1-grokstudy.netlify.app |
| 源码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/four-gospels-GROKstudy |

## 📚 页面（12）

`index` 总览 · `bible` 全本圣经视角与圣约神学 · `history` 时间线 / 故事线 / 地图 / 背景 · `matthew` 马太福音 · `mark` 马可福音 · `luke` 路加福音 · `john` 约翰福音 · `synoptic` 对观福音与受难周 · `doctrine` 十大教义主题 · `creeds` 三大信经（背诵版、深度对比、为何需要三个）· `memory` 记忆宫殿 / 翻转卡 / 测验 / 31 天计划 · `sources` 来源与核对

## ✅ 引文原则与核对

- 经文：和合本（CUV）。
- 信经与信条（使徒信经、尼西亚信经、亚他那修信经、海德堡要理问答、比利时信条、多特信经）以及 CCI 讲道节录：**逐字取自 ccifellowship.org**，构建时断言子串、发布前再抓取现场页面逐字比对（`build/verify.py`）。
- 威斯敏斯特标准仅作辅助引用，同样逐字核对。
- 非逐字的转述一律用「」标示，不用 “ ” 冒充原文。

## 📝 更新说明（Update Notes）

- **2026-10-31 15:53（Asia/Taipei）· v1.0.0**：首次发布。12 个页面；CCI 信条块 93/93 段与现场页面逐字一致，讲道节录 6/6 一致，三大信经背诵版 3/3 一致，WS 7/7 一致；正文引号审计 0 未匹配；Playwright 在 375 / 768 / 1440 三种宽度下 36/36 通过（无横向溢出、无 JS 错误）。

## 🏷️ 版本说明（Version Notes）

- 版本号规则：`主版本.次版本.修订`。v1.0.0 = 首个完整公开版本。
- 目录结构：`build/`（Python 生成器）、`docs/`（静态站点，GitHub Pages 由 main 分支 `/docs` 发布）、`tools/qa.py`（Playwright 版面质检）。
- 重建：`cd build && python3 build.py && python3 verify.py && python3 build.py`。

## ⚠️ 局限

地图为根据 Natural Earth 数据绘制的示意图，古代地点与路线为大致位置；耶路撒冷图非比例。成书日期、作者等学术问题列出主流改革宗 / 保守立场及其理由，并非唯一结论。
