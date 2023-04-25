# Main notebooks

**note**: More information regarding the OR-conv mask can be found in [this repository](https://github.com/predict-idlab/ts-datapoint-selection-vis) - [or conv mask section](https://github.com/predict-idlab/ts-datapoint-selection-vis/blob/main/details/OR-conv_masking.md)

| Name | Description |
|----|-------------|
| <h3> :wrench: **Data parsing** </h3> |  |
| [parse DEBS UCR](0.1_Parse_DEBS_UCR_BTC.ipynb) | This notebook parses the [DEBS 2012](https://debs.org/grand-challenges/2012/), [DEBS 2013](https://debs.org/grand-challenges/2013/), [UCR time series archive](https://arxiv.org/abs/1810.07758) CINECG, and a [bitcoin](https://www.kaggle.com/datasets/prasoonkottarathil/btcinusd) dataset. The parsed data is also stored in a more convenient parquet format. |
| [create agg data](0.2_Create_agg_data.ipynb) | This notebook creates and stores the (reference and) aggregated time series for the datasets parsed in the previous notebook. |
| [Aggregated Figure Generation](0.3_Fig_construction.ipynb) | This notebook performs an extensive grid search over the following parameters:<br><br> - Aggregation algorithm (LTTB / MinMaxLTTB / MinMax) <br> - MinMaxLTTB `MinMax preselection ratio` $r_{ps}$. <br> - `n_out`: the number of aggregated datapoints <br> - Template time series and its data size <br> - Visualization toolkit: plotly <br> - Visualization configuration: interpolation = 'linear' line-width = 2 / <br><br> For each combination of parameters, a figure is generated and stored in the [path_conf](../agg_utils/path_conf.py)'s `figure_root_dir` folder. |
| [Figure Metrics computation](0.4_Fig_metrics.ipynb) | This notebook computes the (D)SSIM and MSE metrics for the aggregated figures generated in the previous notebook. Moreover, an `or-conv` mask is utilized to mitigate the variable range that which template time-series span over the image |
| <h3> **core** :camera: </h3> | |
| [Visual Representativeness](1.1_Visual_representativity.ipynb) | This notebook asesses the visual representativeness using the image metrics from the above rows. Specifically this notebook highlights:<br> - The trend of the aggregator performance over `n_out` <br> - Analyzing hte effect of line width and anti-aliasing <br> - Showing toolkit robustness via the noise data <br> - Distribution plots of the aggregator performances <br> - Dynamic frames showing the performance curves for varying `n_out` / line-width / toolkits  |