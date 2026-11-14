# 四福音书-20261114-v2.1.1-GROKstudy

> 主题：四福音书（马太 · 马可 · 路加 · 约翰）深读 ｜ 时间：2026-11-14（Asia/Taipei） ｜ 版本号：v2.1.1 ｜ GROKstudy

以欧陆改革宗 / 正统立场（圣经神学 + 圣约神学）深读四福音书的简体中文学习网站：先看全本圣经大图景，再进入每卷书的成书因果（为何写）、本质核心、内容（写了什么）、地理足迹、应用（如何活出），配以时间线、故事线、多幅「讲解图 + 实时地图」、文化 / 地域背景、对观福音比较、记忆口诀、翻转卡、填空与测验。

## 🔗 部署链接（v2.1.1，当前版本）

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/four-gospels-GROKstudy/ |
| Surge | https://four-gospels-20261114-v2-1-1-grokstudy.surge.sh |
| Netlify | https://four-gospels-20261114-v2-1-1-grokstudy.netlify.app |
| 源码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/four-gospels-GROKstudy |
| 固定版本 | https://github.com/07-Je-Grok-Love-Personal-20260928/four-gospels-GROKstudy/releases/tag/v2.1.1 |

## 📚 页面（13）

`index` 总览 · `bible` 全本圣经视角与圣约神学 · `history` 时间线 / 故事线 / 巴勒斯坦与耶路撒冷地图 / 希律王国 · `maps` 地图 · 历史 · 文化（v2 新增） · `matthew` · `mark` · `luke` · `john`（各含 💎 本质核心与 🗺️ 地理足迹） · `synoptic` 对观福音与受难周 · `doctrine` 十大教义主题 · `creeds` 三大信经（背诵版 + 朗读、深度对比、为何需要三个） · `memory` 记忆宫殿 / 翻转卡 / 测验 / 31 天计划 · `sources` 来源、核对与标记图例

## 📑 目录（v2.1.x）

三级目录：`h2 → 一级（编号 一、二、…）`、`h3 → 二级`、`h4 → 三级`；每级可展开 / 折叠（另有「全部展开 / 只看一级 / 展开到二级」）；目录打开时可**拖动右边缘自由调宽**（220px～屏宽 60%，平板抽屉最宽 92%，鼠标 / 触控 / 键盘 ←→ 均可，双击复原，宽度存 localStorage）；长标题自动换行。手机为抽屉式目录。

## 🗺️ 地图系统

每张地图 = **离线讲解图**（内联 SVG，可点按地点、开关路线、播放动画）+ **实时地图**（本地打包 Leaflet 1.9.4，无 CDN）。
- **17 个实测底图**（2026-11-14 从服务器逐一请求耶路撒冷 z6/z9/z12 瓦片核对）：Esri 街道 / 地形 / 国家地理 / 卫星 / 自然地貌 / 山体晕渲 / 浅灰 / 夜色、OpenStreetMap、OpenTopoMap、DARE 罗马帝国古地图、CyclOSM、OSM 法国 / 德国 / 人道主义镜像、ÖPNV、高德（大陆网络备用）。已剔除返回「API KEY REQUIRED」占位图的 CARTO、Stadia、Thunderforest，以及拒绝外站调用（403）的 Wikimedia、Mapy.cz；各源设定原生最大缩放，避免「Map data not yet available」占位图。
- 打开地图时**并行测速**（每源 1 张瓦片、6 秒超时、会话缓存 30 分钟），按钮显示绿点 / 红点，自动选用连得上的源；中途 8 秒无瓦片或连续出错再切换；全部失败时保留离线讲解图。
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

- **2026-11-14 16:40（Asia/Taipei）· v2.1.1**
  - 结构：首页（四卷 / 怎样学 / 标记）、对观页（理论 · 篇幅图 · 逐日 · 十架七言 · 显现 · 证据）、记忆页（骨架 / 主动回忆 / 长期记忆）补齐二级目录。
  - 跳转：目录、页内锚点（地图总览卡片）与带 `#` 打开的链接改为「立即定位 + 逐帧校正」，屏幕外区块高度变化后仍精确落在标题处。
  - 地图性能：实时地图初始化拆成多个短任务、滚动进行中不初始化（停下后空闲执行）、页面空闲 4 秒后预载 Leaflet。
  - 性能实测（Playwright，390px 手机 + 4× CPU 降速，5 个代表页各滚动 8 秒）：滚动期间长任务 v2.0.0 共 4 个 / 388 ms → v2.1.1 共 1 个 / 67 ms（v2.1.0 地图页一度回升到 8 个 / 734 ms，本版修复）；>50 ms 掉帧 4 → 1；桌面 1440px 掉帧 1 → 0，平均帧率 58.9–60 fps。Lighthouse 移动端 97–100、桌面 100，CLS 0。
  - 核对与质检：CCI 信条 93/93 段与现场页面逐字一致，讲道 6/6，三大信经 3/3，WS 7/7，正文引号 0 未匹配；Playwright 360 / 390 / 768 / 1024 / 1440 × 13 页 = 65/65 通过（含目录全部展开 / 只看一级 / 展开到二级、逐个折叠按钮、拖宽 / 拖窄 / 双击复原、地图 17 底图切换、全屏），0 溢出 / 裁切 / 重叠 / JS 错误；断网回退测试 3/3（讲解图照常显示并提示）。
