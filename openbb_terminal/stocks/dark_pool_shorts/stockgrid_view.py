""" Stockgrid View """
__docformat__ = "numpy"

import logging
import os

import matplotlib.pyplot as plt

from openbb_terminal.config_plot import PLOT_DPI
from openbb_terminal.core.plots.plotly_helper import OpenBBFigure, theme
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import export_data, plot_autoscale, print_rich_table
from openbb_terminal.rich_config import console
from openbb_terminal.stocks.dark_pool_shorts import stockgrid_model

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def dark_pool_short_positions(
    limit: int = 10,
    sortby: str = "dpp_dollar",
    ascend: bool = False,
    export: str = "",
    sheet_name: str = None,
):
    """Get dark pool short positions. [Source: Stockgrid]

    Parameters
    ----------
    limit : int
        Number of top tickers to show
    sortby : str
        Field for which to sort by, where 'sv': Short Vol. [1M],
        'sv_pct': Short Vol. %%, 'nsv': Net Short Vol. [1M],
        'nsv_dollar': Net Short Vol. ($100M), 'dpp': DP Position [1M],
        'dpp_dollar': DP Position ($1B)
    ascend : bool
        Data in ascending order
    export : str
        Export dataframe data to csv,json,xlsx file
    """
    df = stockgrid_model.get_dark_pool_short_positions(sortby, ascend)

    dp_date = df["Date"].values[0]
    df = df.drop(columns=["Date"])
    df["Net Short Volume $"] = df["Net Short Volume $"] / 100_000_000
    df["Short Volume"] = df["Short Volume"] / 1_000_000
    df["Net Short Volume"] = df["Net Short Volume"] / 1_000_000
    df["Short Volume %"] = df["Short Volume %"] * 100
    df["Dark Pools Position $"] = df["Dark Pools Position $"] / (1_000_000_000)
    df["Dark Pools Position"] = df["Dark Pools Position"] / 1_000_000
    df.columns = [
        "Ticker",
        "Short Vol. [1M]",
        "Short Vol. %",
        "Net Short Vol. [1M]",
        "Net Short Vol. ($100M)",
        "DP Position [1M]",
        "DP Position ($1B)",
    ]

    # Assuming that the datetime is the same, which from my experiments seems to be the case
    print_rich_table(
        df.iloc[:limit],
        headers=list(df.columns),
        show_index=False,
        title=f"Data for: {dp_date}",
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "dppos",
        df,
        sheet_name,
    )


@log_start_end(log=logger)
def short_interest_days_to_cover(
    limit: int = 10, sortby: str = "float", export: str = "", sheet_name: str = None
):
    """Print short interest and days to cover. [Source: Stockgrid]

    Parameters
    ----------
    limit : int
        Number of top tickers to show
    sortby : str
        Field for which to sort by, where 'float': Float Short %%,
        'dtc': Days to Cover, 'si': Short Interest
    export : str
        Export dataframe data to csv,json,xlsx file
    """
    df = stockgrid_model.get_short_interest_days_to_cover(sortby)

    dp_date = df["Date"].values[0]
    df = df.drop(columns=["Date"])

    # Assuming that the datetime is the same, which from my experiments seems to be the case
    print_rich_table(
        df.iloc[:limit],
        headers=list(df.columns),
        show_index=False,
        title=f"Data for: {dp_date}",
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "shortdtc",
        df,
        sheet_name,
    )


