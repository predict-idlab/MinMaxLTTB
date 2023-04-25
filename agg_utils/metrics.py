from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.ndimage as ndi
import scipy.signal as ss
from skimage.metrics import structural_similarity as ssim

from .path_conf import figure_root_dir


def get_data_path(data, n, n_out, aggregator, **kwargs):
    return figure_root_dir / (
        f"data/{data}_{aggregator}_{n}"
        + (f"{('_' + str(n_out)) if aggregator != 'reference' else ''}" + ".parquet")
    )


def get_series(aggregator, data, n, n_out=None, **kwargs) -> pd.Series:
    df = pd.read_parquet(get_data_path(data, n, n_out, aggregator, **kwargs))
    df = df.set_index(df.columns[0])
    return df.iloc[:, 0]


def get_png_path(
    toolkit,
    data,
    n,
    n_out,
    aggregator,
    line_width,
    line_shape,
    aa: bool = False,
    **kwargs,
):
    aa = "_aa" if aa else ""
    return figure_root_dir / (
        f"{toolkit}/{aggregator}_{data}_{n}"
        + f"{('_' + str(n_out)) if aggregator != 'reference' else ''}"
        + f"_ls={line_shape}_lw={line_width}{aa}.png"
    )


def _get_or_conv_mask(img1, img2, win_size: int = 11):
    """Return the OR convolution mask."""
    joined = (img1 + img2) > 0
    # ss.convolve2d(joined, np.ones((win_size, win_size)), mode="same") != 0
    # The above 2d conv is equivalent to applying the following 1d convs
    # which is ~15x faster than the 2d conv
    out = ndi.convolve1d(joined > 0, np.ones(win_size), axis=0, mode="reflect")
    out = ndi.convolve1d(out, np.ones(win_size), axis=1, mode="reflect") > 0
    return out


def _get_dssim_series(agg, ref, dim, or_conv_mask, **ssim_kwargs) -> pd.Series:
    # calculate the SSIM, OR convolution mask, and DSSIM
    ssim_kwgs = dict(win_size=11, full=True, gradient=False)
    ssim_kwgs.update(ssim_kwargs)

    SSIM = ssim(ref[:, :, dim], agg[:, :, dim], **ssim_kwgs, data_range=255)[1]

    # Compute hte (masked) DSSIM, and mask the SSIM as well
    DSSIM = (1 - SSIM) / 2
    DSSIM_masked = DSSIM.ravel()[or_conv_mask.ravel()]
    SSIM_masked = SSIM.ravel()[or_conv_mask.ravel()]

    return pd.Series(
        index=["DSSIM", "DSSIM_masked", "SSIM", "SSIM_masked"],
        data=[
            np.mean(DSSIM),
            np.mean(DSSIM_masked),
            np.mean(SSIM),
            np.mean(SSIM_masked),
        ],
    )


def _get_mse_series(agg, ref, dim, or_conv_mask) -> pd.Series:
    SE = ((agg[:, :, dim] - ref[:, :, dim])) ** 2

    # note: we cast the data to avoid rounding errors when computing the Pixel errors
    # which are derived from the MAE
    AE = np.abs((agg[:, :, dim] - ref[:, :, dim])).astype(int)

    # Illumination errors
    IE = (agg[:, :, dim] > 0) != (ref[:, :, dim] > 0)
    IE_10 = (agg[:, :, dim] > 10) != (ref[:, :, dim] > 10)
    IE_20 = (agg[:, :, dim] > 20) != (ref[:, :, dim] > 20)
    IE_50 = (agg[:, :, dim] > 50) != (ref[:, :, dim] > 50)

    MSE = np.mean(SE)
    MSE_masked = SE.ravel()[or_conv_mask.ravel()].mean()
    MAE = np.mean(AE)
    MAE_masked = AE.ravel()[or_conv_mask.ravel()].mean()

    return pd.Series(
        index=[
            "MSE",
            "MSE_masked",
            "MAE",
            "MAE_masked",
            "conv_mask_size",
            "pixel_errors",
            "pixel_errors_margin_10",
            "pixel_errors_margin_20",
            "pixel_errors_margin_30",
            "pixel_errors_margin_50",
            "pixel_errors_margin_75",
            "pixel_errors_margin_100",
            "illumination_error",
            "illumination_error_margin_10",
            "illumination_error_margin_20",
            "illumination_errror_margin_50",
        ],
        data=[
            MSE,
            MSE_masked,
            MAE,
            MAE_masked,
            or_conv_mask.sum(),
            (AE != 0).sum(),
            (AE > 10).sum(),
            (AE > 20).sum(),
            (AE > 30).sum(),
            (AE > 50).sum(),
            (AE > 75).sum(),
            (AE > 100).sum(),
            IE.sum(),
            IE_10.sum(),
            IE_20.sum(),
            IE_50.sum(),
        ],
    )
