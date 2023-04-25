from typing import Optional, Tuple

import matplotlib.lines as lines
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go


def return_matplotlib_arr(
    x,
    y,
    dpi=96,
    width=800,
    height=250,
    aa: bool = True,
    line_width_px: int = 1,
    xlim: Optional[Tuple] = None,
    ylim: Optional[Tuple] = None,
) -> np.ndarray:
    """Construct a matplotlib figure and return it as a numpy array.

    parameters
    ----------
    x : array-like
        x data
    y : array-like
        y data
    save_path : str
        path to save the figure to
    dpi : int
        dpi of the figure
    width : int
        width of the figure in pixels
    height : int
        height of the figure in pixels
    aa : bool
        whether to use anti-aliasing or not, defaults to True
    line_width_px : int
        width of the line in pixels
    xlim : tuple
        x limits of the figure
    ylim : tuple
        y limits of the figure

    .. Note::
        If you want to ensure that the images are 1-to-1 comparable you should always
        set the xlim and ylim to the same values for all images.

    """
    line_width_points = line_width_px / dpi * 72
    fig = plt.figure(frameon=False, dpi=dpi, linewidth=line_width_points)
    fig.set_size_inches(width / dpi, height / dpi)
    # make an ax that is the size of the figure
    ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
    ax.set_axis_off()
    # Scale x and y to the data ranges
    ax.add_line(
        lines.Line2D(
            xdata=x,
            ydata=y,
            c="black",
            aa=aa,
            linewidth=line_width_points,
        )
    )
    ax.set_xlim((x[0], x[-1]) if xlim is None else xlim)
    ax.set_ylim((min(y), max(y)) if ylim is None else ylim)
    # Add the line to the axes
    fig.add_axes(ax, projection=None)
    fig.canvas.draw()
    arr = np.asarray(fig.canvas.buffer_rgba())
    plt.close(fig)
    return arr


def construct_plotly_fig(
    x,
    y,
    save_path,
    width=800,
    height=250,
    line_shape="linear",
    line_width=1,
    aa=True,
    xlim=None,
    ylim=None,
):
    """Construct a plotly figure and save it to a file.

    TODO::
        Add xlim and ylim parameters.

    parameters
    ----------
    x : array-like
        x data
    y : array-like
        y data
    save_path : str
        path to save the figure to
    width : int
        width of the figure in pixels
    height : int
        height of the figure in pixels
    line_shape : str
        shape of the line; must be one of the following:
        'linear', 'spline', 'hv', 'vh', 'hvh', 'vhv'
    line_width : int
        width of the line in pixels
    aa : bool
        whether to use anti-aliasing can only be True!
    xlim : tuple
        x limits of the figure
    ylim : tuple
        y limits of the figure

    """
    assert aa, "Plotly does not support setting anti-aliasing to False."

    fig = go.Figure()
    axis_kwargs = dict(
        showgrid=False, zeroline=False, automargin=False, showticklabels=False
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        width=width,
        height=height,
        template=None,
        xaxis=axis_kwargs,
        yaxis=axis_kwargs,
    )
    fig.add_trace(
        go.Scatter(
            name="ball",
            line=dict(shape=line_shape, color="black", width=line_width),
            x=x,
            y=y,
        )
    )
    if xlim is not None:
        fig.update_xaxes(range=xlim)
    if ylim is not None:
        fig.update_yaxes(range=ylim)

    with open(save_path, "wb") as f:
        f.write(fig.to_image(format="png", width=width, height=height))
