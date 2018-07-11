import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


def freemf(x_range,y_assosiation):
    x_assosiation_sorted = sorted(list(y_assosiation.keys())) #Make a list of the keys in the input dictionary in ascending order
    y_assosiation_sorted = [y_assosiation[x] for x in x_assosiation_sorted] #Make a list of the associated items in the input dictionary considering 'x_assosiation_sorted'
    return [np.interp(x,x_assosiation_sorted,y_assosiation_sorted) for x in x_range] #Map the two lits to the defined 'x_range' and return it as output
    
#Inputs go here
SD_input = 1.23
dSD_input = -0.03

#Hyperparameter to define the resolution of our Variables
global_resolution = 1000
SD_max = 10
SD_min = 0.1
dSD_max = 1/3
dSD_min = -1/3
x_min = -0.25
x_max = 1.25

#Defining the range of safety distance (SD) we are interested in, from 10% to 1000% in a log10 scale)
SD_range = np.logspace(-1,1,global_resolution)

#Defining the range of change in safety distance (dSD) we are interested in, the maximum Rate of change is when we will colide after 6 seconds, if we do nothing
seconds_until_crash_fast = 6 #Closing in fast
seconds_until_crash_moderat = 30 #Closing in moderatly
dSD_range = np.linspace(-1/seconds_until_crash_fast,1/seconds_until_crash_fast,global_resolution)

#Defining the range of output value x
x_range = np.linspace(-0.25,1.25,global_resolution)

#Defining names for the fuzzy-groups
SD_groups = ['ways_to_view','to_view','just_right','to_much','ways_to_much']
dSD_groups = ['closing_in_fast','closing_in_moderatly','staying_the_same','getting_away_moderatly','getting_away_fast']
x_groups = ['full_safety','mostly_safety','meet_in_the_middle','mostly_speeding','full_speeding']

#Associating the fuzzy-groups in range
SD_ways_to_view = freemf(SD_range,{0:1,0.25:1,0.5:0.25,0.75:0})#fuzz.zmf(SD_range, 0.1,0.5)
SD_to_view = freemf(SD_range,{0.25:0,0.5:0.8,0.75:1,1:0.2,1.3:0})#fuzz.trimf(SD_range,[0.5,0.75,1.1])
SD_just_right = freemf(SD_range,{0.75:0,1:1,1.3:0.4,1.5:0.2,2:0})#fuzz.trimf(SD_range,[0.8,1,1.5])
SD_to_much = freemf(SD_range,{0.75:0,1:0.05,1.3:0.1,1.5:0.3,2:0.5,2.5:1,5:0.2,7:0})#fuzz.trimf(SD_range,[0.95,2,5])
SD_ways_to_much = freemf(SD_range,{2:0,2.5:0.05,5:0.5,10:1,SD_max:1})#fuzz.smf(SD_range,3,8)

dSD_closing_in_fast = freemf(dSD_range,{dSD_min:1,-1/10:0})#fuzz.trimf(dSD_range,[-1/seconds_until_crash_fast,-1/seconds_until_crash_fast,-1/seconds_until_crash_moderat])
dSD_closing_in_moderatly = freemf(dSD_range,{-1/6:0,-1/10:0.2,-1/20:1,0:0})#fuzz.trimf(dSD_range,[-1/seconds_until_crash_fast,-1/seconds_until_crash_moderat,0])
dSD_staying_the_same = freemf(dSD_range,{-1/10:0,-1/20:0.1,0:1,1/20:0.1,1/10:0})#fuzz.trimf(dSD_range,[-1/seconds_until_crash_moderat,0,1/seconds_until_crash_moderat])
dSD_getting_away_moderatly = freemf(dSD_range,{0:0,1/20:1,1/10:0.2,1/6:0})#fuzz.trimf(dSD_range,[0,1/seconds_until_crash_moderat,1/seconds_until_crash_fast])
dSD_getting_away_fast = freemf(dSD_range,{1/10:0,dSD_max:1})#fuzz.trimf(dSD_range,[1/seconds_until_crash_moderat,1/seconds_until_crash_fast,1/seconds_until_crash_fast])

