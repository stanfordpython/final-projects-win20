
Lindsey Engel - lindseye@stanford.edu 

Class: CS 41
Date: March 8, 2020
File Name: CombinedCycleJN.ipynb
Format: Jupyter Notebook


In this project, I wanted to use Cantera (https://cantera.org/) based Python to do an analysis on a combined cycle power plant. 

Cantera:  
Cantera is an add-on program to do thermodynamic analysis. It can be used to model physical energy systems by initializing and solving for thermodynamic properties at various states. Cantera uses "fluid" objects that the programmer can operate on, setting gas chemical composition, pressures, temperatures, enthalpies (a form of energy), and entropies based on known or measurable conditions. Cantera establishes new thermodynamic states through the numeric minimization of the Helmholtz fundamental relation. 


Combined Cycle: 
A combined cycle consists of a gas turbine cycle where waste heat is used to heat up steam in a steam turbine cycle. Good diagrams on: http://sounak4u.weebly.com/vapour--combined-power-cycle.html

 In the gas turbine cycle, air and fuel (natural gas) are separately pressurized and then injected into a combustion chamber where they are combined and combusted. At this point, the hot and high pressure exhaust is expanded through a turbine to extract work (to both power the compressors, and to send electricity to the grid). The exhaust gas out of the turbine is still hot and still has sufficient energy, so we will send that gas through a heat exchanger to heat up some water in the steam cycle. 

In this problem, we are restricted by the maximum temperature of the turbine inlet (due to material melting and failure temperatures). As such, we define the exit temperature of the combustor/ inlet to the turbine, and will iterate on the moles of fuel to the moles of air that we put into our combustor, until it gives us the maximum temperature of the combustor exit. 


We can assess the system by looking at the change in entropy between states. By the second law of thermodynamics, entropy is always generated and increasing in the universe, so theoretically we would want to minimize changes in entropy through out this system. To normalize it, I plotted temperature versus fuel-specific entropy (entropy per kg of fuel added). The fuel and gas initially start at lower entropies, but through the process continue to increase in entropy. 

Efficiency of this system can be measured on a lower heating value (LHV) basis. LHV is defined to be the amount of energy stored in chemical bonds of a fuel compared to energy of chemical bonds in the products that they would form after combustion. We will define efficiency to be: efficiency = Work output / LHV. 


In the steam cycle, liquid water is pumped to increase its pressure. It is then sent through a heat exchanger where heat from the still hot gas turbine exhaust is transferred to the water to evaporate it and to increase its temperature. The water, now at a high temperature, high pressure, and in the vapor phase, is expanded through a steam turbine to extract work output. The water is then sent through a condenser to bring it back to the liquid phase, where it is pumped back to atmospheric pressure. 

In this cycle, the major constraints are on the turbine exit quality (a measure of how much vapor is in the liquid-vapor mixture), and on the pinch point inside the heat exchanger. Due to material constraints, the quality of the steam cannot dip below about 88% (mass percent of vapor compared to total mass). Using this, we will iterate to find a pump pressure that will give us the proper temperature and pressure at the inlet of the turbine. After we have found that pressure, we will use the pinch point of the heat exchanger (a measure of how much heat can be transferred from the gas to the water based on temperature differences) to iterate to find the necessary mass flow rate. At this point, we have solved for the thermodynamic state at each component. 

We will will now track how energy (in the form of enthalpy - h ) changes through the whole cycle, normalizing both cycles by their hottest and most energetic states (after the combustor and after the heat exchanger for the gas and steam cycles respectively). We will again measure efficiency on an LHV basis, but this time, using the net work output from both the gas turbine cycle and the steam turbine cycle. Adding the steam cycle gives us an efficiency of 48% versus the 30% efficiency of the gas turbine alone. 


Code Overview:
As a whole, the code systematically steps through each component listed in the sections above. I wrote a few functions to help solve for certain states, namely polytropicEfficiency and getInletTemp. Turbomachinery components are often rated by their polytropic efficiency, so these two functions help work through these components and account for their non-ideality. I recognize that this code might not be particularly "pythonic." I also wrote a small class to help me store state variables for each particular station in this analysis. 

In addition to Cantera used numpy to create vectors, and matplotlib to visualize and plot the data. 

I definitely had trouble keeping style in check as doing multiple iterative solutions within one analysis can get messy very quickly. Though in my experience in mechanical engineering, functionality almost always trumps style, so my apologies for messier code. It's a skill I have not developed well. But my main goal for this assignment was to successfully do an energy systems analysis using Python based Cantera, so goal achieved! 


Requirements and Installation instructions:
This code requires the installation of Cantera (https://cantera.org/install/index.html). Instructions are for MacOS, but Windows instructions are available on the Cantera website). 

1) download miniconda:  (full instructions: https://cantera.org/install/macos-install.html)
	in terminal run:
	
	cd Downloads
	curl https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o miniconda.sh;
	bash miniconda.sh

2) create an environment for Cantera (full instructions: https://cantera.org/install/conda-install.html#sec-install-conda)
	in terminal run:

	conda create --name spam --channel cantera cantera ipython matplotlib

3) activate environment for Cantera
	in terminal run:

	conda create --name spam --channel cantera cantera ipython matplotlib

4) Add Jupyter Notebook to the same location as the Cantera environment that you just created (full instructions: https://jupyter.org/install)
	in terminal run:	

	conda install -c conda-forge notebook

5) Ensure that the CombinedCycleJN.ipynb file is in the location of the Cantera environment.
If the instructions are followed above, by default, a miniconda3 folder will be added to your home directory. In it: open 'envs' and then 'spam'. The file should be located in 'spam'


Known bugs:
Since this code is often updating the same thermodynamic state values, just running a single kernel can often overwrite previously found values. The code will run properly if it is run from the top each time. 

Publishing and Sharing :
Any and all of this assignment can be posted to the CS 41 site. 

Credit/ Acknowledgements:
The specs for this system were provided from ME 370b, Energy Systems II- Modeling and Advanced Concepts, taught by Professor Chris Edwards. 

Maintainer:
Lindsey Engel - reachable indefinitely at lindze4@gmail.com

