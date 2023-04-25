<div align="center">
<h1>:racehorse: MinMaxLTTB: `TODO fix title` </h1>
</div>

<div align="center">
<img src="gifs/teaser_preselection_ratio.gif" alt="teaser" width="95%"/>
<br></br>
</div>

*Codebase & further details for the paper*:  
> **TODO**  
> Jeroen Van Der Donckt, Jonas Van Der Donckt

<!-- **Preprint**: https://arxiv.org/abs/2304.00900 -->


## Performance of `MinMaxLTTB`

`TODO`

## Visual Representativeness of `MinMaxLTTB`

The visual representativeness is assessed in accordance with https://arxiv.org/abs/2304.00900 

<div align="center">
<img src="gifs/visual_representativeness_preselection_ratio.gif" alt="teaser" width="95%"/>
<br></br>
</div>

**insights**:
- `TODO`: 

---
## How is the repository structured?

- The codebase is located in the `agg_utils` (python scripts) and notebooks folder.
- Additional details can be found in markdown files in the `details` folder.
- Supplementary gifs are located in the `gifs` folder.
- See [notebooks README](notebooks/) for the more details.
  - The `0.*` notebooks contain data parsing and figure generation.
  - The `1.*` notebooks perform the core experiments (visual representativeness and visual stability).
- The `animations` folder contains html animations, which allow to inspect the phenomena in more detail.

Folder structure
```txt
├── agg_utils          <- shared codebase for the notebooks
├── animations         <- html animations
├── details            <- additional details in README.md files
├── gifs               <- supplementary gifs
├── loc_data           <- local data folder 
└── notebooks          <- experiment notebooks see notebooks README.md
```


## How to install the requirements?

This repository uses [poetry](https://python-poetry.org/) as dependency manager.
A specification of the dependencies is provided in the [`pyproject.toml`](pyproject.toml) and [`poetry.lock`](poetry.lock) files.

You can install the dependencies in your Python environment by executing the following steps;
1. Install poetry: https://python-poetry.org/docs/#installation
2. Activate you poetry environment by calling `poetry shell`
3. Install the dependencies by calling `poetry install`

## Utilizing this repository

Make sure that you've extended the [path_conf.py](agg_utils/path_conf.py) file's hostname if statement with your machine's hostname and that you've configured the path to the UCR archive folder.


---

<p align="center">
👤 <i>Jeroen & Jonas Van Der Donckt</i>
</p>