x_full_safety = freemf(x_range,{x_min:0,0:1,0.25:0})#fuzz.trimf(x_range,[-0.25,0,0.25])
x_mostly_safety = freemf(x_range,{0:0,0.25:1,0.5:0})#fuzz.trimf(x_range,[0,0.25,0.5])
x_meet_in_the_middle = freemf(x_range,{0.25:0,0.5:1,0.75:0})#fuzz.trimf(x_range,[0.25,0.5,0.75])
x_mostly_speeding = freemf(x_range,{0.5:0,0.75:1,1:0})#fuzz.trimf(x_range,[0.5,0.75,1])
x_full_speeding = freemf(x_range,{0.75:0,1:1,x_max:0})#fuzz.trimf(x_range,[0.75,1,1.25])

# Visualize these universes and membership functions
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(SD_range, SD_ways_to_view, linewidth=1.5, label=SD_groups[0])
ax0.plot(SD_range, SD_to_view, linewidth=1.5, label=SD_groups[1])
ax0.plot(SD_range, SD_just_right, linewidth=1.5, label=SD_groups[2])
ax0.plot(SD_range, SD_to_much, linewidth=1.5, label=SD_groups[3])
ax0.plot(SD_range, SD_ways_to_much, linewidth=1.5, label=SD_groups[4])
ax0.set_title('Fuzzy input: Safety Distance SD')
ax0.legend()

ax1.plot(dSD_range, dSD_closing_in_fast, linewidth=1.5, label=dSD_groups[0])
ax1.plot(dSD_range, dSD_closing_in_moderatly, linewidth=1.5, label=dSD_groups[1])
ax1.plot(dSD_range, dSD_staying_the_same, linewidth=1.5, label=dSD_groups[2])
ax1.plot(dSD_range, dSD_getting_away_moderatly, linewidth=1.5, label=dSD_groups[3])
ax1.plot(dSD_range, dSD_getting_away_fast, linewidth=1.5, label=dSD_groups[4])
ax1.set_title('Fuzzy input: Change in safety distance dSD')
ax1.legend()

ax2.plot(x_range, x_full_safety, linewidth=1.5, label=x_groups[0])
ax2.plot(x_range, x_mostly_safety, linewidth=1.5, label=x_groups[1])
ax2.plot(x_range, x_meet_in_the_middle, linewidth=1.5, label=x_groups[2])
ax2.plot(x_range, x_mostly_speeding, linewidth=1.5, label=x_groups[3])
ax2.plot(x_range, x_full_speeding, linewidth=1.5, label=x_groups[4])
ax2.set_title('Fuzzy output: Mixing-Fator x')
ax2.legend()

plt.tight_layout()
#plt.show()

#Interpolating the given input parameters
activation_SD_ways_to_view = fuzz.interp_membership(SD_range,SD_ways_to_view,SD_input)
activation_SD_to_view = fuzz.interp_membership(SD_range,SD_to_view,SD_input)
activation_SD_just_right = fuzz.interp_membership(SD_range,SD_just_right,SD_input)
activation_SD_to_much = fuzz.interp_membership(SD_range,SD_to_much,SD_input)
activation_SD_ways_to_much = fuzz.interp_membership(SD_range,SD_ways_to_much,SD_input)

activation_dSD_closing_in_fast = fuzz.interp_membership(dSD_range,dSD_closing_in_fast,dSD_input)
activation_dSD_closing_in_moderatly = fuzz.interp_membership(dSD_range,dSD_closing_in_moderatly,dSD_input)
activation_dSD_staying_the_same = fuzz.interp_membership(dSD_range,dSD_staying_the_same,dSD_input)
activation_dSD_getting_away_moderatly = fuzz.interp_membership(dSD_range,dSD_getting_away_moderatly,dSD_input)
activation_dSD_dSD_getting_away_fast = fuzz.interp_membership(dSD_range,dSD_getting_away_fast,dSD_input)

