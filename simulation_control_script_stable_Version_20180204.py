#Use a Control script to start and run the simulation, you can also do this directly via console comands (obviously :-P)
from car_fuzzy_simulation import simulation_enviroment as env

sim = env()

#Play around with parameters and do some studies like this:
for x in [1,5,10]:
    sim.averaging_last_x_fuzzy_outputs = x
    sim.run_simulation()
    sim.show_plots('Motor Power Diagram',expand_title='Averaging the last {} fuzzy outputs'.format(x))
