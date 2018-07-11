#Use a Control script to start and run the simulation, you can also do this directly via console comands (obviously :-P)
#Lets do some parameter studies and compare the results, for example lets run simulations for different averaging ranges for the fuzzy-output
from car_fuzzy_simulation import simulation_enviroment as env
import matplotlib.pyplot as plt #Required for plotting the results

values = [0.05,0.1,0.2,0.5] #List of values to run different simulations for
plots = [] #Container that holds the plots (ideally i want to merge them into a big subplot at the end, found no good solution so far)
sim = [] #Container for all the different simulations

for idx, value in enumerate(values):
    print('Simulation {} of {}...'.format(idx+1,len(values))) #Print to console where we are
    sim.append(env()) #Construct one simulation_envicoment object form the imported class for each individual parameter simulation, so all the results get preserved and we can inspect them afterwards
    sim[idx].K_i = value #Change some simulation parameters depending on the list of values, in this case try different parameters for the PID-controlers proportional gain.
    sim[idx].run_simulation() #Run the simulation
    plots.append(sim[idx].show_plots('Motor Power Diagram',expand_title='/ PID-Controler I-Gain is {}'.format(value),return_figure_object=True)) #Specify that we are only interested in the 'Motor Power Diagram' and dump the processed figure in the container 'plots' for use later on
print('Simulations are done, now lets take a look at the results.')

#Have not yet found a good solution to combine all figures into one big subplot
for fig in plots: #Iterate over all generated figures
    fig.show() #Plot the figure

#Go ahead and draw some other plots from each individual simulation
    #Hint: sim[0].show_plot('Speed Diagram) somethin like that as terminal-input might work...
