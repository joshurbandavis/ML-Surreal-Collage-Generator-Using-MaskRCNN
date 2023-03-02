#!/bin/bash

# This file is from https://git.corp.adobe.com/euclid/python-project-scaffold

# This script sets up a conda env for you. If you don't have conda installed,
# it will install one locally for you in .miniconda3 directory.
# Then it will install your dependencies in your conda.yaml and finally it will
# install your package in dev mode in your conda env (so that the package is
# recognized by python without you needing to add things to path everytime)

echo "Working directory"
pwd
set +x

## If conda exists, then don't bother
if ! command -v conda &> /dev/null; then

    # if the conda env exists, don't download
    if [ ! -f ".miniconda3/bin/activate" ]; then
        echo "Getting miniconda"
        if [[ "$(uname -a | cut -d' ' -f1)" == "Darwin" ]]; then
            curl -s -S -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
            SCRIPT=Miniconda3-latest-MacOSX-x86_64.sh
        else
            wget -nv https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
            SCRIPT=Miniconda3-latest-Linux-x86_64.sh
        fi

        echo "Installing conda locally"
        bash "$SCRIPT" -bfp ".miniconda3"
        rm -f "$SCRIPT"
    fi

    # Activating conda
    . ".miniconda3/bin/activate"
fi

# ask conda to show folder name instead of tag or abs path for envs in non default location.
conda config --set env_prompt '({name}) '

conda env update -q $CONDA_DEBUG_FLAG --prefix .venv/ --file "tools/conda.yaml" || exit -1
conda activate .venv/ || exit -1
pip install -e .

# store the path to the conda installed python
# this will always be there even if you activate the env with conda and not use the script.
conda env config vars set SURREAL_COLLAGE_PYTHON_PATH=$(python -c 'import sys; print(sys.executable)')
conda deactivate

# The first time the env var is set, it won't be visible until the env
# is refreshed
conda activate .venv/ || exit -1
