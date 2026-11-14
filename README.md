# 四福音书-20261114-v2.0.0-GROKstudy

> 主题：四福音书（马太 · 马可 · 路加 · 约翰）深读 ｜ 时间：2026-11-14（Asia/Taipei） ｜ 版本号：v2.0.0 ｜ GROKstudy

以欧陆改革宗 / 正统立场（圣经神学 + 圣约神学）深读四福音书的简体中文学习网站：先看全本圣经大图景，再进入每卷书的成书因果（为何写）、本质核心、内容（写了什么）、地理足迹、应用（如何活出），配以时间线、故事线、多幅「讲解图 + 实时地图」、文化 / 地域背景、对观福音比较、记忆口诀、翻转卡、填空与测验。

## 🔗 部署链接（v2.0.0，当前版本）

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/four-gospels-GROKstudy/ |
| Surge | https://four-gospels-20261114-v2-grokstudy.surge.sh |
| Netlify | https://four-gospels-20261114-v2-grokstudy.netlify.app |
| 源码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/four-gospels-GROKstudy |

## 📚 页面（13）

`index` 总览 · `bible` 全本圣经视角与圣约神学 · `history` 时间线 / 故事线 / 巴勒斯坦与耶路撒冷地图 / 希律王国 · `maps` 地图 · 历史 · 文化（v2 新增） · `matthew` · `mark` · `luke` · `john`（各含 💎 本质核心与 🗺️ 地理足迹） · `synoptic` 对观福音与受难周 · `doctrine` 十大教义主题 · `creeds` 三大信经（背诵版 + 朗读、深度对比、为何需要三个） · `memory` 记忆宫殿 / 翻转卡 / 测验 / 31 天计划 · `sources` 来源、核对与标记图例

## 🗺️ 地图系统

每张地图 = **离线讲解图**（内联 SVG，可点按地点、开关路线、播放动画）+ **实时地图**（本地打包 Leaflet 1.9.4，无 CDN）。
- 多源底图并自动回退：Esri 街道 → OSM → Esri 地形 → Esri 卫星 → OpenTopoMap → DARE 罗马帝国古地图 → 高德 → OSM-DE → Esri 国家地理 → OSM-HOT → Esri 暗色；8 秒无瓦片或连续出错即切换下一源，全部失败时保留离线讲解图。
- 进入视口前 400px 才加载（IntersectionObserver + 空闲回调）；滚轮缩放需先点按地图；支持适配视野、路线播放、拖动开关、全屏。
- 共 11 幅：罗马世界、巴勒斯坦七段足迹、耶路撒冷受难周、希律王国分封、加利利海、约帕→死海高程剖面、希律圣殿平面，以及四卷福音书各自的地理足迹。

## 🖍️ 标记图例（全站统一，可按 M 键开关）

金色粗体 + 荧光底 = 重点 ｜ 玫红实线 = 基督 / 福音核心 ｜ 紫色双线 = 圣约线索 ｜ 红色波浪线 = 难点 ｜ 青色虚线 = 术语 ｜ 粉色点线 = 记忆钩 ｜ 绿色底块 = 应用 ｜ 灰色删除线 = 误区；另有 重点 / 难点 / 圣约 / 记忆 / 应用 / 警示 / 新增 七类提示框。

## ✅ 引文原则与核对

- 经文：和合本（CUV）。
- 信经与信条（使徒信经、尼西亚信经、亚他那修信经、海德堡要理问答、比利时信条、多特信经）以及 CCI 讲道节录：**逐字取自 ccifellowship.org**，构建时断言子串、发布前再抓取现场页面逐字比对（`build/verify.py`）。
- 威斯敏斯特标准仅作辅助引用，同样逐字核对。
- 非逐字的转述一律用「」标示，不用 “ ” 冒充原文。

## 📝 更新说明（Update Notes）

