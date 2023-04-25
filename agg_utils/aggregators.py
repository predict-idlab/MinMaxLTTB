"""
Tweaked implementations of aggregators with the aim of more convenient Benchmarking
"""

import pandas as pd
from plotly_resampler.aggregation import (
    LTTB,
    AbstractSeriesAggregator,
    MinMaxAggregator,
)


class MinMaxLTTB(AbstractSeriesAggregator):
    """Efficient version off LTTB by first reducing really large datasets with
    the :class:`MinMaxAggregator <MinMaxAggregator>` and then further
    aggregating the reduced result with :class:`LTTB <LTTB>`.

    .. note::
        This implementation enforces the usage of the ``MinMaxAggregator``
    """

    def __init__(self, interleave_gaps: bool = True, nan_position: str = "end"):
        """
        Parameters
        ----------
        interleave_gaps: bool, optional
            Whether None values should be added when there are gaps / irregularly
            sampled data. A quantile-based approach is used to determine the gaps /
            irregularly sampled data. By default, True.
        nan_position: str, optional
            Indicates where nans must be placed when gaps are detected. \n
            If ``'end'``, the first point after a gap will be replaced with a
            nan-value \n
            If ``'begin'``, the last point before a gap will be replaced with a
            nan-value \n
            If ``'both'``, both the encompassing gap datapoints are replaced with
            nan-values \n
            .. note::
                This parameter only has an effect when ``interleave_gaps`` is set
                to *True*.

        """
        self.lttb = LTTB(interleave_gaps=False)
        self.minmax = MinMaxAggregator(interleave_gaps=False)
        super().__init__(
            interleave_gaps,
            nan_position,
            dtype_regex_list=[rf"{dtype}\d*" for dtype in ["float", "int", "uint"]]
            + ["category", "bool"],
        )

    def _aggregate(
        self, s: pd.Series, n_out: int, minmax_ratio: int = 4
    ) -> pd.Series:
        """Compute the aggregation of the series.

        .. Note::
            A minmax_ratio of 1 is equivalent to the MinMaxAggregator.
        """
        s = self.minmax._aggregate(s, n_out * minmax_ratio)
        if len(s) <= n_out: # Return
            return s
        return self.lttb._aggregate(s, n_out)