- **2026-11-14 15:54（Asia/Taipei）· v2.1.0**
  - 目录：三级可折叠目录（一级编号）、拖动调宽并记忆、长标题换行；各页标题层级重整（如每卷福音书 7 个一级 → 背景 / 地理 / 结构 / 神学 / 信条 / 应用，下设二、三级）。
  - 内容：每页顶部「⚡ 30 秒抓核心」；四卷「地理节奏条」（一章一格）；地图页新增「步行距离图」「节期轮（七个节期在基督里的应验）」；历史页新增「权力金字塔」；教义页十大主题归为四组；精简个别措辞，修正篇幅与钥字的前后一致。
  - 地图：17 个实测可用底图 + 并行测速自动选源 + 健康指示；剔除需密钥 / 占位图来源。
  - 性能：屏幕外与滚动进行中暂停需要重绘的装饰动画；进度条改为 CSS scroll-timeline；脚本执行时不再强制同步布局（改用 ResizeObserver）；触屏设备顶栏不做逐帧模糊；地图模块 content-visibility；目录跳转二次校正落点。
  - 视觉：一级标题编号徽章与多色渐变、二级标题色条、更丰富的配色。
  - 核对与质检：CCI 93/93、讲道 6/6、信经 3/3、WS 7/7；Playwright 65/65；断网回退 3/3（见 Release v2.1.0）。
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
| v2.1.1（当前） | 2026-11-14 | [Surge](https://four-gospels-20261114-v2-1-1-grokstudy.surge.sh) · [Netlify](https://four-gospels-20261114-v2-1-1-grokstudy.netlify.app) · [GitHub Pages](https://07-je-grok-love-personal-20260928.github.io/four-gospels-GROKstudy/) · [Release](https://github.com/07-Je-Grok-Love-Personal-20260928/four-gospels-GROKstudy/releases/tag/v2.1.1) |
| v2.1.0 | 2026-11-14 | [Surge](https://four-gospels-20261114-v2-1-grokstudy.surge.sh) · [Netlify](https://four-gospels-20261114-v2-1-grokstudy.netlify.app) · [Release](https://github.com/07-Je-Grok-Love-Personal-20260928/four-gospels-GROKstudy/releases/tag/v2.1.0)（GitHub Pages 已更新为 v2.1.1） |
| v2.0.0 | 2026-11-14 | [Surge](https://four-gospels-20261114-v2-grokstudy.surge.sh) · [Netlify](https://four-gospels-20261114-v2-grokstudy.netlify.app) · [Release](https://github.com/07-Je-Grok-Love-Personal-20260928/four-gospels-GROKstudy/releases/tag/v2.0.0)（GitHub Pages 已更新为 v2.1.1） |
| v1.0.0 | 2026-10-31 | [Surge](https://four-gospels-20261031-v1-grokstudy.surge.sh) · [Netlify](https://four-gospels-20261031-v1-grokstudy.netlify.app) · [Release](https://github.com/07-Je-Grok-Love-Personal-20260928/four-gospels-GROKstudy/releases/tag/v1.0.0)（GitHub Pages 已更新为 v2.1.1） |

- 版本号规则：`主版本.次版本.修订`。
- 目录结构：`build/`（Python 生成器；`maps.py` 地图模块、`ess.py` 本质核心、`p_maps.py` 地图页、`palgeo.py` / `geo.py` 底图几何、`verify.py` 逐字核对）、`docs/`（静态站点，GitHub Pages 由 main 分支 `/docs` 发布；`assets/maps.js` 实时地图、`assets/vendor/` 本地 Leaflet 与 Lenis）、`tools/qa.py`（Playwright 多宽度交互质检）。
- 重建：`cd build && python3 verify.py && python3 build.py`；质检：`WIDTHS=360,390,768,1024,1440 python3 tools/qa.py`（含目录逐级展开 / 折叠与拖动调宽）；断网回退：`python3 tools/offline.py`；性能：`python3 tools/perf.py <标签> [站点目录]`（Playwright 滚动帧率 / 长任务 + Lighthouse 移动 / 桌面）。

## ⚠️ 局限

- 讲解图依据 Natural Earth 数据绘制，古代地点与路线为大致位置（以马忤斯、格拉森等有争议）；耶路撒冷与圣殿图非比例。
- 实时地图依赖第三方瓦片服务；本版已剔除已知占位图来源并加入测速，但第三方服务今后仍可能变更政策，届时可手动切换图层（离线讲解图不受影响）。
- 成书日期、作者等学术问题列出主流改革宗 / 保守立场及其理由，并非唯一结论。
- 多媒体以 SVG / CSS 动画与浏览器朗读实现，未嵌入任何受版权保护的音视频。
