# COMPAS Setup Guide for Windows 11

### Navigation

- [Section 1: Windows Subsystem for Linux (WSL)](#section-1-windows-subsystem-for-linux-wsl)
- [Section 2: Visual Studio Code (VS Code)](#section-2-visual-studio-code-vs-code)
- [Section 3: VS Code Extensions](#section-3-vs-code-extensions-ctrlshiftx)
- [Section 4: VS Code Workspace](#section-4-vs-code-workspace)
- [Section 5: Install COMPAS Dependencies](#section-5-install-compas-dependencies)
- [Section 6: Clone COMPAS Repository](#section-6-clone-compas-repository)
- [Section 7: Define COMPAS Environment Variable](#section-7-define-compas-environment-variable)
- [Section 8: Build COMPAS](#section-8-build-compas)
- [Section 9: conda-forge Python Environment Manager](#section-9-conda-forge-python-environment-manager)
- [Section 10: Setup (compas_py) Python Environment](#section-10-setup-compas_py-python-environment)
- [Section 11: Install Python Modules to compas_py Environment](#section-11-install-python-modules-to-compas_py-environment)
- [Section 12: Create Jupyter Notebooks](#section-12-create-jupyter-notebooks)
- [Section 13: Mounting External Storage Devices](#section-13-mounting-external-storage-devices)

## Section 1: Windows Subsystem for Linux (WSL)

### Windows Subsystem for Linux (WSL)

1. Right-click the Windows Start menu and select "Terminal (Admin)" to open an elevated terminal.
2. Install WSL: `wsl --install`
    - You may be prompted to restart the machine, in which case you should repeat the above steps.
    - This will enable WSL and install the Ubuntu distribution of Linux.
3. You will then be prompted to create a new Linux user account and password.

## Section 2: Visual Studio Code (VS Code)

### Check System Type (CPU Architecture)

1. Right-click the Windows Start menu and select "Settings".
2. Navigate to System > About.
3. Under Device Info, it is displayed next to System Type.

### Install VS Code

1. Install [Visual Studio Code](https://code.visualstudio.com/Download).
2. Select Windows User Installer.
    - Choose x64 for x86_64 architecture, or Arm64 for aarch64 architecture.
3. During installation, verify that VS Code is added to PATH.

## Section 3: VS Code Extensions

### Connect VS Code to WSL

1. Open the Extensions tab (Ctrl+Shift+X).
2. Search and install "WSL" extension.
3. Open Command Palette (Ctrl+Shift+P or F1).
4. Search and select "WSL: Connect to WSL".

### Install Extensions for Working with Python and Jupyter Environments

- Python
    - Pylance
    - Python Debugger
    - Python Environments

- Jupyter
    - Jupyter Keymap
    - Jupyter Notebook Renderers
    - Jupyter Slide Show
    - Jupyter Cell Tags

## Section 4: VS Code Workspace

### Create New Workspace 

1. Open Explorer tab (Ctrl+Shift+E).
2. File > Open Folder...
3. /home/your-linux-username
4. File > Save Workspace As...
5. /home/your-linux-username/your-workspace-name.code-workspace

## Section 5: Install COMPAS Dependencies

1. Open a new terminal in VS Code (Ctrl+Shift+`).
2. Update Ubuntu package lists: `sudo apt-get update`
3. Upgrade packages, if applicable: `sudo apt-get upgrade`
4. Install C++ compiler and its make command, and the boost, gsl, and hdf5 library packages:

        sudo apt-get install g++ make libboost-all-dev libgsl-dev libhdf5-dev

## Section 6: Clone COMPAS Repository

1. Toggle open the terminal in VS Code (Ctrl+`).
2. Change to home directory: `cd ~`
3. Make new directory for repositories: `mkdir repositories`
4. Change to repositories directory: `cd ~/repositories`
5. Clone COMPAS repository: `git clone https://github.com/TeamCOMPAS/COMPAS`

## Section 7: Build COMPAS

#### *Note for aarch64 Systems:* For those with aarch64 instead of x86_64 CPU architecture, please perform the following modification:

1. Open terminal (Ctrl+`).
2. Open COMPAS source code Makefile: `nano ~/repositories/COMPAS/src/Makefile`
3. Toggle Replace (Ctrl+\\).
4. Search (to replace): `x86_64`
5. Replace with: `aarch64`
6. Toggle to replace all instances (A).
7. Exit Nano (Ctrl+X).
8. Save modified buffer (Y).

### Build COMPAS Source Code

1. Open terminal (Ctrl+`).
2. Change to COMPAS source code directory: `cd ~/repositories/COMPAS/src`
3. Clean lingering builds of COMPAS: `make clean`
4. Build COMPAS in parallel using (4) CPU threads: `make -j4`
    - Not recommended to build with more than 4 since the compilation has high RAM consumption.

## Section 9: conda-forge Python Environment Manager

### Download conda-forge Python environment manager with the Miniforge3 installer:

#### x86_64 Architecture

    wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh

    bash Miniforge3-Linux-x86_64.sh

    source ~/.bashrc

#### aarch64 Architecture

    wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh

    bash Miniforge3-Linux-aarch64.sh

    source ~/.bashrc

## Section 10: Setup (compas_py) Python Environment

1. Open terminal (Ctrl+`).
2. Update Conda package lists: `conda update --all`
3. Upgrade Conda packages, if applicable: `conda upgrade --all`
4. Disable automatic activation of (base) environment: `conda config --set auto_activate false`
5. Create new (compas_py) environment: `conda create -n compas_py`
6. Append (compas_py) environment activation script to .bashrc file:

        echo >> ~/.bashrc

        echo '# Activate compas_py Environment' >> ~/.bashrc

        echo '# Only uncomment the last line of this block if Python > Terminal: Activate Environment is disabled.' >> ~/.bashrc
        
        echo '# Can be accessed in VS Code settings (Ctrl + ,) by searching "python.terminal.activateEnvironment".' >> ~/.bashrc

        echo 'conda activate compas_py' >> ~/.bashrc

        echo >> ~/.bashrc

7. Reload terminal: `source ~/.bashrc`

### *IF Python extension is enabled:*

1. Open VS Code Settings (Ctrl + ,).
2. Search "python.terminal.activateEnvironment"
3. Disable "Python > Terminal: Activate Environment"

### *IF Pylance extension is enabled:*

1. Open Command Palette (Ctrl+Shift+P or F1)
2. Search "Python: Select Interpreter"
3. Select "Python version-here (compas_py) ./miniforge3/envs/compas/bin/python"

## Section 11: Install Python Modules to (compas_py) Environment

### Install Python Package Installer (pip): `conda install pip`

### Install Python Packages

- **Astropy**: `pip install astropy` (astrophysics library)
    - Installs the following dependencies:
        - NumPy
        - packaging
        - PyERFA
        - PyYAML
- **SciPy**: `pip install scipy` (scientific library)
    - Installs the following dependencies:
        - NumPy
- **Matplotlib**: `pip install matplotlib` (provides plotting functionality)
    - Installs the following dependencies:
        - ContourPy
        - cycler
        - fontTools
        - Kiwisolver
        - NumPy
        - packaging
        - pillow
        - PyParsing
        - python-dateutil
        - six
- **h5py**: `pip install h5py` (read/write `Table` objects from/to HDF5 files)
    - Installs the following dependencies:
        - NumPy
- **pandas**: `pip install pandas` (convert `Table` objects from/to pandas DataFrame objects)
    - Installs the following dependencies:
        - NumPy
        - python-dateutil
        - pytz
        - six
        - tzdata
- **ipykernel**: `pip install ipykernel` (interact with Jupyter kernels within VS Code)
    - Installs the following dependencies:
        - asttokens
        - comm
        - debugpy
        - decorator
        - executing
        - ipython
        - ipython_pygments_lexers
        - jedi
        - jupyter_client
        - jupyter_core
        - matplotlib-inline
        - nest-asyncio
        - packaging
        - parso
        - pexpect
        - platformdirs
        - prompt_toolkit
        - psutil
        - ptyprocess
        - pure_eval
        - Pygments
        - python-dateutil
        - pyzmq
        - six
        - stack-data
        - tornado
        - traitlets
        - wcwidth

## Section 12: Create Jupyter Notebooks

### Create Notebooks Directory

1. Open terminal (Ctrl+`).
2. Change to home directory: `cd ~`
3. Make new directory for notebooks: `mkdir notebooks`
4. Change to notebooks directory: `cd ~/notebooks`

### Create Jupyter Notebook

1. Open Explorer (Ctrl+Shift+E).
2. File > New File... 
3. your-filename.ipynb
4. Select newly created file to open.
5. In the top-right section of notebook, choose "Select Kernel" or "Detecting Kernels".
6. Select Kernel > Python Environments... > compas_py (Python <version#>) miniforge3/envs/compas_py/bin/python

## Section 13: Mounting External Storage Devices

1. Open terminal (Ctrl+`).
2. Mount external storage device on Windows D: drive:
    - `sudo mount -t drvfs D: /mnt/d`
    - `sudo mount -t drvfs E: /mnt/e`
    - etc.
