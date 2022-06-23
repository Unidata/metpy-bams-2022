#!/bin/bash
cd ./scripts
conda run -n bams-manuscript python fig1_skewt.py &
conda run -n bams-manuscript python fig2_multilayer.py &
conda run -n bams-manuscript python fig3_cross_section.py &
conda run -n bams-manuscript python fig5_declarative.py &
conda run -n bams-manuscript python fig6_plotgeometry.py &
wait
