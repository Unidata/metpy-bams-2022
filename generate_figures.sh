#!/bin/bash
conda run -n bams-manuscript python scripts/fig1_skewt.py &
conda run -n bams-manuscript python scripts/fig2_multilayer.py &
conda run -n bams-manuscript python scripts/fig3_cross_section.py &
conda run -n bams-manuscript python scripts/fig5_declarative.py &
conda run -n bams-manuscript python scripts/fig6_plotgeometry.py &
wait
