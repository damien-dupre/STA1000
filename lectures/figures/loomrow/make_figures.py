"""Figures for the STA1000 decks, generated from data/insta-data.csv.
Lecture 3 uses them: the four families of figure on the Loomrow data.

Run from the repository root:  python3 lectures/figures/loomrow/make_figures.py

Palette: slots 1-3 of the Anthropic data-viz reference palette for `format`,
validated for all-pairs separation under colour-vision deficiency in light mode,
and slots 6-7 (green, violet) for `is_paid`, validated as a pair.
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
# A critique exercise, not used by a deck at present. Every fault here is intentional: a 0.5 point
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


# ============================================================================
# LECTURE 3: THE FOUR FAMILIES, REDRAWN ON LOOMROW
# The ggplot figures in lectures/data_analytics/visualisation_principle.Rmd
# (drawn there on organisation_alpha) rebuilt on insta-data.csv, so the
# principles section and the Tableau exercises use the same data.
# ============================================================================

GREEN, VIOLET = "#008300", "#4a3aa7"   # slots 6 and 7, validated as a pair
PAID_ORDER = [False, True]
PAID_LABEL = {False: "organic", True: "paid"}
PAID_COLOUR = {False: GREEN, True: VIOLET}
REACH_CAP = 60000     # reach axes stop here; 3 posts lie above it
IMPR_CAP = 100000     # impressions axes stop here; 2 posts lie above it
N_REACH_ABOVE = int((df["reach"] > REACH_CAP).sum())
N_IMPR_ABOVE = int((df["impressions"] > IMPR_CAP).sum())
NOTE = dict(ha="right", va="bottom", fontsize=12, color=INK2)
RNG = np.random.default_rng(42)
KILO = FuncFormatter(lambda v, _: "0" if v == 0 else f"{v / 1000:,.0f}k")


def label_bars(ax, bars, values, fmt, offset):
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, b.get_y() + b.get_height() + offset,
                fmt.format(v), ha="center", va="bottom", fontsize=14)


def bandwidth(x):
    """Silverman's robust rule: the long tail must not flatten the curve."""
    x = np.asarray(x, dtype=float)
    iqr = np.subtract(*np.percentile(x, [75, 25]))
    return 0.9 * min(x.std(ddof=1), iqr / 1.34) * len(x) ** (-0.2)


def density(x, grid):
    x = np.asarray(x, dtype=float)
    h = bandwidth(x)
    z = (grid[:, None] - x[None, :]) / h
    return np.exp(-0.5 * z ** 2).sum(axis=1) / (len(x) * h * np.sqrt(2 * np.pi))


def mean_ci(x, n_boot=2000):
    """Mean with a bootstrap 95% interval, as mean_cl_boot does in the Rmd."""
    x = np.asarray(x, dtype=float)
    boots = RNG.choice(x, size=(n_boot, len(x)), replace=True).mean(axis=1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return x.mean(), lo, hi


paid_counts = df["is_paid"].value_counts().reindex(PAID_ORDER)
format_counts = df["format"].value_counts()          # sorted, largest first
x3 = np.arange(len(FORMAT_ORDER))

# 8. COMPOSITION: COUNTS ------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.3), sharey=True,
                         gridspec_kw={"width_ratios": [2, 3]})
bars = axes[0].bar([PAID_LABEL[k] for k in PAID_ORDER], paid_counts.values,
                   color=[PAID_COLOUR[k] for k in PAID_ORDER], width=0.6)
label_bars(axes[0], bars, paid_counts.values, "{:,.0f}", 4)
axes[0].set_title("is_paid: two categories")
axes[0].set_ylabel("Posts")
bars = axes[1].bar(format_counts.index, format_counts.values,
                   color=[FORMAT_COLOUR[f] for f in format_counts.index], width=0.6)
label_bars(axes[1], bars, format_counts.values, "{:,.0f}", 4)
axes[1].set_title("format: three categories")
axes[0].set_ylim(0, 340)
for ax in axes:
    tidy(ax)
save(fig, "viz_composition_counts.png")

