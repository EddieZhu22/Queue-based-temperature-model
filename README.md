# Queue-based Temperature Model
## Table Of Contents
- [Description](#description)
- [Getting Started](#getting-started)
- [Code Structure](#code-structure)
- [References](#references)
- [License](#license)


## Description
This is a repository is for the Queue-based Temperature Model (QTM). Based on traffic flow theory and fluid approximation queuing theory, this model highlights a simplified version of the world's atmosphere and the relationships between solar radiation and total solar energy to draw several useful inferences about the system's performance, resilience, and adaptability.

### MODEL
The model first takes in solar radiation & temperature data from a data source. Data for a case study done from 2022-2023 used 2019 NSRDB[1] data to attain a modelled 2-meter height and spatially homogeneous gridded dataset usable for the model. 

Then, the model is split into 2 steps:

**QTM STEP 1** - generates general sub-mesoscale system dynamics (Queue, inflow, outflow)

**QTM STEP 2** - turn these sub-mesoscale system dynamics into something meaningful (mesoscale indicators)


A table describing the equations & symbols used in this model are shown in these tables:
![GitHub Logo](https://github.com/EddieZhu22/Queue-based-temperature-model/blob/master/images/Picture1.png)

## Getting Started
1. Clone the repository to your local machine using git clone https://github.com/YOUR_USERNAME/REPO_NAME.git.
2. Navigate to the repository directory using cd REPO_NAME.
3. Install the necessary dependencies using pip install -r requirements.txt.
4. Run the code in Queue-based_Temperature_Model.py

## Code Structure
The code is split up into folders: Data Collection, QueueBasedTemperatureModel, and spatial regression.

## References
[1] NSRDB https://nsrdb.nrel.gov/
