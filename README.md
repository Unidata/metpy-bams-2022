# metpy-bams-2022

## Figure generation for the 2022 Bulletin of the American Meteorology Society article on MetPy

### :open_book: Instructions

Set up an environment using [conda](https://docs.conda.io/en/latest/miniconda.html) and the provided `environment.yml`,

```shell
conda env create .
```

and use the bash script `generate_figures.sh` to run the separate Python scripts for generating the figures. Note that `scripts/fig2_multilayer.py` generates a plot with near-real-time satellite imagery.


### :warning: Maintenance

These workflows may undergo slight changes in the spirit of reusability by the BAMS community. Please check out the [list of closed pull requests](https://github.com/Unidata/metpy-bams-2022/pulls?q=is%3Apr+is%3Aclosed) for a history of changes since publication.

Some of the published figures may reflect data that was current at the time and date of original generation. Re-generating these figures will result in different images.
