# Queue-based Temperature Model
## Table Of Contents
- [Description](#description)
- [Getting Started](#getting-started)
- [Code Structure](#code-structure)
- [References](#references)
- [License](#license)


## Description
This is a repository is for the Queue-based Temperature Model (QTM). Based on traffic flow theory and fluid approximation queuing theory, this model highlights a simplified version of the world's atmosphere and the relationships between solar radiation and total solar energy to draw several useful inferences about the system's performance, resilience, and adaptability.

### Model Overview
The model first takes in solar radiation & temperature data from a data source. Data for a case study done from 2022-2023 used 2019 NSRDB[1] data to attain a modelled 2-meter height and spatially homogeneous gridded dataset usable for the model. 

Then, the model is split into 2 steps:

**QTM STEP 1** - generates general sub-mesoscale system dynamics (Queue, inflow, outflow)

**QTM STEP 2** - turn these sub-mesoscale system dynamics into something meaningful (mesoscale indicators)

A table describing the equations & symbols used in this model are shown below:
![Table](https://github.com/EddieZhu22/Queue-based-temperature-model/blob/master/Images/Picture1.png)

Background Information: The Queue-based Temperature Model (QTM) is inspired by Newell’s fluid queueing model [2] and the Queue Volume Delay Function’s meso-macro framework [3], which offer the theoretical foundation for the model's underlying principles. The QTM consists of a two-step process. In the first step, sub-mesoscale system dynamics present within each day are obtained. In the second step, these dynamics are leveraged to make inferences on the mesoscale level. This allows for the analysis of the system at different levels of fidelity, providing valuable insights into the system's performance, resilience, and adaptability.
Model Framework: In the first step, intraday dynamics of extreme heat are approximated. When the temperature passes through an “extreme heat” cutoff temperature, a queue of energy (Q(t)) starts forming. The queue has two critical components: an inflow and outflow denoted by λ(t) and µ(t) respectively. λ(t) is given by the incoming solar radiation (Global Horizontal Irradiance). µ(t) is the culmination of all factors that release energy out of the system. Because µ(t) is not directly observable, a linear piecewise function is instead used to approximate the behavior. The net flow at a specific time (π(t)) is given by subtracting λ(t) from µ(t). By integrating the net flow, a queue can be calculated. Boundary conditions of the model, t0 and t3, are at the start of the queue and the end of the queue respectively.
In the second step, using the dynamics present in each day and location, several inferences can be made regarding the system. Model outputs include P (heat exposure duration), C (capacity of the system), and D (total inflow demand). Each day these outputs are different, and give a more comprehensive picture of the system’s performance. These indicators can then directly be used in the mesoscale for further analysis.

![image](https://user-images.githubusercontent.com/51139973/228726659-e7ac356c-c3db-49b3-986e-59a898e132b1.png)

In the second step, using the dynamics present in each day and location, several inferences can be made regarding the system. Model outputs include P (heat exposure duration), C (capacity of the system), and D (total inflow demand). Each day these outputs are different, and give a more comprehensive picture of the system’s performance. These indicators can then directly be used in the mesoscale for further analysis.

### QTM STEP 1

#### EQUATIONS: ![image](https://user-images.githubusercontent.com/51139973/228726931-c1b58771-0ab1-4fae-a8c5-4ba51be840c5.png)


## Getting Started
1. Clone the repository to your local machine using git clone https://github.com/YOUR_USERNAME/REPO_NAME.git.
2. Navigate to the repository directory using cd REPO_NAME.
3. Install the necessary dependencies using pip install -r requirements.txt.
4. Run the code in Queue-based_Temperature_Model.py

## Code Structure
The code is split up into folders: Data Collection, QueueBasedTemperatureModel, and spatial regression.

## Acknowledgements
Special thanks to Dr. Zhou & the ASU Transportation AI department for providing continuous support on this project. Thanks to Dr. Zhi Hua Wang and Dr. Gorgescu for providing feedback and giving very professional and useful tips.
## References
[1] NSRDB https://nsrdb.nrel.gov/
[1] Newell, C. (2013). Applications of queueing theory (Vol. 4). Springer Science & Business Media.
[2] Zhou, X. (2022). A meso-to-macro cross-resolution performance approach for connecting polynomial arrival queue            
           model to volume-delay function with inflow demand-to-capacity ratio. Multimodal Transportation, 1(2). 
           https://doi.org/10.1016/j.multra.2022.100017 

