# What was that bird? Learning driven through Wingspan play

**Author:** Elean Huang  
**Course:** 776500121Y: Big Data II (University of Amsterdam)  
**Date:** 28 March 2026  

---

## Project Overview
This project investigates whether playing the board game *Wingspan* (Hargrave, 2019) drives curiosity-driven information seeking based on the Information Gap Theory of Curiosity (Golman & Loewestein, 2018). An analysis evaluates if recorded Wingspan plays on BoardGameGeek correlate with increased Wikipedia searches for the North American bird species featured in the game, whilst controlling for real-world bird sightings using the eBird API.

The following research question was therefore asked.

**Research Question:** How does the board game Wingspan cause curiosity-driven learning?

---

## Repository Structure
This repo is organised to separate raw data, processing scripts, and the final analysis:

* **[`data/`](./data/)**
    * **[`raw/`](./data/raw/)**: The eBird observation logs and the Wingspan bird list from [coolbutuseless](https://github.com/coolbutuseless/wingspan).
    * **[`processed/`](./data/processed/)**: Cleaned and aggregated datasets for analysis.
* **[`libraries/`](./libraries/)**: Python modules for data extraction:
    * [`retrieve_BGG_data.py`](./libraries/retrieve_BGG_data.py): Retrieves Wingspan play logs via the BGG XML2 API.
    * [`retrieve_ebird_data.py`](./libraries/retrieve_ebird_data.py): Retrieves ecological sightings via the eBird API.
    * [`retrieve_wikipedia_pageviews.py`](./libraries/retrieve_wikipedia_pageviews.py): Retrieves page views via the Wikimedia REST API.
    * [`find_bird_links.py`](./libraries/find_bird_links.py): Maps Wikipedia link connections between bird species for the network analysis.
* **[`notebooks/`](./notebooks/)**:
    * [`analysis.ipynb`](./notebooks/analysis.ipynb): The main notebook containing the Fixed-Effects Panel Regression model and the network analysis.
* **[`tables/`](./tables/)**: Output directory for generated figures, graphs, and descriptive statistics.
* **Root Files**:
    * [`environment.yml`](./environment.yml): Conda environment configuration file containing necessary dependencies.

---

## Setup Instructions
This project uses a Conda environment for dependency management to ensure reproducibility.

1. Clone the repository to your computer.
2. Open a terminal in the project root directory.
3. Create the environment from the configuration file:
   ```bash
   conda env create -f environment.yml
4. Activate the environment
   ```bash
   conda activate bdacaII
   ```

---

## Usage
The seperate modules in [`libraries/`](./libraries/) can be used as follows. Include python3 or python depending on local installations of python. Generally speaking, when constructing the environment through Conda, this should be `python`.

```bash
cd libraries
python module_name.py
```

Modules can also be imported for example as follows (based on Windows)

```python
import os
import sys

sys.path.append(os.path.abspath(".."))
from libraries import module_name
# OR
from libraries.module_name import object
```

### Running the analysis
The full analysis can be ran by opening the [`analysis.ipynb`](./notebooks/analysis.ipynb) jupyter notebook in an editor of your choice and running everything. This notebook assumes that you open it in VSCode, but a standard JupyterLab environment is also functional. The outputs can be seen in [`tables/`](./tables/), which were downloaded from this analysis notebook.

---

## Methodology
1.  **Data Collection:** 30 days of data (22 Feb 2026 up and until 23 Mar 2026) were collected across Wikipedia (page views), BoardGameGeek (play counts), and eBird (real-world sightings).
2.  **Primary Analysis:** A Fixed-Effects Panel Regression model evaluates daily variance in page views relative to a bird's historical average.
3.  **Placebo Test:** A robustness check using a control group of 170 North American birds not featured in the game to ensure observed variance is related to Wingspan.
4.  **Network Analysis:** A network analysis of Wikipedia links between Wingspan birds, which are then clustered using the Louvain community detection algorithm.