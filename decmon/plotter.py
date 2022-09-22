from pandas import DataFrame
from seaborn import FacetGrid, catplot, barplot, boxplot

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
