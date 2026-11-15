"""Static SVG charts styled for arunima811.github.io (light theme, no JavaScript).

Marks follow the dataviz spec: columns <= 24px with 4px rounded data-ends, 2px lines,
end dots r=4 with a 2px surface ring, hairline solid gridlines, selective labels,
native <title> tooltips on hit targets at least 24px wide.
"""
from html import escape
import math

SURFACE = "#ffffff"
INK = "#1b1b1b"
MUTED = "#6b6b6b"
AXIS = "#898781"
GRID = "#ececec"
BASELINE = "#c3c2b7"
BAND = "#f4f7fb"
BLUE = "#2a78d6"
BLUE_LIGHT = "#86b6ef"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
GRAY = "#c3c2b7"
SANS = "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

W, H = 640, 250
LEFT, RIGHT, TOP, BOTTOM = 52, 16, 36, 30


def compact(v: float) -> str:
    for size, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(v) >= size:
            text = f"{v / size:.1f}".rstrip("0").rstrip(".")
            return f"{text}{suffix}"
    return f"{v:,.0f}" if v >= 10 or v == 0 else f"{v:.1f}"


def nice_ticks(vmax: float, count: int = 4) -> list[float]:
    if vmax <= 0:
        return [0, 1]
    raw = vmax / count
    magnitude = 10 ** math.floor(math.log10(raw))
    step = next(m * magnitude for m in (1, 2, 2.5, 5, 10) if m * magnitude >= raw)
    return [i * step for i in range(int(math.ceil(vmax / step)) + 1)]


def _frame(inner: str, label: str, height: int = H) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" '
        f'role="img" aria-label="{escape(label)}" font-family="{SANS}">'
        f'<rect width="{W}" height="{height}" fill="{SURFACE}"/>{inner}</svg>'
    )


def _y_axis(ticks: list[float], y, fmt) -> str:
    parts = []
    for t in ticks:
        parts.append(f'<line x1="{LEFT}" x2="{W - RIGHT}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="{GRID if t else BASELINE}" stroke-width="1"/>')
        parts.append(f'<text x="{LEFT - 8}" y="{y(t) + 4:.1f}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{AXIS}">{escape(fmt(t))}</text>')
    return "".join(parts)


def _column(x: float, y_top: float, y_base: float, width: float, fill: str) -> str:
    height = y_base - y_top
    if height <= 0:
        return ""
    r = min(4.0, width / 2, height)
    return (
        f'<path d="M{x:.1f},{y_base:.1f} V{y_top + r:.1f} Q{x:.1f},{y_top:.1f} {x + r:.1f},{y_top:.1f} '
        f'H{x + width - r:.1f} Q{x + width:.1f},{y_top:.1f} {x + width:.1f},{y_top + r:.1f} V{y_base:.1f} Z" fill="{fill}"/>'
    )


def _band(x0: float, x1: float, label: str) -> str:
    return (
        f'<rect x="{x0:.1f}" y="{TOP - 16}" width="{x1 - x0:.1f}" height="{H - BOTTOM - TOP + 16}" fill="{BAND}"/>'
        f'<text x="{x0 + 6:.1f}" y="{TOP - 5}" font-size="11" fill="{MUTED}">{escape(label)}</text>'
    )


def _legend(items: list[tuple[str, str]], x: float = LEFT, y: float = 12) -> str:
    parts, cursor = [], x
    for name, color in items:
        parts.append(f'<rect x="{cursor:.1f}" y="{y - 8}" width="10" height="10" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{cursor + 14:.1f}" y="{y + 1}" font-size="11" fill="{MUTED}">{escape(name)}</text>')
        cursor += 14 + 6.6 * len(name) + 16
    return "".join(parts)


