"""Figures for Lecture 2, generated from data/insta-data.csv.

Run from the repository root:  python3 lectures/figures/loomrow/make_figures.py

Palette: slots 1-3 of the Anthropic data-viz reference palette, which is
validated for all-pairs separation under colour-vision deficiency in light mode.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

THOUSANDS = FuncFormatter(lambda v, _: f"{v:,.0f}")
PERCENT = FuncFormatter(lambda v, _: f"{v:g}%")

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "insta-data.csv"

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
FORMAT_ORDER = ["carousel", "image", "reel"]
FORMAT_COLOUR = dict(zip(FORMAT_ORDER, [BLUE, ORANGE, AQUA]))

plt.rcParams.update({
    "font.size": 15,
    "axes.titlesize": 17,
    "axes.labelsize": 15,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def tidy(ax, grid_axis="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


df = pd.read_csv(DATA, parse_dates=["posted_at"])
df["engagements"] = df["engagements_followers"] + df["engagements_non_followers"]

# 1. COMPOSITION -------------------------------------------------------------
counts = df["format"].value_counts().reindex(FORMAT_ORDER)
fig, ax = plt.subplots(figsize=(7.5, 4.0))
bars = ax.bar(counts.index, counts.values,
              color=[FORMAT_COLOUR[f] for f in counts.index], width=0.62)
for b, v in zip(bars, counts.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 3, f"{v}", ha="center", fontsize=14)
ax.set_ylabel("Posts")
ax.set_title("Composition: how the 431 posts split by format")
tidy(ax)
save(fig, "viz_composition.png")

# 2. DISTRIBUTION ------------------------------------------------------------
CUT = 60000
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.hist(df["reach"].clip(upper=CUT), bins=np.linspace(0, CUT, 61), color=BLUE)
med, mean = df["reach"].median(), df["reach"].mean()
ax.axvline(med, color=INK, linewidth=2)
ax.axvline(mean, color=ORANGE, linewidth=2, linestyle="--")
ax.set_xlim(0, CUT)
ax.set_ylim(0, 105)
ax.set_xlabel("Reach (accounts), top of range piled into the last bar")
ax.set_ylabel("Posts")
ax.set_title("Distribution: reach per post")
ax.xaxis.set_major_formatter(THOUSANDS)
ax.annotate(f"median {med:,.0f}", xy=(med, 62), xytext=(14000, 88),
            color=INK, fontsize=14,
            arrowprops=dict(arrowstyle="->", color=INK, linewidth=1.4))
ax.annotate(f"mean {mean:,.0f}", xy=(mean, 30), xytext=(20000, 58),
            color=ORANGE, fontsize=14,
            arrowprops=dict(arrowstyle="->", color=ORANGE, linewidth=1.4))
ax.annotate("one post reached 535,086", xy=(CUT, 6), xytext=(30000, 25),
            color=INK2, fontsize=13,
            arrowprops=dict(arrowstyle="->", color=INK2, linewidth=1.2))
tidy(ax)
save(fig, "viz_distribution.png")

# 3. COMPARISON --------------------------------------------------------------
rate = (df.groupby("format")[["engagements", "reach"]].sum()
          .assign(er=lambda d: 100 * d["engagements"] / d["reach"])
          .reindex(FORMAT_ORDER))
fig, ax = plt.subplots(figsize=(7.5, 4.0))
bars = ax.bar(rate.index, rate["er"],
              color=[FORMAT_COLOUR[f] for f in rate.index], width=0.62)
for b, v in zip(bars, rate["er"]):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.12, f"{v:.1f}%", ha="center", fontsize=14)
ax.set_ylabel("Engagement rate")
ax.set_title("Comparison: engagement rate by format")
ax.yaxis.set_major_formatter(PERCENT)
tidy(ax)
save(fig, "viz_comparison.png")

# 4. RELATIONSHIP ------------------------------------------------------------
sub = df[df["reach"] < 60000]
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.scatter(sub["reach"], sub["engagements"], s=26, color=BLUE, alpha=0.45,
           edgecolors="white", linewidths=0.6)
b1, b0 = np.polyfit(sub["reach"], sub["engagements"], 1)
xs = np.linspace(0, sub["reach"].max(), 50)
ax.plot(xs, b0 + b1 * xs, color=ORANGE, linewidth=2)
r = sub["reach"].corr(sub["engagements"])
ax.text(0.03, 0.93, f"r = {r:.2f}", transform=ax.transAxes, fontsize=15, color=INK)
ax.set_xlabel("Reach (accounts)")
ax.set_ylabel("Engagements")
ax.xaxis.set_major_formatter(THOUSANDS)
ax.yaxis.set_major_formatter(THOUSANDS)
ax.set_title("Relationship: engagements against reach")
tidy(ax, grid_axis="both")
save(fig, "viz_relationship.png")

# 5. PIE VS BAR --------------------------------------------------------------
theme = df["theme"].value_counts()
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
axes[0].pie(theme.values, labels=theme.index, textprops={"fontsize": 12},
            colors=plt.cm.Blues(np.linspace(0.35, 0.9, len(theme))),
            wedgeprops={"edgecolor": "white", "linewidth": 2})
axes[0].set_title("Six slices. Which is bigger?", fontsize=15)
order = theme.sort_values()
axes[1].barh(order.index, order.values, color=BLUE, height=0.62)
for y, v in enumerate(order.values):
    axes[1].text(v + 2, y, f"{v}", va="center", fontsize=13)
axes[1].set_title("Same data, answerable", fontsize=15)
axes[1].set_xlabel("Posts")
tidy(axes[1], grid_axis="x")
save(fig, "viz_pie_vs_bar.png")

# 6. AXIS PRINCIPLE ----------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.2))
vals = rate["er"]
for ax, lo, title in [(axes[0], 3.6, "Truncated axis: reels look ruinous"),
                      (axes[1], 0.0, "Zero baseline: the honest gap")]:
    bars = ax.bar(vals.index, vals.values,
                  color=[FORMAT_COLOUR[f] for f in vals.index], width=0.62)
    ax.set_ylim(lo, 8.9)
    for b, v in zip(bars, vals.values):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.1, f"{v:.1f}%", ha="center", fontsize=13)
    ax.set_title(title, fontsize=15)
    ax.set_ylabel("Engagement rate")
    ax.yaxis.set_major_formatter(PERCENT)
    tidy(ax)
save(fig, "viz_principle_axes.png")

# 7. A DELIBERATELY BAD CHART -------------------------------------------------
# The Lecture 2 critique exercise. Every fault here is intentional: a 0.5 point
# spread stretched by a truncated axis, rainbow colour carrying no information,
# a legend duplicating the axis, spurious precision, a meaningless y label, and
# no sample size anywhere.
pl = (df.groupby("product_line")[["engagements_followers", "reach_followers"]].sum()
        .assign(er=lambda d: 100 * d["engagements_followers"] / d["reach_followers"]))
fig, ax = plt.subplots(figsize=(8.0, 4.4))
rainbow = ["#d62728", "#ff7f0e", "#ffdd00", "#2ca02c", "#1f77b4"]
bars = ax.bar(pl.index, pl["er"], color=rainbow, width=0.86)
ax.set_ylim(9.8, 10.52)
ax.set_ylabel("Value")
ax.grid(axis="both", color="#999999", linewidth=1.1)
ax.set_axisbelow(False)
for b, v in zip(bars, pl["er"]):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.012, f"{v:.4f}",
            ha="center", fontsize=12)
ax.legend(bars, list(pl.index), ncol=3, fontsize=11, loc="upper center",
          bbox_to_anchor=(0.5, 1.16))
save(fig, "viz_bad_chart.png")
