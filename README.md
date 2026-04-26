# ecommerce-content-compliance-review

## Way to AIC | 通往AI电商之路

Fixed README prefix for Way to AIC repositories.

- 官网 / Website: [waytoaic.com](https://waytoaic.com) | [www.waytoaic.com](https://www.waytoaic.com)
- 社群招募 / Community: `Way to AIC社群招募 | WaytoAIC.com`
- 公众号 / WeChat Official Account: `维正 WaytoAIC`
- 知识星球 / Xiaozhixing: `AI电商之路 WaytoAIC`
- AIC = `AI Commerce`

在 AI 重塑商业的时代，我们希望和每一个拥抱 AI 的卖家，找到场景，定义问题，积累能力，设计系统，共同通往 AI 电商之路。

Way to AIC 不是教学，不是工具，而是一条所有电商人共同走的进化之路。

后续 Way to AIC 相关 GitHub 项目，默认都应在 README 顶部保留这一前缀区块。

### WaytoAIC 理念 | Principles

| 中文 | English |
|---|---|
| 场景先于方法 | Context before method |
| AI 的价值来自真实业务场景，而不是技术本身。 | AI creates value through real business contexts, not through technology alone. |
| 问题先于答案 | Problem before answer |
| 定义问题，比拥有工具更重要。 | Defining the problem matters more than collecting tools. |
| 系统胜过技巧 | System over tricks |
| 技巧是术，系统才是道，决定卖家的上限。 | Tricks are tactical; systems define long-term leverage and ceiling. |
| 共创优于独行 | Co-creation over solo progress |
| 我们相信，真正的进化发生在共同探索的过程中。 | Real evolution happens through shared exploration. |

---

中文 | [English](#english)

## Quick Install

```bash
# Codex
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/ecommerce-content-compliance-review/main/install.sh | bash -s -- --target codex
```

```bash
# OpenClaw
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/ecommerce-content-compliance-review/main/install.sh | bash -s -- --target openclaw
```

```bash
# Version-pinned
curl -fsSL https://raw.githubusercontent.com/WaytoAIC/ecommerce-content-compliance-review/v1.0.0/install.sh | bash -s -- --target codex --ref v1.0.0 --repo WaytoAIC/ecommerce-content-compliance-review
```

复制即用。安装后重启 Codex / OpenClaw。

---

一个面向跨境电商卖家的内容合规审查 skill，用来检查标题、五点描述、详情页文案、广告图文、搜索词与品牌故事中的违规风险。

它默认按 Amazon 美国站标准审查，也支持 eBay、Shopee、Lazada、Shopify、Temu、Walmart 等平台场景。

## 中文

### 这个 skill 会帮你做什么

- 审查标题、五点描述、产品描述、图片文案、后台关键词
- 扫描知识产权、广告法、平台政策、跨境法规四类风险
- 标注风险等级、问题定位、修改建议和合规重写版本
- 在用户只想快速判断时输出精简版高风险清单
- 在完整报告中额外生成可直接打开的 HTML 审查页，支持原图热点框高亮侵权点

### 它覆盖的重点风险

- 商标、版权、专利和品牌暗示相关风险
- 绝对化用语、虚假宣传、医疗功效和价格欺诈风险
- Amazon、eBay、Shopee、Lazada 等平台政策风险
- 认证、儿童安全、隐私、出口管制和特殊品类监管风险

### 仓库内容

- 主 skill 入口：[SKILL.md](./SKILL.md)
- UI 元数据：[agents/openai.yaml](./agents/openai.yaml)
- 审查报告模板：[assets/report-template.md](./assets/report-template.md)
- HTML 报告数据模板：[assets/html-report-data-template.json](./assets/html-report-data-template.json)
- 风险检查清单：[assets/risk-checklist.md](./assets/risk-checklist.md)
- HTML 报告渲染脚本：[scripts/render_html_report.py](./scripts/render_html_report.py)
- 广告法参考：[references/advertising-law.md](./references/advertising-law.md)
- 跨境法规参考：[references/cross-border-regulations.md](./references/cross-border-regulations.md)
- 商标与知识产权参考：[references/ip-trademark.md](./references/ip-trademark.md)
- 平台政策参考：[references/platform-policies.md](./references/platform-policies.md)
- 敏感词参考：[references/sensitive-words.md](./references/sensitive-words.md)

### 推荐使用方式

直接在 Codex 里说：

- `用 $ecommerce-content-compliance-review 审查这段 Amazon 标题有没有违规风险`
- `帮我快速检查这组五点描述，按美国站标准看`
- `按 Shopee 东南亚规则审查这段广告文案，并给我合规改写版`
- `检查这组 search terms 是否涉及商标侵权或平台违规`
- `把这张主图里的关键侵权点高亮标出，并额外输出 HTML 报告`

### HTML 报告

完整审查可额外输出 `*-compliance-review.html`。有图片时，报告会加入「原图审查页」，用编号热点框标出商标、版权、IP 外观、售卖范围混淆等风险点。

也可以手动用标准库脚本渲染：

```bash
python3 scripts/render_html_report.py report-data.json -o product-compliance-review.html
```

带图报告建议强制自测：

```bash
python3 scripts/render_html_report.py report-data.json -o product-compliance-review.html --require-image-audit
```

### 许可说明

- 当前仓库是公开可见、可学习和可使用的 `source-available` 仓库
- 默认不允许商用
- 如果你基于本仓库进行修改、二次分发或合并进更大的功能并对外提供，需要公开对应源码

---

## English

This skill reviews ecommerce copy for compliance risk across product titles, bullet points, long descriptions, image copy, backend search terms, and brand-story content.

It defaults to Amazon US review standards when the user does not specify a platform, while also supporting common cross-border marketplace contexts such as eBay, Shopee, Lazada, Shopify, Temu, and Walmart.

### What it helps with

- reviewing listing titles, bullets, descriptions, image copy, and keywords
- scanning IP, advertising, platform-policy, and cross-border regulatory risks
- returning issue severity, exact problem locations, rewrite suggestions, and compliant replacements
- supporting both full reports and quick high-risk checks
- producing a standalone HTML companion report with image hotspots for visual IP/policy risks

### Included files

- Main skill entry: [SKILL.md](./SKILL.md)
- UI metadata: [agents/openai.yaml](./agents/openai.yaml)
- Report template: [assets/report-template.md](./assets/report-template.md)
- HTML report data template: [assets/html-report-data-template.json](./assets/html-report-data-template.json)
- Risk checklist: [assets/risk-checklist.md](./assets/risk-checklist.md)
- HTML report renderer: [scripts/render_html_report.py](./scripts/render_html_report.py)
- Advertising-law reference: [references/advertising-law.md](./references/advertising-law.md)
- Cross-border regulations reference: [references/cross-border-regulations.md](./references/cross-border-regulations.md)
- IP and trademark reference: [references/ip-trademark.md](./references/ip-trademark.md)
- Platform-policy reference: [references/platform-policies.md](./references/platform-policies.md)
- Sensitive-words reference: [references/sensitive-words.md](./references/sensitive-words.md)

### Suggested prompts

- `Use $ecommerce-content-compliance-review to review this Amazon listing title for compliance risk.`
- `Use $ecommerce-content-compliance-review to quickly check these bullet points for US marketplace violations.`
- `Use $ecommerce-content-compliance-review to review this Shopee ad copy and rewrite it into a safer version.`
- `Use $ecommerce-content-compliance-review to check whether these backend keywords create trademark or policy risk.`
- `Use $ecommerce-content-compliance-review to highlight the key infringement points in this main image and generate an HTML report.`

### HTML companion reports

Full reviews can include a standalone `*-compliance-review.html` file. When an image is involved, the report can embed the source image and draw numbered hotspots around trademark, copyright, IP-lookalike, or misleading product-scope risks.

The bundled renderer uses only the Python standard library:

```bash
python3 scripts/render_html_report.py report-data.json -o product-compliance-review.html
```

For image-based reports, force the built-in validation:

```bash
python3 scripts/render_html_report.py report-data.json -o product-compliance-review.html --require-image-audit
```

### License note

- This repository is public and source-available
- Commercial use is not allowed by default
- Public redistribution or derivative distribution must keep the same license set and publish the corresponding source code