#Defining the fuzzy-rule-set
rule_full_safety = np.max([activation_SD_ways_to_view * activation_dSD_closing_in_fast,
                                   activation_SD_ways_to_view * activation_dSD_closing_in_moderatly,
                                   activation_SD_ways_to_view * activation_dSD_staying_the_same,
                                   activation_SD_ways_to_view * activation_dSD_getting_away_moderatly,
                                   activation_SD_ways_to_view * activation_dSD_dSD_getting_away_fast,
                                   activation_SD_to_view * activation_dSD_closing_in_fast,
                                   activation_SD_to_view * activation_dSD_closing_in_moderatly,
                                   activation_SD_to_view * activation_dSD_staying_the_same,
                                   activation_SD_just_right * activation_dSD_closing_in_fast,
                                   activation_SD_just_right * activation_dSD_closing_in_moderatly,
                                   activation_SD_just_right * activation_dSD_staying_the_same])

rule_mostly_safety = np.max([activation_SD_to_view * activation_dSD_getting_away_moderatly,
                                     activation_SD_just_right * activation_dSD_getting_away_moderatly,
                                     activation_SD_to_much * activation_dSD_closing_in_moderatly,
                                     activation_SD_to_much * activation_dSD_closing_in_fast])

rule_meet_in_the_middle = np.max([activation_SD_to_view * activation_dSD_dSD_getting_away_fast,
                                          activation_SD_to_much * activation_dSD_staying_the_same,
                                          activation_SD_ways_to_much * activation_dSD_closing_in_fast])

rule_mostly_speeding = np.max([activation_SD_just_right * activation_dSD_dSD_getting_away_fast,
                                       activation_SD_to_much * activation_dSD_getting_away_moderatly,
                                       activation_SD_ways_to_much * activation_dSD_closing_in_moderatly])

rule_full_speeding = np.max([activation_SD_to_much * activation_dSD_dSD_getting_away_fast,
                                     activation_SD_ways_to_much * activation_dSD_staying_the_same,
                                     activation_SD_ways_to_much * activation_dSD_getting_away_moderatly,
                                     activation_SD_ways_to_much * activation_dSD_dSD_getting_away_fast])

#Maping the degree of activation of the rule-set
activation_full_safety = np.minimum(x_full_safety,rule_full_safety)
activation_mostly_safety = np.minimum(x_mostly_safety,rule_mostly_safety)
activation_meet_in_the_middle = np.minimum(x_meet_in_the_middle,rule_meet_in_the_middle)
activation_mostly_speeding = np.minimum(x_mostly_speeding,rule_mostly_speeding)
activation_full_speeding = np.minimum(x_full_speeding,rule_full_speeding)

activation_aggregated = np.maximum.reduce([activation_full_safety,activation_mostly_safety,activation_meet_in_the_middle,activation_mostly_speeding,activation_full_speeding])


COG_of_output = fuzz.defuzz(x_range,activation_aggregated,'centroid')

#Display the rule activation

fig, ax0 = plt.subplots(figsize=(8, 3))
ax0.fill_between(x_range,0, activation_full_safety, alpha=0.7,label=x_groups[0])
ax0.fill_between(x_range,0, activation_mostly_safety, alpha=0.7,label=x_groups[1])
ax0.fill_between(x_range,0, activation_meet_in_the_middle, alpha=0.7,label=x_groups[2])
ax0.fill_between(x_range,0, activation_mostly_speeding, alpha=0.7,label=x_groups[3])
ax0.fill_between(x_range,0, activation_full_speeding, alpha=0.7,label=x_groups[3])

ax0.set_title('Activation of rule set')
ax0.legend()
plt.ylim((0,1))

fig, ax0 = plt.subplots(figsize=(8, 3))
ax0.fill_between(x_range,0,activation_aggregated,label='Activation aggregated')
ax0.set_title('Activation center of gragity: {}'.format(round(COG_of_output,2)))
ax0.legend()
plt.ylim((0,1))
plt.show()

print(COG_of_output)
x_output = COG_of_output
