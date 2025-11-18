# SAT-PQH: A Proactive, Seamless Post-Quantum Handover Architecture for LEO Satellite Mega-Constellations

This repository contains the simulation framework and experimental results for the research paper proposing **SAT-PQH**, a novel post-quantum secure handover protocol tailored for LEO satellite mega-constellations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 1. Introduction

The advent of quantum computers poses a significant threat to classical cryptography currently used in satellite communication networks. The "harvest now, decrypt later" attack vector is particularly concerning for satellites, which have long operational lifecycles. This project addresses the critical challenge of performing secure and efficient user handovers in LEO (Low Earth Orbit) mega-constellations within a post-quantum cryptographic (PQC) framework.

We introduce **SAT-PQH**, a proactive handover protocol that minimizes latency and computational overhead by leveraging the predictable nature of satellite orbits. This simulation framework is designed to evaluate the performance of SAT-PQH against traditional handover schemes under various network conditions.

## 2. Project Structure

The repository is organized as follows to maintain a clean and scalable codebase:

```
pqc-satellite-handover/
├── .gitignore              # Specifies intentionally untracked files to ignore
├── README.md               # This file
├── environment.yml         # Conda environment definition for reproducibility
├── data/                   # Input data for the simulation (e.g., TLE files)
├── notebooks/              # Jupyter notebooks for exploratory analysis and visualization
├── results/                # Simulation outputs (plots, tables, logs)
├── scripts/                # Standalone Python scripts for running experiments
└── src/                    # Main source code of the simulation framework
    ├── config.py           # Global configurations and parameters
    ├── core/               # Core components of the simulation environment
    │   ├── satellite.py    # Satellite and Constellation classes
    │   ├── user.py         # Ground User and mobility models
    │   └── channel.py      # Communication channel model (latency, bandwidth)
    ├── crypto/             # PQC algorithm handlers
    │   └── pqc_handler.py  # Wrapper for OQS library operations
    ├── protocols/          # Implementation of handover protocols
    │   ├── baseline_handover.py # Naive PQC handover implementation
    │   └── sat_pqh_protocol.py  # Our proposed SAT-PQH protocol
    └── simulation/         # Main simulation logic
        ├── simulator.py    # The event-driven simulation engine
        ├── metrics.py      # Classes for collecting performance metrics
        └── logger.py       # Configuration for logging
```

## 3. Setup and Installation

Follow these steps to set up the project environment. A Conda package manager is required.

**1. Clone the Repository**
```bash
git clone https://github.com/ailabteam/pqc-satellite-handover.git
cd pqc-satellite-handover
```

**2. Create and Activate the Conda Environment**

This project uses a dedicated Conda environment to ensure all dependencies are managed correctly. The environment is defined in the `environment.yml` file.

```bash
# Create the conda environment named 'sat-pqh-env'
conda env create -f environment.yml

# Activate the environment
conda activate sat-pqh-env
```
_All subsequent commands should be run within this activated environment._

**3. Download Satellite Data**

The simulation requires Two-Line Element set (TLE) data to calculate satellite orbits.
- Go to [CelesTrak](https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle).
- Copy the entire content.
- Paste it into a new file located at `data/raw/starlink.tle`.

## 4. Usage

The project is primarily run through scripts located in the `/scripts` directory.

**1. Benchmark PQC Algorithms**

To get a baseline of the performance of the underlying PQC algorithms on your machine, run:
```bash
python scripts/benchmark_pqc.py
```

**2. Run a Simulation**

To execute the main handover simulation, use the `run_simulation.py` script. (This will be configured later).
```bash
python scripts/run_simulation.py --protocol SAT-PQH --num-users 1000
```

## 5. Contributing

(Optional: Can be filled in later if the project becomes collaborative)

## 6. License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
````

#### **C. File `environment.yml` và `.gitignore`**

Nội dung của hai file này mà chúng ta đã thống nhất ở lần trao đổi trước là rất tốt và không cần thay đổi. Tôi xin nhắc lại ở đây để đảm bảo tính nhất quán.

**`environment.yml`**
```yaml
name: sat-pqh-env
channels:
  - pytorch
  - nvidia
  - conda-forge
  - defaults
dependencies:
  - python=3.12
  - pip
  # Core numerical and data handling
  - numpy
  - pandas
  - scipy
  # GPU computing (CuPy is a great choice for NumPy on GPU)
  - cupy
  # Satellite orbit simulation
  - skyfield
  # Network simulation
  - simpy
  # Visualization
  - matplotlib
  - seaborn
  - plotly
  # Progress bars
  - tqdm
  # PQC Library (will be installed via pip)
  - pip:
    - oqs
```

**`.gitignore`**
```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Conda environment files
.conda/

# Jupyter Notebook checkpoints
.ipynb_checkpoints/

# Sensitive files
.env

# Data, results, and logs (can be large)
data/
results/
logs/

# IDE settings
.vscode/
.idea/
.DS_Store
```

