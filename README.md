# metpy-bams-2022

## Figure generation for the 2022 Bulletin of the American Meteorology Society article on MetPy

### :open_book: Instructions

Set up an environment using [conda](https://docs.conda.io/en/latest/miniconda.html) and the provided `environment.yml`,

```shell
conda env create .
```

and use the bash script `generate_figures.sh` to run the separate Python scripts for generating the figures. Note that `scripts/fig2_multilayer.py` generates a plot with near-real-time satellite imagery.
