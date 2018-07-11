#Use a Control script to start and run the simulation, you can also do this directly via console comands (obviously :-P)
from car_fuzzy_simulation import simulation_enviroment as env

sim = env() #Construct a simulation_envicoment object form the imported class

#Lets do some parameter studies and compare the results, for example lets run simulations for different averaging ranges for the fuzzy-output

import matplotlib.pyplot as plt #Required for plotting the results
plots = [] #Container that holds the plots (ideally i want to merge them into a big subplot at the end, found no good solution so far)

values = [1,5,20] #List of values to iterate over

for idx, value in enumerate(values):
    print('Simulation {} of {}...'.format(idx+1,len(values))) #Print to console where we are
    sim.K_i = value #Change some simulation parameters depending on the list of values, in this case try different parameters for the PID-controlers proportional gain.
    sim.run_simulation() #Run the simulation
    plots.append(sim.show_plots('PID Controler Diagram',expand_title='/ PID-Controler P-Gain is {}'.format(value),return_figure_object=True)) #Specify that we are only interested in the 'Motor Power Diagram' and dump the processed figure in the container 'plots' for use later on
print('Simulations are done, now lets take a look at the results.')

#Have not yet found a good solution to combine all figures into one big subplot
for fig in plots: #Iterate over all generated figures
    fig.show() #Plot the figure
