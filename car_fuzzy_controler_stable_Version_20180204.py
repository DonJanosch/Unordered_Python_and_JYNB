import numpy as np
import skfuzzy as fuzz

class car_fuzzy_controler:
    def __init__(self, name, global_resolution = 1000):
        self.name = name
        self.SD_input = 0
        self.dSD_input = 0
        self.x_output = 0
        self.seconds_until_crash_fast = 6 #Closing in fast
        self.seconds_until_crash_moderat = 30 #Closing in moderately
        self.global_resolution = global_resolution
        self.SD_max = 10
        self.SD_min = 0.1
        self.dSD_max = 1/self.seconds_until_crash_fast
        self.dSD_min = -1/self.seconds_until_crash_fast

        #Defining the range of safety distance (SD) we are interested in, from 10% to 1000%
        self.SD_range = np.logspace(-1,1,self.global_resolution) #log space to the powers of 10
        #self.SD_range = np.linspace(0.1,10,self.global_resolution)

        #Defining the range of change in safety distance (dSD) we are interested in, the maximum Rate of change is when we will collide after 6 seconds, if we do nothing

        self.dSD_range = np.linspace(-1/self.seconds_until_crash_fast,1/self.seconds_until_crash_fast,self.global_resolution)

        #Defining the range of output value x
        self.x_range = np.linspace(-0.25,1.25,self.global_resolution)

        #Defining names for the fuzzy-groups
        self.SD_groups = ['ways_to_view','to_view','just_right','to_much','ways_to_much']
        self.dSD_groups = ['closing_in_fast','closing_in_moderatly','staying_the_same','getting_away_moderatly','getting_away_fast']
        self.x_groups = ['full_safety','mostly_safety','meet_in_the_middle','mostly_speeding','full_speeding']

        #Associating the fuzzy-groups in range
        self.SD_ways_to_view = fuzz.zmf(self.SD_range, 0.1,0.5)
        self.SD_to_view = fuzz.trimf(self.SD_range,[0.5,0.75,1.1])
        self.SD_just_right = fuzz.trimf(self.SD_range,[0.8,1,1.5])
        self.SD_to_much = fuzz.trimf(self.SD_range,[0.95,2,5])
        self.SD_ways_to_much = fuzz.smf(self.SD_range,3,8)

        self.dSD_closing_in_fast = fuzz.trimf(self.dSD_range,[-1/self.seconds_until_crash_fast,-1/self.seconds_until_crash_fast,-1/self.seconds_until_crash_moderat])
        self.dSD_closing_in_moderatly = fuzz.trimf(self.dSD_range,[-1/self.seconds_until_crash_fast,-1/self.seconds_until_crash_moderat,0])
        self.dSD_staying_the_same = fuzz.trimf(self.dSD_range,[-1/self.seconds_until_crash_moderat,0,1/self.seconds_until_crash_moderat])
        self.dSD_getting_away_moderatly = fuzz.trimf(self.dSD_range,[0,1/self.seconds_until_crash_moderat,1/self.seconds_until_crash_fast])
        self.dSD_getting_away_fast = fuzz.trimf(self.dSD_range,[1/self.seconds_until_crash_moderat,1/self.seconds_until_crash_fast,1/self.seconds_until_crash_fast])

        self.x_full_safety =fuzz.trimf(self.x_range,[-0.25,0,0.25])
        self.x_mostly_safety =fuzz.trimf(self.x_range,[0,0.25,0.5])
        self.x_meet_in_the_middle =fuzz.trimf(self.x_range,[0.25,0.5,0.75])
        self.x_mostly_speeding =fuzz.trimf(self.x_range,[0.5,0.75,1])
        self.x_full_speeding =fuzz.trimf(self.x_range,[0.75,1,1.25])

        return None

    def compute_input(self,SD,dSD):
        #Clip the inputs to stay within the specified range
        self.SD_input = np.clip(SD,self.SD_min,self.SD_max)
        self.dSD_input = np.clip(dSD,self.dSD_min,self.dSD_max)

        #Interpolating the given input parameters
        activation_SD_ways_to_view = fuzz.interp_membership(self.SD_range,self.SD_ways_to_view,self.SD_input)
        activation_SD_to_view = fuzz.interp_membership(self.SD_range,self.SD_to_view,self.SD_input)
        activation_SD_just_right = fuzz.interp_membership(self.SD_range,self.SD_just_right,self.SD_input)
        activation_SD_to_much = fuzz.interp_membership(self.SD_range,self.SD_to_much,self.SD_input)
        activation_SD_ways_to_much = fuzz.interp_membership(self.SD_range,self.SD_ways_to_much,self.SD_input)

        activation_dSD_closing_in_fast = fuzz.interp_membership(self.dSD_range,self.dSD_closing_in_fast,self.dSD_input)
        activation_dSD_closing_in_moderatly = fuzz.interp_membership(self.dSD_range,self.dSD_closing_in_moderatly,self.dSD_input)
        activation_dSD_staying_the_same = fuzz.interp_membership(self.dSD_range,self.dSD_staying_the_same,self.dSD_input)
        activation_dSD_getting_away_moderatly = fuzz.interp_membership(self.dSD_range,self.dSD_getting_away_moderatly,self.dSD_input)
        activation_dSD_dSD_getting_away_fast = fuzz.interp_membership(self.dSD_range,self.dSD_getting_away_fast,self.dSD_input)

        #Defining the fuzzy-rule-set
        rule_full_safety = np.max([activation_SD_ways_to_view * activation_dSD_closing_in_fast,
                                   activation_SD_ways_to_view * activation_dSD_closing_in_moderatly,
                                   activation_SD_ways_to_view * activation_dSD_staying_the_same,
                                   activation_SD_to_view * activation_dSD_closing_in_fast,
                                   activation_SD_to_view * activation_dSD_closing_in_moderatly,
                                   activation_SD_to_view * activation_dSD_staying_the_same,
                                   activation_SD_just_right * activation_dSD_closing_in_fast,
                                   activation_SD_just_right * activation_dSD_closing_in_moderatly,
                                   activation_SD_just_right * activation_dSD_staying_the_same])

        rule_mostly_safety = np.max([activation_SD_ways_to_view * activation_dSD_getting_away_moderatly,
                                     activation_SD_ways_to_view * activation_dSD_dSD_getting_away_fast,
                                     activation_SD_to_view * activation_dSD_getting_away_moderatly,
                                     activation_SD_just_right * activation_dSD_getting_away_moderatly,
                                     activation_SD_to_much * activation_dSD_closing_in_moderatly,
                                     activation_SD_to_much * activation_dSD_closing_in_fast])

        rule_meet_in_the_middle = np.max([activation_SD_to_view * activation_dSD_dSD_getting_away_fast,
                                          activation_SD_to_much * activation_dSD_staying_the_same,
                                          activation_SD_ways_to_much * activation_dSD_closing_in_fast])

        rule_mostly_speeding = np.max([activation_SD_just_right * activation_dSD_dSD_getting_away_fast,
                                       activation_SD_ways_to_much * activation_dSD_closing_in_moderatly])

        rule_full_speeding = np.max([activation_SD_to_much * activation_dSD_getting_away_moderatly,
                                     activation_SD_to_much * activation_dSD_dSD_getting_away_fast,
                                     activation_SD_ways_to_much * activation_dSD_staying_the_same,
                                     activation_SD_ways_to_much * activation_dSD_getting_away_moderatly,
                                     activation_SD_ways_to_much * activation_dSD_dSD_getting_away_fast])

        #Mapping the degree of activation of the rule-set
        activation_full_safety = np.minimum(self.x_full_safety,rule_full_safety)
        activation_mostly_safety = np.minimum(self.x_mostly_safety,rule_mostly_safety)
        activation_meet_in_the_middle = np.minimum(self.x_meet_in_the_middle,rule_meet_in_the_middle)
        activation_mostly_speeding = np.minimum(self.x_mostly_speeding,rule_mostly_speeding)
        activation_full_speeding = np.minimum(self.x_full_speeding,rule_full_speeding)

        #Aggregate all the activations by OR overlapping them
        activation_aggregated = np.maximum.reduce([activation_full_safety,activation_mostly_safety,activation_meet_in_the_middle,activation_mostly_speeding,activation_full_speeding])

        #Compute the output by defuzzifying the result
        self.x_output = np.clip(fuzz.defuzz(self.x_range,activation_aggregated,'centroid'),0,1) #Might determine values slightly more than 1 or less than 0 therefore the np.clip
        
        return self.x_output