# 9. COMPOSITION: PROPORTIONS -------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.3),
                         gridspec_kw={"width_ratios": [2, 3]})
paid_share = 100 * paid_counts / paid_counts.sum()
wedges, _ = axes[0].pie(paid_share.values, startangle=90, counterclock=False,
                        colors=[PAID_COLOUR[k] for k in PAID_ORDER],
                        wedgeprops={"edgecolor": "white", "linewidth": 2})
for w, k, v in zip(wedges, PAID_ORDER, paid_share.values):
    angle = np.deg2rad((w.theta1 + w.theta2) / 2)
    axes[0].text(0.58 * np.cos(angle), 0.58 * np.sin(angle),
                 f"{PAID_LABEL[k]}\n{v:.1f}%", ha="center", va="center",
                 color="white", fontsize=15, fontweight="bold")
axes[0].set_title("is_paid: a pie works for two")
format_share = 100 * format_counts / format_counts.sum()
bars = axes[1].bar(format_share.index, format_share.values,
                   color=[FORMAT_COLOUR[f] for f in format_share.index], width=0.6)
label_bars(axes[1], bars, format_share.values, "{:.1f}%", 0.6)
axes[1].set_ylim(0, 55)
axes[1].set_ylabel("Share of posts")
axes[1].yaxis.set_major_formatter(PERCENT)
axes[1].set_title("format: proportions as bars")
tidy(axes[1])
save(fig, "viz_composition_proportions.png")

# 10. DISTRIBUTION: FOUR FORMS OF ONE VARIABLE ---------------------------------
reach = df["reach"]
grid = np.linspace(0, REACH_CAP, 600)
fig, axes = plt.subplots(1, 4, figsize=(12.0, 4.6), sharey=True)
axes[0].hist(reach, bins=np.arange(0, REACH_CAP + 2000, 2000),
             orientation="horizontal", color=BLUE, edgecolor="white", linewidth=0.6)
axes[0].set_xlabel("Posts")
axes[0].set_title("Histogram")
dens = density(reach, grid)
axes[1].fill_betweenx(grid, 0, dens, color=BLUE, alpha=0.2, linewidth=0)
axes[1].plot(dens, grid, color=BLUE, linewidth=2)
axes[1].set_xlim(left=0)
axes[1].set_xticks([])
axes[1].set_xlabel("Density")
axes[1].set_title("Density")
axes[2].boxplot(reach, widths=0.5, patch_artist=True, whis=1.5,
                boxprops=dict(facecolor="#cde2fb", edgecolor=BLUE, linewidth=1.6),
                whiskerprops=dict(color=BLUE, linewidth=1.6),
                capprops=dict(color=BLUE, linewidth=1.6),
                medianprops=dict(color=INK, linewidth=2.2),
                flierprops=dict(marker="o", markersize=5, markerfacecolor=BLUE,
                                markeredgecolor="white", alpha=0.6))
axes[2].set_xticks([])
axes[2].set_title("Box plot")
m, lo, hi = mean_ci(reach)
axes[3].bar([0], [m], width=0.5, color=BLUE)
axes[3].errorbar([0], [m], yerr=[[m - lo], [hi - m]], color=INK, capsize=10, linewidth=2)
axes[3].set_xlim(-0.8, 0.8)
axes[3].set_xticks([])
axes[3].set_title("Dynamite")
axes[3].text(0.42, m, f"mean\n{m:,.0f}", va="center", fontsize=13, color=INK)
axes[0].set_ylim(0, REACH_CAP)
axes[0].set_ylabel("Reach (accounts)")
axes[0].yaxis.set_major_formatter(THOUSANDS)
for ax in axes:
    tidy(ax, grid_axis="y")
fig.text(0.99, -0.02, f"Axis cut at 60,000: {N_REACH_ABOVE} posts reached more, "
         f"up to {reach.max():,.0f}. Error bar: 95% interval of the mean.", **NOTE)
save(fig, "viz_distribution_forms.png")

# 11. COMPARISON: TWO CATEGORICAL VARIABLES ------------------------------------
ct = (pd.crosstab(df["format"], df["is_paid"])
        .reindex(index=FORMAT_ORDER, columns=PAID_ORDER))
fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.4))
bottom = np.zeros(len(x3))
for k in PAID_ORDER:
    axes[0].bar(x3, ct[k].values, bottom=bottom, width=0.62, color=PAID_COLOUR[k],
                edgecolor="white", linewidth=1.5, label=PAID_LABEL[k])
    bottom += ct[k].values
axes[0].set_title("Stacked")
axes[0].set_ylabel("Posts")
width = 0.36
for i, k in enumerate(PAID_ORDER):
    axes[1].bar(x3 + (i - 0.5) * width, ct[k].values, width=width,
                color=PAID_COLOUR[k], edgecolor="white", linewidth=1.5)
axes[1].set_title("Dodged")
axes[1].set_ylabel("Posts")
share = ct.div(ct.sum(axis=1), axis=0) * 100
bottom = np.zeros(len(x3))
for k in PAID_ORDER:
    axes[2].bar(x3, share[k].values, bottom=bottom, width=0.62, color=PAID_COLOUR[k],
                edgecolor="white", linewidth=1.5)
    for xi, b, v in zip(x3, bottom, share[k].values):
        axes[2].text(xi, b + v / 2, f"{v:.0f}%", ha="center", va="center",
                     color="white", fontsize=13, fontweight="bold")
    bottom += share[k].values
axes[2].set_title("Proportion (100%)")
axes[2].set_ylabel("Share of posts")
axes[2].yaxis.set_major_formatter(PERCENT)
for ax in axes:
    ax.set_xticks(x3, FORMAT_ORDER)
    tidy(ax)
axes[1].set_ylim(axes[0].get_ylim())
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False,
           bbox_to_anchor=(0.5, 1.07), fontsize=14)
save(fig, "viz_comparison_counts.png")

# 12. COMPARISON: CATEGORICAL AND CONTINUOUS, THE SHAPES -----------------------
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
for f in FORMAT_ORDER:
    axes[0].plot(grid, density(df.loc[df["format"] == f, "reach"], grid),
                 color=FORMAT_COLOUR[f], linewidth=2.2, label=f)
axes[0].set_xlim(0, REACH_CAP)
axes[0].set_ylim(bottom=0)
axes[0].set_yticks([])
axes[0].set_ylabel("Density")
axes[0].set_xlabel("Reach (accounts)")
axes[0].xaxis.set_major_formatter(KILO)
axes[0].legend(frameon=False, fontsize=14)
axes[0].set_title("Density by format")
tidy(axes[0], grid_axis="x")
groups = [df.loc[df["format"] == f, "reach"].values for f in FORMAT_ORDER]
bp = axes[1].boxplot(groups, widths=0.45, patch_artist=True, whis=1.5,
                     medianprops=dict(color=INK, linewidth=2.2),
                     flierprops=dict(marker="o", markersize=4.5, markeredgecolor="white",
                                     alpha=0.6))
for i, f in enumerate(FORMAT_ORDER):
    c = FORMAT_COLOUR[f]
    bp["boxes"][i].set(facecolor=matplotlib.colors.to_rgba(c, 0.22), edgecolor=c, linewidth=1.6)
    for part in ("whiskers", "caps"):
        for line in bp[part][2 * i:2 * i + 2]:
            line.set(color=c, linewidth=1.6)
    bp["fliers"][i].set(markerfacecolor=c)
    med = np.median(groups[i])
    axes[1].text(i + 1.26, med, f"{med:,.0f}", ha="left", va="center",
                 fontsize=12, color=INK)
axes[1].set_xticks([1, 2, 3], FORMAT_ORDER)
axes[1].set_xlim(0.6, 3.75)
axes[1].set_ylim(0, REACH_CAP)
axes[1].set_ylabel("Reach (accounts)")
axes[1].yaxis.set_major_formatter(THOUSANDS)
axes[1].set_title("Box plots by format, medians labelled")
tidy(axes[1])
fig.text(0.99, -0.02, f"Axes cut at 60,000: {N_REACH_ABOVE} posts reached more.", **NOTE)
save(fig, "viz_comparison_shapes.png")

