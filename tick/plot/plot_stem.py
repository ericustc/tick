import numpy as np


def stem(y: np.ndarray, show=True, title=None, x_range=None, y_range=None):
    """Stem plot using bokeh

    Parameters
    ----------
    y : `numpy.ndarray`, shape=(n_coeffs,)
        The vector to plot

    show : `bool`, default=`True`
        if True, show the plot. Use False if you want to superpose several
        plots

    title : `str`, default=`None`
        The title of the plot

    x_range : `bokeh.models.ranges.Range1d` or `list` with 2 elements
        The x-axis range

    y_range : `bokeh.models.ranges.Range1d` or `list` with 2 elements
        The y-axis range

    Returns
    -------
    output : `bokeh.plotting.figure` or `None`
        A `bokeh` Figure object if ``show=False``, None otherwise
    """
    import bokeh.plotting as bk

    dim = y.shape[0]
    x = np.arange(dim)
    plot_width = 600
    plot_height = 200
    fig = bk.figure(plot_width=plot_width, plot_height=plot_height,
                    x_range=x_range, y_range=y_range)
    fig.scatter(x, y, size=4, fill_alpha=0.5)
    fig.segment(x, np.zeros(dim), x, y)
    fig.title.text_font_size = "12pt"
    if title is not None:
        fig.title.text = title
    if show:
        bk.show(fig)
        return fig
    else:
        return fig


def stems_bokeh(ys: list, titles: list = None, show=True, sync_axes=True):
    """Several stem plots with synchronized axes using bokeh rendering

    Parameters
    ----------
    ys : `list` of `np.ndarray`
        A list of numpy arrays to be plotted

    titles : `list` of `str`
        The titles of each plot

    show : `bool`, default=`True`
        if True, show the plot. Use False if you want to superpose several
        plots

    sync_axes : `bool`, default=`True`
        If True, the axes of the stem plot are synchronized

    Returns
    -------
    output : `bokeh.models.layouts.Column` or `None`
        A bokeh object containing the layout of the plot, when ``show=False``,
        None otherwise.
    """
    import bokeh.plotting as bk
    figs = []
    x_range = None
    y_range = None
    for idx, y in enumerate(ys):
        if titles is not None:
            title = titles[idx]
        else:
            title = None
        fig = stem(y, show=False, title=title, x_range=x_range, y_range=y_range)
        figs.append(fig)
        if idx == 0 and sync_axes:
            x_range = fig.x_range
            y_range = fig.y_range
    p = bk.gridplot([[e] for e in figs])
    if show:
        bk.show(p)
        return None
    else:
        return p


def stems_matplotlib(ys: list, titles: list = None, show=True, sync_axes=True):
    """Several stem plots with synchronized axes using bokeh rendering

    Parameters
    ----------
    ys : `list` of `np.ndarray`
        A list of numpy arrays to be plotted

    titles : `list` of `str`
        The titles of each plot

    show : `bool`, default=`True`
        if True, show the plot. Use False if you want to superpose several
        plots

    sync_axes : `bool`, default=`True`
        If True, the axes of the stem plot are synchronized

    Returns
    -------
    output : `bokeh.models.layouts.Column` or `None`
        A bokeh object containing the layout of the plot, when ``show=False``,
        None otherwise.
    """
    import matplotlib.pyplot as plt
    figs = []
    x_range = None
    y_range = None
    plt.figure(figsize=())
    for idx, y in enumerate(ys):
        if titles is not None:
            title = titles[idx]
        else:
            title = None
        fig = plt.stem(y, title=title, x_range=x_range, y_range=y_range)
        figs.append(fig)
        if idx == 0 and sync_axes:
            x_range = fig.x_range
            y_range = fig.y_range
    p = bk.gridplot([[e] for e in figs])
    if show:
        bk.show(p)
        return None
    else:
        return p


def stems(ys: list, titles: list = None, show=True, sync_axes=True,
          rendering: str='bokeh'):
    """Several stem plots with synchronized axes

    Parameters
    ----------
    ys : `list` of `np.ndarray`
        A list of numpy arrays to be plotted

    titles : `list` of `str`
        The titles of each plot

    show : `bool`, default=`True`
        if True, show the plot. Use False if you want to superpose several
        plots

    sync_axes : `bool`, default=`True`
        If True, the axes of the stem plot are synchronized (available only
        with ``rendering='bokeh'``

    rendering : {'matplotlib', 'bokeh'}, default='matplotlib'
        Rendering library. 'bokeh' might fail if the module is not installed.

    Returns
    -------
    output : `bokeh.models.layouts.Column` or `None`
        A bokeh object containing the layout of the plot, when ``show=False``,
        None otherwise.
    """

    # TODO: put matplotlib rendering outsize. It has to return the figure if show=False
    # TODO: add a unittest
    if titles is not None:
        if len(ys) != len(titles):
            raise ValueError('Length of ``titles`` differs from the length of '
                             '``ys``')
    if rendering == 'matplotlib':
        import matplotlib.pyplot as plt
        x_range = None
        y_range = None
        fig = plt.figure(figsize=(8, 2.5 * len(ys)))
        for idx, y in enumerate(ys):
            if titles is not None:
                title = titles[idx]
            else:
                title = None
            ax = plt.subplot(len(ys), 1, idx + 1)
            fig = plt.stem(y, title=title, x_range=x_range, y_range=y_range)
            if title is not None:
                plt.title(title, fontsize=18)
        plt.tight_layout()
        if show:
            plt.show()
            return None
        else:
            return ax
    elif rendering == 'bokeh':
        return stems_bokeh(ys, titles, show, sync_axes)
    else:
        raise ValueError("Unknown rendering type. Expected 'matplotlib' or "
                         "'bokeh', received %s" % rendering)
