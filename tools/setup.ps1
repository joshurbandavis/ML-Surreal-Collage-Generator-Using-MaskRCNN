# This file is from https://git.corp.adobe.com/euclid/python-project-scaffold

Write-Host "Current Path: $ENV:PATH"

Write-Host "Current Directory"
Get-ChildItem

## If conda is globally already available just use it
if ( -not(Get-Command "conda" -ErrorAction SilentlyContinue) ) {

    # if it is already downloaded, don't redownload
    if( -not(Test-Path ".miniconda3\shell\condabin\conda-hook.ps1" -PathType Leaf) ) {
        ## Download miniconda3 installer&
        $AllProtocols = [System.Net.SecurityProtocolType]'Ssl3,Tls,Tls11,Tls12'
        [System.Net.ServicePointManager]::SecurityProtocol = $AllProtocols
        $SCRIPT="Miniconda3-latest-Windows-x86_64.exe"
        $URL="https://repo.anaconda.com/miniconda/$SCRIPT"
        Invoke-WebRequest -Uri $URL -OutFile "$SCRIPT"

        ## Install
        Write-Host "Installing conda locally"
        # The -Wait is important
        Start-Process -Wait -FilePath "$SCRIPT" -ArgumentList "/S","/AddToPath=0","/RegisterPython=0","/D=${PWD}\.miniconda3"
        Remove-Item -force "$SCRIPT"
        if( -not $? ) { Write-Host "Failed to install miniconda"; exit -1 }
    }

    # Activating conda
    & ".\.miniconda3\shell\condabin\conda-hook.ps1"
}

#conda init
Write-Host "Status of conda executable"
Get-Command conda

#Activate conda env
conda config --set ssl_verify no
# ask conda to show folder name instead of tag or abs path for envs in non default location.
conda config --set env_prompt '({name}) '

if( -not $? ) { exit -1 }
conda env update $ENV:CONDA_DEBUG_FLAG --prefix .venv\ --file "tools\conda.yaml"
if( -not $? ) { exit -1 }
conda activate .venv\
if( -not $? ) { exit -1 }

# Install package in dev mode
pip install -e .
if( -not $? ) { exit -1 }

# store the path to the conda installed python
# this will always be there even if you activate the env with conda and not use the script.
conda env config vars set SURREAL_COLLAGE_PYTHON_PATH=$(python -c "import sys; print(sys.executable)")
if( -not $? ) { exit -1 }
conda deactivate  # this will throw a harmless error about Remove-Item https://github.com/conda/conda/issues/10126
if( -not $? ) { exit -1 }

# The first time the env var is set, it won't be visible until the env
# is refreshed
conda activate .venv\
if( -not $? ) { exit -1 }