# 13. COMPARISON: THE RANKING FLIPS -------------------------------------------
stats = [mean_ci(g) for g in groups]
medians = [np.median(g) for g in groups]
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4), sharey=True)
colours = [FORMAT_COLOUR[f] for f in FORMAT_ORDER]
means = np.array([s[0] for s in stats])
yerr = np.array([[s[0] - s[1] for s in stats], [s[2] - s[0] for s in stats]])
axes[0].bar(x3, means, width=0.6, color=colours)
axes[0].errorbar(x3, means, yerr=yerr, fmt="none", ecolor=INK, capsize=8, linewidth=2)
for xi, v, top in zip(x3, means, means + yerr[1]):
    axes[0].text(xi, top + 350, f"{v:,.0f}", ha="center", va="bottom", fontsize=14)
axes[0].set_title("Mean reach, with 95% interval")
axes[0].set_ylabel("Reach (accounts)")
bars = axes[1].bar(x3, medians, width=0.6, color=colours)
label_bars(axes[1], bars, medians, "{:,.0f}", 350)
axes[1].set_title("Median reach")
for ax in axes:
    ax.set_xticks(x3, FORMAT_ORDER)
    ax.yaxis.set_major_formatter(THOUSANDS)
    tidy(ax)
axes[0].set_ylim(0, max(means + yerr[1]) * 1.12)
save(fig, "viz_comparison_mean_median.png")

# 14. RELATIONSHIP: SCATTERPLOT AND REGRESSION LINE ----------------------------
sub = df[df["impressions"] <= IMPR_CAP]
b1, b0 = np.polyfit(sub["impressions"], sub["likes"], 1)
r_sub = sub["impressions"].corr(sub["likes"])
r_all = df["impressions"].corr(df["likes"])
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4), sharex=True, sharey=True)
for ax in axes:
    ax.scatter(sub["impressions"], sub["likes"], s=30, color=BLUE, alpha=0.45,
               edgecolors="white", linewidths=0.6)
    ax.set_xlabel("Impressions")
    ax.xaxis.set_major_formatter(THOUSANDS)
    ax.yaxis.set_major_formatter(THOUSANDS)
    tidy(ax, grid_axis="both")
xs = np.linspace(0, sub["impressions"].max(), 50)
axes[1].plot(xs, b0 + b1 * xs, color=ORANGE, linewidth=2.2)
axes[1].text(0.04, 0.92, f"r = {r_sub:.2f}", transform=axes[1].transAxes, fontsize=15)
axes[0].set_ylabel("Likes")
axes[0].set_title("Scatterplot")
axes[1].set_title("With a regression line")
fig.text(0.99, -0.02, f"{N_IMPR_ABOVE} posts with more than 100,000 impressions not shown; "
         f"with them included, r = {r_all:.2f}.", **NOTE)
save(fig, "viz_relationship_forms.png")

# 15. RELATIONSHIP: ONE PANEL PER FORMAT --------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.3), sharex=True, sharey=True)
for ax, f in zip(axes, FORMAT_ORDER):
    s = sub[sub["format"] == f]
    fb1, fb0 = np.polyfit(s["impressions"], s["likes"], 1)
    ax.scatter(s["impressions"], s["likes"], s=26, color=FORMAT_COLOUR[f], alpha=0.5,
               edgecolors="white", linewidths=0.5)
    xs = np.linspace(0, s["impressions"].max(), 50)
    ax.plot(xs, fb0 + fb1 * xs, color=INK, linewidth=2)
    ax.text(0.05, 0.93, f"{100 * fb1:.1f} likes per\n100 impressions", transform=ax.transAxes,
            va="top", fontsize=14)
    ax.set_title(f)
    ax.set_xlabel("Impressions")
    ax.xaxis.set_major_formatter(KILO)
    ax.yaxis.set_major_formatter(THOUSANDS)
    tidy(ax, grid_axis="both")
axes[0].set_ylabel("Likes")
save(fig, "viz_relationship_facets.png")
