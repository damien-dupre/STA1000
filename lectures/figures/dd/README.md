# Cached slide images from damien-dupre/img

Downloaded from `https://raw.githubusercontent.com/damien-dupre/img/main/`, which is
what `include_img()` resolves to in the xaringan decks under
`~/Drive/Projects/lectures/`. Cached here so these decks render without network
access and without depending on that repository staying put.

Re-fetch any of them with:

    curl -sSfL -O "https://raw.githubusercontent.com/damien-dupre/img/main/<name>"

## Used by lecture 2

| File | Where | Original source |
|---|---|---|
| `clean_zoom.jpg` | "What Is Going Wrong With This Table?" | @kareem_carr on Twitter |
| `clean_answer.png` | "Michael's Answer" | @CoffeeCodeCrash on Twitter |
| `name_convention.jpg` | "Michael's Answer" | unattributed meme |
| `viz_exercise_1.png` | Exercise 2 | Northwind sample database |
| `viz_key_figures_1.jpeg` | "A Chart for Every Question" | unattributed chart-chooser matrix |
| `viz_med_quartiles_1.png` | "What a Figure Throws Away" | unattributed |
| `viz_correlation_2.png` | "What a Figure Throws Away" | unattributed |
| `viz_piechart_1.jpeg` | "When Is a Pie Chart Acceptable?" | depictdatastudio.com |
| `dataviz_principle_2,3` | Principle 1: axes | Wilke, *Fundamentals of Data Visualization* |
| `dataviz_principle_8,9` | Principle 2: make it easy | Wilke |
| `dataviz_principle_10,11` | Principle 3: be fancy | Wilke |
| `dataviz_principle_14,15` | Principle 4: colour | Wilke |
| `dataviz_principle_18,19` | Principle 5: details | Wilke |
| `dataviz_exercise_1.png` | Exercise 3 | @WhiteHouse on Twitter |

## Used by lecture 2 and 3

| File | Where | Original source |
|---|---|---|
| `clean_zoom.jpg` | "What Is Going Wrong With This Table?" | @kareem_carr on Twitter |
| `clean_answer.png` | "Michael's Answer" | @CoffeeCodeCrash on Twitter |
| `name_convention.jpg` | "Michael's Answer" | unattributed meme |
| `viz_exercise_1.png` | Exercise 2 | Northwind sample database |
| `viz_key_figures_1.jpeg` | "A Chart for Every Question" | unattributed chart-chooser matrix |
| `viz_med_quartiles_1,2,3` | "What a Figure Throws Away" & Quartiles zoom | unattributed |
| `viz_correlation_1,2` | "What a Figure Throws Away" & Correlation zoom | unattributed |
| `viz_piechart_1,2` | "When Is a Pie Chart Acceptable?" | depictdatastudio.com |
| `example_piechart.jpg` | "When Is a Pie Chart Acceptable?" | depictdatastudio.com |
| `dataviz_principle_1..20` | Wilke's 5 Principles (before/after comparisons) | Wilke, *Fundamentals of Data Visualization* |
| `dataviz_exercise_1,3,4,6,7,9,10,11,12` | "How Charts Lie: The Hall of Shame" | Various news & social media |
| `tableau_frederica.png`, `tableau_good*`, `tableau_bad.png` | Tableau Dashboard Showcase | Federica Pinza (EDHEC 2024 Challenge) |
| `tableau_composition_*`, `tableau_simple_bar.gif`, `tableau_pie_chart.gif` | Composition in Tableau | Tableau Public demo |
| `tableau_distribution_*`, `tableau_histogram.gif`, `tableau_box_plot.gif`, `tableau_average_bar.gif` | Distribution in Tableau | Tableau Public demo |
| `tableau_comparison_*`, `tableau_multiple_bar.gif` | Comparison in Tableau | Tableau Public demo |
| `tableau_relationship_*`, `tableau_scatterplot.gif` | Relationship in Tableau | Tableau Public demo |
| `tableau_dashboard.png`, `tableau_dashboard.gif` | Building Dashboards in Tableau | Tableau Public demo |

Several are reproductions of third-party material. Fine for closed university
teaching; review before publishing the decks openly.

## Used by lecture 5

The three GIFs are Damien's own Tableau Public recordings, on the Covid-19 sample
(`lectures/data/covid_data_sample.csv`), compressed for the slides: 1050 px wide,
12 frames a second, 128 colours. The stills are frames cut from the same
recordings, or crops of images in the img repo.

| File | Where | Made from |
|---|---|---|
| `tableau_dual_axis.gif` | "Two Measures, One Chart" | `tableau_dual_axis.gif` (26.7 MB), stopped at frame 885, before the screen-recording dock appears |
| `tableau_map.gif` | "Mapping with Tableau" | `tableau_sheet_tooltip.gif` (54.2 MB), frames 420 to 961: Location, Show Me, filled map |
| `tableau_sheet_tooltip.gif` | "A Figure in the Tooltip" | `tableau_sheet_tooltip.gif`, frame 950 to the end: Insert, Sheets, then hover |
| `tableau_data_icons.png` | "Space and Time Variables" | frame 150 of `tableau_dual_axis.gif`, the Data pane |
| `tableau_date_menu.png` | "Date Parts or Date Values?" | frame 280 of `tableau_sheet_tooltip.gif`, the date pill menu |
| `tableau_show_filter_menu.png` | "Filter and Highlighter Menus" | the same frame, top of the menu |
| `tableau_tooltip_editor.png` | "Tooltips" | frame 995 of `tableau_sheet_tooltip.gif`, the Edit Tooltip dialog |
| `tableau_publish_as.png` | "Publish" | crop of `tableau_public.png` |
| `tableau_alias_dialog.png` | "Aliases" | crop of `tableau_alias_2.png` |
| `tableau_linecharts.png` | "Line and Area Charts" | `tableau_linecharts.png`, unchanged |
| `tableau_published.png` | "Publish" | `tableau_published.png`, unchanged |
| `tableau_public_actions.png` | "Dashboard Actions" | `tableau_public_actions.png`, unchanged |

Compression, with the frame range of each GIF:

    ffmpeg -i in.gif -vf "trim=start_frame=A:end_frame=B,setpts=PTS-STARTPTS,fps=12,scale=1050:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128:stats_mode=diff[p];[s1][p]paletteuse=dither=none:diff_mode=rectangle" out.gif
