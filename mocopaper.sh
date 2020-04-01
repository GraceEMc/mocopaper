#!/bin/bash

# Generate the results and figures.
python3 code/mocopaper.py

# Compile the paper.
cd paper
pdflatex -interaction=nonstopmode MocoPaper.tex
bibtex MocoPaper
pdflatex -interaction=nonstopmode MocoPaper.tex
pdflatex -interaction=nonstopmode MocoPaper.tex

pdflatex -interaction=nonstopmode MocoPaperAppendix.tex
bibtex MocoPaperAppendix
pdflatex -interaction=nonstopmode MocoPaperAppendix.tex
pdflatex -interaction=nonstopmode MocoPaperAppendix.tex
cd ../

# If this script is being run inside a Docker container, copy certain files
# to a folder that a user could mount from their local file system to export
# the outputs from the Docker container.
if [ -f /.dockerenv ]; then
    cp paper/MocoPaper.pdf /output/
    cp paper/MocoPaperAppendix.pdf /output/
    cp results/* /output/
    cp figures/*.png /output/
    cp figures/*.tiff /output/
fi