def column_chart(points, *, label, fmt=compact, band_from=None, band_label="", legend=None, value_labels=(), tick_every=1):
    """points: dicts with x (axis label), value, color, tip."""
    ticks = nice_ticks(max(p["value"] for p in points))
    top = ticks[-1]
    plot_h = H - TOP - BOTTOM
    y = lambda v: TOP + plot_h * (1 - v / top)
    slot = (W - LEFT - RIGHT) / len(points)
    bar_w = min(24.0, slot * 0.62)
    xs = [LEFT + slot * i + (slot - bar_w) / 2 for i in range(len(points))]

    parts = []
    if band_from is not None:
        i = next(k for k, p in enumerate(points) if p["x"] == band_from)
        parts.append(_band(LEFT + slot * i, W - RIGHT, band_label))
    parts.append(_y_axis(ticks, y, fmt))
    for i, p in enumerate(points):
        parts.append(_column(xs[i], y(p["value"]), y(0), bar_w, p["color"]))
        if i % tick_every == 0:
            parts.append(f'<text x="{xs[i] + bar_w / 2:.1f}" y="{H - BOTTOM + 16}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{AXIS}">{escape(str(p.get("tick", p["x"])))}</text>')
        if p["x"] in value_labels:
            parts.append(f'<text x="{xs[i] + bar_w / 2:.1f}" y="{y(p["value"]) - 6:.1f}" text-anchor="middle" font-size="11" font-weight="600" fill="{INK}">{escape(fmt(p["value"]))}</text>')
        parts.append(f'<rect x="{LEFT + slot * i:.1f}" y="{TOP}" width="{max(slot, 24):.1f}" height="{plot_h}" fill="transparent"><title>{escape(p["tip"])}</title></rect>')
    if legend:
        parts.append(_legend(legend))
    return _frame("".join(parts), label)


