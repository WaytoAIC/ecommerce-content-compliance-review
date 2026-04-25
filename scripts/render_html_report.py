#!/usr/bin/env python3
"""Render an ecommerce compliance review JSON file into a portable HTML report.

The renderer intentionally uses only the Python standard library so it can run
inside Codex/OpenClaw skill folders without dependency setup.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path
from typing import Any


SEVERITY_CLASS = {
    "HIGH": "high",
    "MEDIUM": "medium",
    "LOW": "low",
    "INFO": "info",
    "PASS": "pass",
}

SEVERITY_LABEL = {
    "HIGH": "HIGH",
    "MEDIUM": "MEDIUM",
    "LOW": "LOW",
    "INFO": "INFO",
    "PASS": "PASS",
}


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def severity_class(value: Any) -> str:
    return SEVERITY_CLASS.get(str(value or "").upper(), "info")


def severity_label(value: Any) -> str:
    return SEVERITY_LABEL.get(str(value or "").upper(), esc(value or "INFO"))


def read_image_data_uri(image_path: str | None, base_dir: Path) -> str:
    if not image_path:
        return ""
    path = Path(image_path)
    if not path.is_absolute():
        path = base_dir / path
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    mime_type = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def render_meta(meta: dict[str, Any]) -> str:
    pairs = [
        ("审查平台", meta.get("platform")),
        ("目标市场", meta.get("market")),
        ("内容类型", meta.get("content_type")),
        ("产品品类", meta.get("category")),
        ("审查时间", meta.get("review_time")),
    ]
    return " · ".join(f"{label}：{esc(value)}" for label, value in pairs if value)


def render_critical_cards(points: list[dict[str, Any]]) -> str:
    if not points:
        return ""
    cards = []
    for index, point in enumerate(points, start=1):
        number = point.get("id", index)
        cards.append(
            f"""
          <div class="critical-card">
            <p><span class="num">{esc(number)}</span><strong>{esc(point.get("title"))}</strong></p>
            <p>{esc(point.get("description"))}</p>
          </div>"""
        )
    return f'<div class="critical-strip">{"".join(cards)}</div>'


def render_metrics(counts: dict[str, Any]) -> str:
    items = [
        ("HIGH", "严重风险"),
        ("MEDIUM", "中等风险"),
        ("LOW", "低风险/优化项"),
        ("INFO", "提示项"),
    ]
    cards = []
    for key, label in items:
        css = severity_class(key)
        cards.append(
            f"""
      <div class="metric">
        <b class="{css}-text">{esc(counts.get(key, 0))}</b>
        <span>{label}</span>
      </div>"""
        )
    return "".join(cards)


def render_original_content(content: dict[str, Any]) -> str:
    if not content:
        return ""
    title = content.get("title")
    bullets = as_list(content.get("bullets"))
    parts = []
    if title:
        parts.append(f"<strong>原标题：</strong>{esc(title)}")
    if bullets:
        bullet_items = "".join(f"<li>{esc(item)}</li>" for item in bullets)
        parts.append(f"<strong>原五点：</strong><ul>{bullet_items}</ul>")
    if not parts:
        return ""
    return f'<div class="quote">{"".join(parts)}</div>'


def render_image_audit(image: dict[str, Any], base_dir: Path) -> str:
    if not image or not image.get("path"):
        return ""
    data_uri = read_image_data_uri(image.get("path"), base_dir)
    hotspots = []
    for index, hotspot in enumerate(as_list(image.get("hotspots")), start=1):
        number = hotspot.get("id", index)
        label = hotspot.get("label", "")
        border = " dashed" if hotspot.get("style") == "dashed" else ""
        hotspots.append(
            f"""<div class="hotspot{border}" data-num="{esc(number)}" data-label="{esc(label)}" style="left:{float(hotspot.get("x", 0))}%;top:{float(hotspot.get("y", 0))}%;width:{float(hotspot.get("width", 10))}%;height:{float(hotspot.get("height", 10))}%;"></div>"""
        )

    notes = []
    for index, point in enumerate(as_list(image.get("notes")), start=1):
        notes.append(
            f"""
          <div class="audit-item">
            <strong>{esc(point.get("title", f"图像风险 {index}"))}</strong>
            <p>{esc(point.get("description"))}</p>
          </div>"""
        )

    if image.get("action_required"):
        notes.append(
            f"""
          <div class="audit-item action-required">
            <strong>必须整改后再上架</strong>
            <p>{esc(image.get("action_required"))}</p>
          </div>"""
        )

    return f"""
    <section class="section">
      <h2>原图审查页：关键侵权点高亮</h2>
      <div class="image-audit-layout">
        <figure class="image-frame">
          <img src="{data_uri}" alt="{esc(image.get("alt", "原始产品图"))}">
          {''.join(hotspots)}
        </figure>
        <div class="audit-list">{''.join(notes)}</div>
      </div>
    </section>"""


def render_issues(issues: list[dict[str, Any]]) -> str:
    rows = []
    for issue in issues:
        sev = str(issue.get("severity", "INFO")).upper()
        row_class = ' class="infringement"' if sev == "HIGH" else ""
        rows.append(
            f"""
          <tr{row_class}>
            <td>{esc(issue.get("location"))}</td>
            <td><span class="pill {severity_class(sev)}">{severity_label(sev)}</span></td>
            <td>{esc(issue.get("problem"))}</td>
            <td>{esc(issue.get("recommendation"))}</td>
          </tr>"""
        )
    return "".join(rows) or '<tr><td colspan="4">未发现问题。</td></tr>'


def render_rewrite(rewrite: dict[str, Any]) -> str:
    if not rewrite:
        return ""
    title = rewrite.get("title")
    bullets = as_list(rewrite.get("bullets"))
    description = rewrite.get("description")
    parts = []
    if title:
        parts.append(f"<div class=\"copybox\"><strong>建议标题</strong>{esc(title)}</div>")
    if bullets:
        bullet_items = "".join(f"<li>{esc(item)}</li>" for item in bullets)
        parts.append(f"<div class=\"copybox\"><strong>建议五点</strong><ol>{bullet_items}</ol></div>")
    if description:
        parts.append(f"<div class=\"copybox\"><strong>建议产品描述</strong>{esc(description)}</div>")
    if not parts:
        return ""
    return f"""
    <section class="section">
      <h2>合规改写版本</h2>
      <div class="rewrite">{''.join(parts)}</div>
    </section>"""


def render_image_guidelines(guidelines: dict[str, Any]) -> str:
    if not guidelines:
        return ""
    blocks = []
    labels = [("main", "主图"), ("secondary", "副图")]
    for key, label in labels:
        items = as_list(guidelines.get(key))
        if not items:
            continue
        lis = "".join(f"<li>{esc(item)}</li>" for item in items)
        blocks.append(f"<div class=\"callout\"><h3>{label}</h3><ul>{lis}</ul></div>")
    if not blocks:
        return ""
    return f"""
    <section class="section">
      <h2>图片整改底线</h2>
      <div class="two-col">{''.join(blocks)}</div>
    </section>"""


def render_checklist(checklist: list[dict[str, Any]]) -> str:
    if not checklist:
        return ""
    rows = []
    for item in checklist:
        sev = str(item.get("severity", "INFO")).upper()
        rows.append(
            f"""
          <tr>
            <td>{esc(item.get("item"))}</td>
            <td><span class="pill {severity_class(sev)}">{esc(item.get("status"))}</span></td>
            <td>{esc(item.get("pass_standard"))}</td>
          </tr>"""
        )
    return f"""
    <section class="section">
      <h2>上架前检查清单</h2>
      <table>
        <thead><tr><th>检查项</th><th>当前状态</th><th>通过标准</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>"""


def render_sources(sources: list[dict[str, Any]]) -> str:
    if not sources:
        return ""
    items = []
    for source in sources:
        label = esc(source.get("label", source.get("url", "Source")))
        url = esc(source.get("url", "#"))
        items.append(f'<li><a href="{url}">{label}</a></li>')
    return f"""
    <section class="section">
      <h2>参考依据</h2>
      <ul class="source-list">{''.join(items)}</ul>
    </section>"""


def render_html(data: dict[str, Any], base_dir: Path) -> str:
    title = data.get("title", "电商内容合规审查报告")
    meta = data.get("meta", {})
    overall = data.get("overall", {})
    level = str(overall.get("level", "INFO")).upper()
    summary = overall.get("summary", "")
    critical_points = as_list(data.get("critical_points"))

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>
    :root {{
      --ink: #1f2933;
      --muted: #667085;
      --line: #d8dee9;
      --paper: #ffffff;
      --bg: #f5f7fa;
      --danger: #b42318;
      --danger-bg: #fff1f0;
      --warn: #b54708;
      --warn-bg: #fff7ed;
      --ok: #087443;
      --ok-bg: #ecfdf3;
      --info: #175cd3;
      --info-bg: #eff6ff;
      --panel: #f8fafc;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
      line-height: 1.55;
    }}
    .page {{ width: min(1180px, calc(100% - 40px)); margin: 32px auto 56px; }}
    .hero {{
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 28px;
      display: grid;
      grid-template-columns: 1.4fr 0.8fr;
      gap: 24px;
      align-items: start;
    }}
    h1, h2, h3 {{ margin: 0; letter-spacing: 0; }}
    h1 {{ font-size: 30px; line-height: 1.22; margin-bottom: 12px; }}
    h2 {{ font-size: 21px; margin-bottom: 14px; }}
    h3 {{ font-size: 16px; margin-bottom: 8px; }}
    p {{ margin: 0 0 12px; }}
    .meta {{ color: var(--muted); font-size: 14px; }}
    .verdict {{ border: 1px solid #f0b8b2; background: var(--danger-bg); border-radius: 8px; padding: 16px; }}
    .verdict .label {{ color: var(--danger); font-size: 14px; font-weight: 700; text-transform: uppercase; }}
    .verdict .level {{ color: var(--danger); font-size: 32px; font-weight: 800; margin: 2px 0 6px; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin: 18px 0; }}
    .metric {{ background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 16px; }}
    .metric b {{ display: block; font-size: 26px; line-height: 1; margin-bottom: 6px; }}
    .metric span {{ color: var(--muted); font-size: 13px; }}
    .high-text {{ color: var(--danger); }}
    .medium-text {{ color: var(--warn); }}
    .low-text, .pass-text {{ color: var(--ok); }}
    .info-text {{ color: var(--info); }}
    .section {{ background: var(--paper); border: 1px solid var(--line); border-radius: 8px; margin-top: 18px; padding: 24px; }}
    table {{ width: 100%; border-collapse: collapse; overflow: hidden; border-radius: 8px; font-size: 14px; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 12px 10px; text-align: left; vertical-align: top; }}
    th {{ background: var(--panel); color: #344054; font-weight: 700; white-space: nowrap; }}
    tr:last-child td {{ border-bottom: 0; }}
    .pill {{ display: inline-block; border-radius: 999px; padding: 3px 10px; font-size: 12px; font-weight: 700; white-space: nowrap; }}
    .high {{ color: var(--danger); background: var(--danger-bg); border: 1px solid #f0b8b2; }}
    .medium {{ color: var(--warn); background: var(--warn-bg); border: 1px solid #fed7aa; }}
    .low, .pass {{ color: var(--ok); background: var(--ok-bg); border: 1px solid #abefc6; }}
    .info {{ color: var(--info); background: var(--info-bg); border: 1px solid #bfdbfe; }}
    .infringement {{ background: #fff1f0; box-shadow: inset 4px 0 0 var(--danger); }}
    .quote {{ background: var(--panel); border-left: 4px solid #98a2b3; border-radius: 6px; padding: 12px 14px; color: #344054; font-size: 14px; margin: 8px 0 14px; }}
    .quote strong {{ display: block; margin-bottom: 6px; }}
    .critical-strip {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: 18px; }}
    .critical-card {{ border: 1px solid #f0b8b2; background: #fff7f5; border-radius: 8px; padding: 14px; }}
    .critical-card .num {{ width: 28px; height: 28px; display: inline-grid; place-items: center; border-radius: 50%; background: var(--danger); color: #fff; font-weight: 800; margin-right: 8px; }}
    .critical-card strong {{ color: var(--danger); }}
    .image-audit-layout {{ display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr); gap: 18px; align-items: start; }}
    .image-frame {{ position: relative; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; margin: 0; }}
    .image-frame img {{ display: block; width: 100%; height: auto; }}
    .hotspot {{ position: absolute; border: 4px solid rgba(180, 35, 24, 0.92); background: rgba(255, 241, 240, 0.18); box-shadow: 0 0 0 2px rgba(255,255,255,0.88), 0 10px 28px rgba(180,35,24,0.22); border-radius: 8px; }}
    .hotspot.dashed {{ border-style: dashed; border-color: rgba(181, 71, 8, 0.92); background: transparent; }}
    .hotspot::before {{ content: attr(data-num); position: absolute; top: -16px; left: -16px; width: 34px; height: 34px; display: grid; place-items: center; border-radius: 50%; background: var(--danger); color: #fff; border: 3px solid #fff; font-weight: 800; font-size: 16px; }}
    .hotspot.dashed::before {{ background: var(--warn); }}
    .hotspot::after {{ content: attr(data-label); position: absolute; left: 8px; bottom: 8px; max-width: min(230px, calc(100% - 16px)); background: rgba(180,35,24,0.94); color: #fff; border-radius: 6px; padding: 6px 8px; font-size: 12px; font-weight: 700; line-height: 1.35; }}
    .hotspot.dashed::after {{ background: rgba(181, 71, 8, 0.96); }}
    .audit-list {{ display: grid; gap: 12px; }}
    .audit-item {{ border: 1px solid var(--line); border-radius: 8px; padding: 12px; background: #fbfcfe; }}
    .audit-item strong {{ display: block; color: var(--danger); margin-bottom: 4px; }}
    .action-required {{ background: var(--danger-bg); border-color: #f0b8b2; }}
    .rewrite {{ display: grid; gap: 12px; }}
    .copybox {{ background: #fbfcfe; border: 1px solid var(--line); border-radius: 8px; padding: 14px; }}
    .copybox strong {{ display: block; color: #344054; margin-bottom: 6px; }}
    ol, ul {{ margin: 8px 0 0 20px; padding: 0; }}
    li {{ margin: 7px 0; }}
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .callout {{ border-radius: 8px; padding: 14px 16px; border: 1px solid var(--line); background: var(--panel); }}
    .source-list a {{ color: var(--info); text-decoration: none; }}
    .source-list a:hover {{ text-decoration: underline; }}
    .footer {{ margin-top: 18px; color: var(--muted); font-size: 12px; text-align: center; }}
    @media (max-width: 860px) {{
      .page {{ width: min(100% - 24px, 1180px); margin-top: 16px; }}
      .hero, .two-col, .critical-strip, .image-audit-layout {{ grid-template-columns: 1fr; }}
      .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      h1 {{ font-size: 24px; }}
      table {{ display: block; overflow-x: auto; white-space: normal; }}
      .hotspot::after {{ max-width: 180px; font-size: 11px; }}
    }}
    @media print {{
      body {{ background: #fff; }}
      .page {{ width: 100%; margin: 0; }}
      .hero, .section, .metric {{ break-inside: avoid; border-color: #cbd5e1; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <div>
        <h1>{esc(title)}</h1>
        <p class="meta">{render_meta(meta)}</p>
        {render_original_content(data.get("original_content", {}))}
        <p>{esc(summary)}</p>
        {render_critical_cards(critical_points)}
      </div>
      <aside class="verdict">
        <div class="label">Overall Risk</div>
        <div class="level">{esc(level)}</div>
        <p>{esc(overall.get("action", ""))}</p>
      </aside>
    </section>

    <section class="grid" aria-label="风险统计">
      {render_metrics(data.get("risk_counts", {}))}
    </section>

    {render_image_audit(data.get("image", {}), base_dir)}

    <section class="section">
      <h2>风险明细</h2>
      <table>
        <thead><tr><th>位置</th><th>等级</th><th>问题</th><th>整改建议</th></tr></thead>
        <tbody>{render_issues(as_list(data.get("issues")))}</tbody>
      </table>
    </section>

    {render_rewrite(data.get("rewrite", {}))}
    {render_image_guidelines(data.get("image_guidelines", {}))}
    {render_checklist(as_list(data.get("checklist")))}
    {render_sources(as_list(data.get("sources")))}

    <p class="footer">{esc(data.get("footer", "Generated for internal compliance review. This report is operational guidance, not legal advice."))}</p>
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a compliance review JSON file into HTML.")
    parser.add_argument("input_json", help="Path to the report JSON file")
    parser.add_argument("-o", "--output", help="Output HTML path")
    args = parser.parse_args()

    input_path = Path(args.input_json).resolve()
    data = json.loads(input_path.read_text(encoding="utf-8"))
    output_path = Path(args.output).resolve() if args.output else input_path.with_suffix(".html")
    output_path.write_text(render_html(data, input_path.parent), encoding="utf-8")
    print(f"Wrote HTML report: {output_path}")


if __name__ == "__main__":
    main()
