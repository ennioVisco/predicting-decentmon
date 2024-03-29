import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame, concat
from seaborn import FacetGrid, catplot, barplot, boxplot

from decmon.constants import METRICS, PATTERNS, ALPHABET
from decmon.runner import formula_patterns

_COLOR_PALETTE = "dark"
_BAR_INTERVAL = "sd"     # as of Standard Deviation


def plot_grid_barplots(df: DataFrame, grid_cell_field: str,
                       y_axis: str, x_axis: str, order: [str]):
    """
    Plots a grid of plots, one for each value of the grid_cell_field
    :param df: the dataframe to plot
    :param grid_cell_field: the field to use to split the grid
    :param y_axis: the common numerical field to use as y-axis
    :param x_axis: the categorical field to use as x-axis
    :param order: the order of the categorical values over the x-axis
    :return: nothing. Plots the data
    """
    g = FacetGrid(df, col=grid_cell_field, sharey=False)
    # plt.ylim(0, 5000)
    fig = g.map(
        barplot, x_axis, y_axis,
        order=order,
        errorbar=_BAR_INTERVAL,
        palette=_COLOR_PALETTE
    )
    return fig


def plot_barplot(df: DataFrame):
    """
    Plots the data from a single-strategy dataframe
    :param df: single-strategy dataframe
    :return: nothing. Plots the data
    """
    fig = catplot(
        # ax=ax,
        data=df,
        kind="bar",
        errorbar=_BAR_INTERVAL,
        palette=_COLOR_PALETTE,
        alpha=.8,
        height=6
    )
    fig.set_axis_labels("", "Count")
    return fig


def plot_boxplot(df: DataFrame):
    """
    Plots the data from a single-strategy dataframe
    :param df: single-strategy dataframe
    :return: nothing. Plots the data
    """
    fig = boxplot(
        # ax=ax,
        data=df,
        # kind="bar",
        # errorbar=_BAR_INTERVAL,
        palette=_COLOR_PALETTE,
        # alpha=.8,
        # height=6
    )
    # fig.set_axis_labels("", "Count")
    return fig


def plot_metrics_by_patterns(dfs: [DataFrame]):
    df = concat(dfs)
    df['metric'] = df['metric'].replace(METRICS.keys(), METRICS.values())

    g = FacetGrid(df, col="metric", sharey=False)
    g.fig.suptitle('Mean, and std. dev. by metric, for each pattern',
                   fontsize=14)

    g.map_dataframe(barplot, x='pattern', y='value', hue='strategy',
                    palette='bright')
    g.add_legend()
    return g


def plot_metrics_by_components(df: DataFrame, metric: str):
    # Draw a nested boxplot to show bills by day and time
    ax = boxplot(x="nodes", y="value",
                 hue="strategy", palette='bright', showfliers=False,
                 data=df)
    ax.set(title=f'Metric: {metric}')
    # sns.despine(offset=10, trim=True)
    ax.legend(bbox_to_anchor=(1.1, 0.95))
    return ax


def plot_temp_pattern_variance(dfs: [DataFrame]):
    to_drop = ['formula_id', 'x']

    for i in PATTERNS:
        cleaned_up_data = dfs[i].drop(to_drop, axis=1)
        plot = plot_boxplot(cleaned_up_data)
    return plot


def plot_atoms_variation(dfs: [DataFrame], cap: int) -> [DataFrame]:
    to_return = []
    for i in PATTERNS:
        target_df = dfs[i].transpose()
        result = DataFrame()
        for letter in range(1, cap + 1):
            result[ALPHABET[letter - 1]] = target_df.where(target_df == -letter).count()
        result = result.sort_index(key=result.sum(1).get, ascending=False)
        result2 = DataFrame({'data': (result > 0).transpose().sum()})
        result2 = DataFrame(result2['data'].value_counts())
        result2 = result2.sort_index()

        plt.plot(result2, label=f'{formula_patterns[i][0][1:]}')
        to_return.append(result)
    plt.ylabel('Identifier of the formula')
    plt.xlabel('Number of unique atoms')
    plt.title('Number of unique atoms per formula')
    plt.legend(loc='upper right')
    return to_return