- **2026-11-14（Asia/Taipei）· v2.0.0**
  - 地图：新增 `maps.html` 与 11 幅「讲解图 + 实时地图」模块；本地 Leaflet、11 个底图源自动回退、懒加载、全屏 / 播放。
  - 性能：仅粘性页眉保留 backdrop-filter；背景改为只做 transform 的「浮云」动画；滚动处理不再读取布局；IntersectionObserver 驱动目录高亮与渐显；长区块用 content-visibility；JS 全部 defer；尊重 prefers-reduced-motion；桌面端可选 Lenis 平滑滚动。
  - 内容：每卷福音书新增「💎 本质核心」（一句话 / 三根柱 / 旧约→基督→教会 / 误区对照 / 记忆链）与「🗺️ 地理足迹」；新增「地理就是神学」表、生活文化卡、钱币度量表、「一位基督 · 四重见证」动画图、受难周篇幅图、信经朗读（TTS）。
  - 标记：8 种统一行内标记 + 7 类提示框 + 图例栏，可一键关闭。
  - 核对：CCI 93/93 段与现场一致，讲道 6/6，信经 3/3，WS 7/7，正文引号 290 处 0 未匹配；Playwright 在 360 / 390 / 768 / 1024 / 1440 五种宽度 × 13 页（65/65）逐一点按目录、图例、手风琴、翻转卡、标签、地图图层、测验后无溢出、无裁切、无 JS 错误。
- **2026-10-31 15:53（Asia/Taipei）· v1.0.0**：首次发布。12 个页面；CCI 信条块 93/93 段与现场页面逐字一致，讲道节录 6/6，三大信经背诵版 3/3，WS 7/7；正文引号审计 0 未匹配；Playwright 375 / 768 / 1440 三种宽度 36/36 通过。

## 🏷️ 版本说明（Version Notes）

| 版本 | 日期（Asia/Taipei） | 链接 |
|---|---|---|
| v2.0.0 | 2026-11-14 | [Surge](https://four-gospels-20261114-v2-grokstudy.surge.sh) · [Netlify](https://four-gospels-20261114-v2-grokstudy.netlify.app) · [GitHub Pages](https://07-je-grok-love-personal-20260928.github.io/four-gospels-GROKstudy/) |
| v1.0.0 | 2026-10-31 | [Surge](https://four-gospels-20261031-v1-grokstudy.surge.sh) · [Netlify](https://four-gospels-20261031-v1-grokstudy.netlify.app) · [Release](https://github.com/07-Je-Grok-Love-Personal-20260928/four-gospels-GROKstudy/releases/tag/v1.0.0)（GitHub Pages 已更新为 v2） |

- 版本号规则：`主版本.次版本.修订`。
- 目录结构：`build/`（Python 生成器；`maps.py` 地图模块、`ess.py` 本质核心、`p_maps.py` 地图页、`palgeo.py` / `geo.py` 底图几何、`verify.py` 逐字核对）、`docs/`（静态站点，GitHub Pages 由 main 分支 `/docs` 发布；`assets/maps.js` 实时地图、`assets/vendor/` 本地 Leaflet 与 Lenis）、`tools/qa.py`（Playwright 多宽度交互质检）。
- 重建：`cd build && python3 verify.py && python3 build.py`；质检：`WIDTHS=360,390,768,1024,1440 python3 tools/qa.py`。

## ⚠️ 局限

- 讲解图依据 Natural Earth 数据绘制，古代地点与路线为大致位置（以马忤斯、格拉森等有争议）；耶路撒冷与圣殿图非比例。
- 实时地图依赖第三方瓦片服务；个别服务可能返回「需要密钥」等占位图而不报错，此时请手动切换图层。
- 成书日期、作者等学术问题列出主流改革宗 / 保守立场及其理由，并非唯一结论。
- 多媒体以 SVG / CSS 动画与浏览器朗读实现，未嵌入任何受版权保护的音视频。
