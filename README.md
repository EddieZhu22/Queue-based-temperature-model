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

### ABSTRACT
Extreme heat events have risen dramatically in the past decades. Understanding underlying interactions within the built environment has become increasingly imperative for developing measures to mitigate the impact of extreme heat. While researchers primarily use Partial Differential Equations (PDEs) to analyze extreme heat, PDE-based analysis overlooks dynamics at individual locations. The proposed Queue-based Temperature Model (QTM), on the other hand, is designed to provide a theoretically rigorous framework and closed-form solutions to capture intraday energy flow dynamics under extreme heat conditions with little computational resources. The model offers a way of using Ordinary Differential Equations based on Fluid Queuing Theory where the inflow and outflow of energy serve as the derivatives for the total energy within the system (Queue). This study used 2-meter height air temperatures and GHI of Maricopa County in 2019. After capturing the heat exchange dynamics using the QTM, the model was used to derive several closed-form expressions. The model had an 11.29% MAPE (n=419,830) when comparing estimated heat exposure duration (P) to observed values using log-transformed sensitivity analysis, suggesting that the model outputs work well for extreme heat conditions. Then, several covariates known to correlate with extreme heat were tested with Multi-Scale Geographically Weighted Regression. Normalized Difference Vegetation Index and urban land cover indicated statistically significant coefficients with model outputs. The QTM provides a reliable, efficient and economical alternative to traditional PDE models and can be applied in areas like urban planning, public policy as well as environmental education and research.

A table describing the equations & symbols used in this model are shown below:
![Table](https://github.com/EddieZhu22/Queue-based-temperature-model/blob/master/Images/Picture1.png)

## Getting Started
1. Clone the repository to your local machine using git clone https://github.com/YOUR_USERNAME/REPO_NAME.git.
2. Navigate to the repository directory using cd REPO_NAME.
3. Install the necessary dependencies using pip install -r requirements.txt.
4. Run the code in Queue-based_Temperature_Model.py

## Code Structure
The code is split up into folders: Data Collection, QueueBasedTemperatureModel, and spatial regression.

## References
[1] NSRDB https://nsrdb.nrel.gov/