def line_chart(points, *, label, fmt=compact, band_from=None, band_label="", end_label=True, y_min_zero=True):
    """points: dicts with x (axis label), value, tip. One series."""
    values = [p["value"] for p in points]
    ticks = nice_ticks(max(values))
    top = ticks[-1]
    plot_h = H - TOP - BOTTOM
    y = lambda v: TOP + plot_h * (1 - v / top)
    slot = (W - LEFT - RIGHT - 40) / max(1, len(points) - 1)
    xs = [LEFT + 12 + slot * i for i in range(len(points))]

    parts = []
    if band_from is not None:
        i = next(k for k, p in enumerate(points) if p["x"] == band_from)
        parts.append(_band(xs[i] - slot / 2, W - RIGHT, band_label))
    parts.append(_y_axis(ticks, y, fmt))
    path = " ".join(f"{'M' if i == 0 else 'L'}{xs[i]:.1f},{y(v):.1f}" for i, v in enumerate(values))
    parts.append(f'<path d="{path}" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    step = max(1, math.ceil(len(points) / 12))
    for i, p in enumerate(points):
        if i % step == 0 or i == len(points) - 1:
            parts.append(f'<text x="{xs[i]:.1f}" y="{H - BOTTOM + 16}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{AXIS}">{escape(str(p["x"]))}</text>')
        parts.append(f'<rect x="{xs[i] - max(slot, 24) / 2:.1f}" y="{TOP}" width="{max(slot, 24):.1f}" height="{plot_h}" fill="transparent"><title>{escape(p["tip"])}</title></rect>')
    last_x, last_y = xs[-1], y(values[-1])
    parts.append(f'<circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="6" fill="{SURFACE}"/><circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="4" fill="{BLUE}"/>')
    if end_label:
        parts.append(f'<text x="{last_x + 9:.1f}" y="{last_y + 4:.1f}" font-size="11" font-weight="600" fill="{INK}">{escape(fmt(values[-1]))}</text>')
    return _frame("".join(parts), label)


def time_line_chart(points, *, label, fmt=compact, x_ticks, band_from=None, band_label="", width=W):
    """points: dicts with x (number, e.g. 2012.9), value, tip. x is placed proportionally on the time axis."""
    values = [p["value"] for p in points]
    ticks = nice_ticks(max(values))
    top = ticks[-1]
    plot_h = H - TOP - BOTTOM
    x0, x1 = x_ticks[0], x_ticks[-1]
    sx = lambda x: LEFT + 8 + (width - LEFT - RIGHT - 52) * (x - x0) / (x1 - x0)
    y = lambda v: TOP + plot_h * (1 - v / top)

    parts = []
    if band_from is not None:
        parts.append(_band(sx(band_from), width - RIGHT, band_label))
    parts.append(_y_axis(ticks, y, fmt))
    for t in x_ticks:
        parts.append(f'<text x="{sx(t):.1f}" y="{H - BOTTOM + 16}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{AXIS}">{t}</text>')
    path = " ".join(f"{'M' if i == 0 else 'L'}{sx(p['x']):.1f},{y(p['value']):.1f}" for i, p in enumerate(points))
    parts.append(f'<path d="{path}" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for p in points:
        cx, cy = sx(p["x"]), y(p["value"])
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="{BLUE}" stroke="{SURFACE}" stroke-width="2"/>')
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="12" fill="transparent"><title>{escape(p["tip"])}</title></circle>')
    last = points[-1]
    parts.append(f'<text x="{sx(last["x"]) + 10:.1f}" y="{y(last["value"]) + 4:.1f}" font-size="11" font-weight="600" fill="{INK}">{escape(fmt(last["value"]))}</text>')
    return _frame("".join(parts), label)


def stacked_columns(xs_labels, series, *, label, fmt=compact, tick_every=1):
    """series: list of (name, color, values) stacked bottom-up; 2px surface gap between segments."""
    totals = [sum(s[2][i] for s in series) for i in range(len(xs_labels))]
    ticks = nice_ticks(max(totals))
    top = ticks[-1]
    plot_h = H - TOP - BOTTOM
    y = lambda v: TOP + plot_h * (1 - v / top)
    slot = (W - LEFT - RIGHT) / len(xs_labels)
    bar_w = min(24.0, slot * 0.7)

    parts = [_y_axis(ticks, y, fmt)]
    for i, x_label in enumerate(xs_labels):
        x = LEFT + slot * i + (slot - bar_w) / 2
        base = 0.0
        visible = [(name, color, vals[i]) for name, color, vals in series if vals[i] > 0]
        for k, (name, color, v) in enumerate(visible):
            y0, y1 = y(base), y(base + v)
            gap = 2 if k > 0 else 0
            if k == len(visible) - 1:
                parts.append(_column(x, y1, y0 - gap, bar_w, color))
            elif y0 - gap - y1 > 0:
                parts.append(f'<rect x="{x:.1f}" y="{y1:.1f}" width="{bar_w:.1f}" height="{y0 - gap - y1:.1f}" fill="{color}"/>')
            base += v
        if i % tick_every == 0 or i == len(xs_labels) - 1:
            parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{H - BOTTOM + 16}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{AXIS}">{escape(x_label)}</text>')
        tip = f"{x_label}: " + ", ".join(f"{name} {fmt(vals[i])}" for name, _, vals in series if vals[i] > 0) + f" (total {fmt(totals[i])})"
        parts.append(f'<rect x="{LEFT + slot * i:.1f}" y="{TOP}" width="{max(slot, 24):.1f}" height="{plot_h}" fill="transparent"><title>{escape(tip)}</title></rect>')
    parts.append(_legend([(name, color) for name, color, _ in series]))
    return _frame("".join(parts), label)


def hbar_chart(items, *, label, fmt=compact):
    """items: dicts with name, value, tip. One series, sorted as given; value labels at the bar tips."""
    row, name_w = 30, 120
    height = TOP - 16 + row * len(items) + 8
    vmax = max(i["value"] for i in items)
    sx = lambda v: (W - name_w - RIGHT - 64) * v / vmax
    parts = []
    for k, it in enumerate(items):
        y = TOP - 16 + k * row
        w = max(sx(it["value"]), 2)
        r = min(4.0, w / 2)
        parts.append(f'<text x="{name_w - 10}" y="{y + 15}" text-anchor="end" font-size="12" fill="{INK}">{escape(it["name"])}</text>')
        parts.append(
            f'<path d="M{name_w},{y + 4} H{name_w + w - r:.1f} Q{name_w + w:.1f},{y + 4} {name_w + w:.1f},{y + 4 + r:.1f} '
            f'V{y + 20 - r:.1f} Q{name_w + w:.1f},{y + 20} {name_w + w - r:.1f},{y + 20} H{name_w} Z" fill="{BLUE}"/>'
        )
        parts.append(f'<text x="{name_w + w + 8:.1f}" y="{y + 16}" font-size="11" font-weight="600" fill="{INK}">{escape(fmt(it["value"]))}</text>')
        parts.append(f'<rect x="0" y="{y}" width="{W}" height="{row}" fill="transparent"><title>{escape(it["tip"])}</title></rect>')
    return _frame("".join(parts), label, height=height)