@log_start_end(log=logger)
def short_interest_volume(
    symbol: str,
    limit: int = 84,
    raw: bool = False,
    export: str = "",
    sheet_name: str = None,
    external_axes: bool = False,
):
    """Plot price vs short interest volume. [Source: Stockgrid]

    Parameters
    ----------
    symbol : str
        Stock to plot for
    limit : int
        Number of last open market days to show
    raw : bool
        Flag to print raw data instead
    export : str
        Export dataframe data to csv,json,xlsx file
    external_axes : bool, optional
        Whether to return the figure object or not, by default False

    """

    df, prices = stockgrid_model.get_short_interest_volume(symbol)
    if df.empty:
        return console.print("[red]No data available[/red]\n")

    if raw:
        df.date = df.date.dt.date

        print_rich_table(
            df.iloc[:limit],
            headers=list(df.columns),
            show_index=False,
            title="Price vs Short Volume",
        )
    else:
        # Output data
        fig = OpenBBFigure.create_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            horizontal_spacing=0,
            row_width=[0.3, 0.6],
            specs=[[{"secondary_y": True}], [{"secondary_y": False}]],
        )
        # pycodestyle: disable=E501,E203
        fig.add_scatter(
            name=symbol,
            x=df["date"],
            y=prices[len(prices) - len(df) :],  # pycodestyle: disable=E501,E203
            line=dict(color="#fdc708", width=2),
            connectgaps=True,
            yaxis="y2",
            opacity=1,
            showlegend=False,
            row=1,
            col=1,
            secondary_y=True,
        )
        fig.add_bar(
            x=df["date"],
            y=df["Total Vol. [1M]"],
            name="Total Volume",
            marker_color=theme.up_color,
            row=1,
            col=1,
            secondary_y=False,
        )
        fig.add_bar(
            x=df["date"],
            y=df["Short Vol. [1M]"],
            name="Short Volume",
            marker_color=theme.down_color,
            row=1,
            col=1,
            secondary_y=False,
        )
        fig.add_scatter(
            name="Short Vol. %",
            x=df["date"],
            y=df["Short Vol. %"],
            line=dict(width=2),
            connectgaps=True,
            opacity=1,
            showlegend=False,
            row=2,
            col=1,
            secondary_y=False,
        )

        fig.update_traces(hovertemplate="%{y:.2f}")
        fig.update_layout(
            margin=dict(l=40, r=0),
            title=f"<b>Price vs Short Volume Interest for {symbol}</b>",
            title_x=0.025,
            title_font_size=14,
            yaxis2_title="Stock Price ($)",
            yaxis_title="FINRA Volume [M]",
            yaxis3_title="Short Vol. %",
            yaxis=dict(
                side="left",
                fixedrange=False,
                showgrid=False,
                titlefont=dict(color="#d81aea"),
                tickfont=dict(color="#d81aea"),
                nticks=20,
                title_standoff=20,
                layer="above traces",
            ),
            yaxis2=dict(
                side="right",
                fixedrange=False,
                anchor="x",
                overlaying="y",
                titlefont=dict(color="#fdc708"),
                tickfont=dict(color="#fdc708"),
                nticks=10,
                layer="below traces",
                title_standoff=10,
            ),
            yaxis3=dict(
                fixedrange=False,
                titlefont=dict(color="#9467bd"),
                tickfont=dict(color="#9467bd"),
                nticks=10,
            ),
            hovermode="x unified",
            spikedistance=1,
            hoverdistance=1,
        )

        fig.hide_holidays()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "shortint(stockgrid)",
        df,
        sheet_name,
    )

    return None if raw else fig.show() if not external_axes else fig


@log_start_end(log=logger)
def net_short_position(
    symbol: str,
    limit: int = 84,
    raw: bool = False,
    export: str = "",
    sheet_name: str = None,
    external_axes: bool = False,
):
    """Plot net short position. [Source: Stockgrid]

    Parameters
    ----------
    symbol: str
        Stock to plot for
    limit : int
        Number of last open market days to show
    raw : bool
        Flag to print raw data instead
    export : str
        Export dataframe data to csv,json,xlsx file
    external_axes : bool, optional
        Whether to return the figure object or not, by default False

    """

    df = stockgrid_model.get_net_short_position(symbol)
    if df.empty:
        console.print("[red]No data available[/red]\n")
        return

    if raw:

        df["dates"] = df["dates"].dt.date

        print_rich_table(
            df.iloc[:limit],
            headers=list(df.columns),
            show_index=False,
            title="Net Short Positions",
        )

    else:

        # This plot has 2 axes
        _, ax1 = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
        ax2 = ax1.twinx()

        df = df.sort_values(by=["dates"])
        ax1.bar(
            df["dates"],
            df["Net Short Vol. (1k $)"],
            color=theme.down_color,
            label="Net Short Vol. (1k $)",
        )
        ax1.set_ylabel("Net Short Vol. (1k $)")

        ax2.plot(
            df["dates"].values,
            df["Position (1M $)"],
            c=theme.up_color,
            label="Position (1M $)",
        )
        ax2.set_ylabel("Position (1M $)")

        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc="upper left")

        ax1.set_xlim(
            df["dates"].values[max(0, len(df) - limit)], df["dates"].values[len(df) - 1]
        )

        ax1.set_title(f"Net Short Vol. vs Position for {symbol}")

        # theme.style_twin_axes(ax1, ax2)

        # if not external_axes:
        #     theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "shortpos",
        df,
        sheet_name,
    )
