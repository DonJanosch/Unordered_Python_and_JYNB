import numpy as np
from car_fuzzy_controler import car_fuzzy_controler
import matplotlib.pyplot as plt

class simulation_enviroment:
    '''A class which controls the simulation environment for a proof of concept in fuzzy-controls.
    The environment simulates two cars via the formula P_motor = P_air_friction + P_roller_friction + P_kin.
    Input is the cars motor power which is consumed by air-friction and roller-friction. The difference goes into kinetic energy
    and either accelerates or decelerates the car. Effectively this forms a differential equation which is solved in a time-series calculation.
    Safety distance is calculated by the rule of thumb: Take your speed in km/h, halve it and take the value as safety-distance in m.
    The relative safety-distance is the quotient of the values actual distance and required safety distance which ideally should stay at 100%.
    Speed, Position, distance between the cars and many more variables are calculated.\n

    The first cars motor power is controlled by a look-up-table in a way like: stay at 100% from 0s to 10s, then decrease to 60% until 15s and so on.
    The second cars motor power is controlled in a way that the car should mimic human behavior and try always to stay
    at about 100% safety distance from the first car. Never the less it shall do better than just giving a PID controller the job to stay at 100% safety distance.
    The control scheme utilizes fuzzy logic and PID controllers. The fuzzy controller creates a 'smart' set point for the PID controller, who in turn acts on the motor power.
    
    Feel free to experiment and play around with the parameters.
    Cheers - Jan Macenka, 2018-02-03
    Contact: jan.macenka@gmail.com'''

    def __init__(self):
        '''Initializing function which will set all the parameters and run build_simulation_enviroment once.'''
        print('Constructing a class object')
        self.simulation_time = 100 #simulated driving time in s
        self.dt = 0.15 #simulation resolution in s (lower values make the controller act more often)

        #Specify fixed parameters
        #General
        self.air_dens = 1.225 #Air density in kg/m³ (at +15°C)
        self.g = 9.81 #Gravitational pull in m/s²

        #Car 1 (the leading car)
        self.Pmax1PS = 105 #Cars maximum motor power in HP (Deutsch PS)
        self.m1 = 1500 #Cars weight in kg
        self.A1 = 0.5 #Cars frontal surface area in m²
        self.c_w1 = 0.45 #Cars air friction coefficient in -
        self.c_p1 = 0.015 #Cars roller friction coefficient in -
        self.a1_max = 0.8*self.g #Cars maximum acceleration (corresponds to the ratio of power to mass) in m/s²
        self.a1_min = -3*self.g #Cars maximum breaking deceleration in m/s²
        self.v1_0 = 10/3.6 #cars initial speed in m/s
        self.x1_0 = 200 #Cars initial position in m
        self.look_up_Ppower1 = [[0,10,11,12,14 ,30 ,50 ,51 ,60,61,65,70,90 ,100], #Cars motor power look up table, seconds into simulation in s
                                [1,1 ,-2,-3,0.8,0.8,0.3,0.1,1 ,-3,-3,1 ,0.6,1  ]] #Cars motor power look up table, percentage of motor power in 1 is 100%

        #Car 2 (the controlled following car)
        self.Pmax2PS = 200 #Cars maximum motor power in HP (deutsch PS)
        self.m2 = 1200 #Cars weight in kg
        self.A2 = 0.35 #Cars frontal surface area in m²
        self.c_w2 = 0.35 #Cars air friction coefficient in -
        self.c_p2 = 0.015 #Cars roller friction coefficient in -
        self.a2_max = 1.5*self.g #Cars maximum acceleration (corresponds to the ratio of power to mass) in m/s²
        self.a2_min = -3*self.g #Cars maximum breaking deceleration in m/s²
        self.max_motor_power = 1 #Cars maximum motor power to be asked for by the controller in 1 as 100%
        self.max_breaking_power = -3 #Cars maximum breaking power to be asked for by the controller in 1 as 100%
        self.v2_0 = 0.001/3.6 #cars initial speed in m/s
        self.x2_0 = 0 #Cars initial position in m
        self.DSkmh = 150 #Cars desired cruise control speed in km/h

        #Set point generation
        self.smart_clipping = False #Makes better behavior if closing in fast onto the car up front
        self.averaging_last_x_fuzzy_outputs = 3 #Smoothen the fuzzy-output by taking the average value of the last view samples, leads to less spikes in motor power

        #PID Controller
        self.K_p = 0.8 #Gain of the proportional part
        self.K_i = 0.1 #Gain of the integral part, since the behavior of the integral part would be depending on the sampling rate, it is scaled with the sampling rate to remain the same :)
        self.cap_i = 3 #Cap for maximum and minimum charge of the integrator part
        self.K_d = 0 #Gain of the derivative part
        self.controler_cap = 3 #Cap for the controller as a whole, it shall only output values in the range of -cap ... +cap
        
        #When initializing, also set up the environment. Unless the parameters are changed, that is only necessary once.
        self.simulated_steps = 0
        self.build_simulation_enviroment()
        self.build_fuzzy_controler()
        
    def show_simulation_parameters(self):
        '''TO BE DEVELOPED. Needs to return a long list of Parameters that in turn can be displayed by the user.
        There will be no set/get functions for individual parameter as they are hyper parameters. Just set them directly (quick and dirty).'''
        #parameter_list = sorted(vars(self), key=str.lower)
        parameter_list = vars(self)
        print('*********************************************',
              '\nThe simulation uses the following parameters:',
              '\n*********************************************')
        print ('\n\n'.join("%s: %s" % item for item in parameter_list.items()))
        print('\n*********************************************')

    def build_simulation_enviroment(self):
        '''Configures and sets up the numpy 'memory' array for the simulation.
        Also creates the fuzzy-controller object from its class-file.
        Is required to run each time simulation parameters get changed.'''
        print('Updating the simulation enviroment')
       
        #Define the np-array that holds the simulation data
        self.column_headers = ['t','v1','v1kmh','x1','Ppower1','Pmot1','Pair1','Proller1','Pkin1','a1','v2','v2kmh','x2','Ppower2','Pmot2','Pair2','Proller2','Pkin2','a2','Distance','SD','dSD','x_fuzzy','SS','DS','S_SP','S','S_Error','PID_P','PID_I', 'PID_D','PID_output'] #Define all the existing columns
        self.simulated_timesepts = int(np.ceil(self.simulation_time/self.dt))
        self.results = np.zeros((self.simulated_timesepts,len(self.column_headers))) #Make an empty numpy array in the correct size

        #Pre-compute the time for all time steps that are taken
        self.t_precomputed=np.arange(0,self.simulated_timesepts*self.dt,self.dt) #Pre-compute all time labels for easy access
        self.results[:,0]+=self.t_precomputed.T #Write the time labels to the results array already

    def build_fuzzy_controler(self):
        '''Builds the fuzzy controller (Object) from the fuzzy-controller class in 'car_fuzzy_controler.py'.
        The File and class gets imported as an dependency.'''
        self.my_fzz = car_fuzzy_controler(0) #Takes a name for initialization, just named it 0

    def load_from_memory(self,k,variable_name):
        '''Helper function used by function run_simulation.
        Takes the current memory-index k and a value-identifier string variable name
        Returns the value from the k-1 memory field.'''
        return self.results[k-1,self.column_headers.index(str(variable_name))]

    def save_to_memory(self,k,variable_name,variable_parameter):
        '''Helper function used by function run_simulation.
        Takes the current memory-index k, a value-identifier string variable name and the corresponding value
        Dumps it into memory for time-step k and return None.'''
        self.results[k,self.column_headers.index(str(variable_name))] = variable_parameter

    def run_simulation(self):
        self.build_simulation_enviroment() #Re-Setting up the simulation environment in case some parameter have been changed
        print('Starting simulation')
        #Do some scaling
        self.DS = self.DSkmh/3.6 #Cars desired cruise control speed in m/s
        self.Pmax1 = self.Pmax1PS*735.5 #Cars maximum motor power in W
        self.Pmax2 = self.Pmax2PS*735.5 #Cars maximum motor power in W
        #Dont want to write self. everywhere so I just import it once, also this might boost performance
        dt = self.dt
        save_to_memory = self.save_to_memory
        load_from_memory = self.load_from_memory
        
        #'Hand'-initialize the first time step where t=0, rest is all zero
        k = 0
        #Car 1
        self.save_to_memory(k,'v1',self.v1_0)
        save_to_memory(k,'v1kmh',self.v1_0*3.6)
        save_to_memory(k,'x1',self.x1_0)
        #Car2
        save_to_memory(k,'v2',self.v2_0)
        save_to_memory(k,'v2kmh',self.v2_0*3.6)
        save_to_memory(k,'x2',self.x2_0)
        #General
        SS = self.v1_0
        Distance = self.x1_0-self.x2_0
        SD = Distance/2/(SS*3.6) #Rule of thumb: Safety distance in meters is halve your speed in km/h
        dSD = (SD-0)/dt
        save_to_memory(k,'SS',SS)
        save_to_memory(k,'Distance',Distance)
        save_to_memory(k,'SD',SD)
        save_to_memory(k,'dSD',dSD)

        #Go to first time step and then compute the loop
        t=dt
        k = 1
        while t<=self.simulation_time:
            #Read previous results
            x1_prev = load_from_memory(k,'x1')
            v1_prev = load_from_memory(k,'v1')
            a1_prev = load_from_memory(k,'a1')

            x2_prev = load_from_memory(k,'x2')
            v2_prev = load_from_memory(k,'v2')
            a2_prev = load_from_memory(k,'a2')
            
            SD_prev = load_from_memory(k,'SD')
            PID_I_prev = load_from_memory(k,'PID_I')
            S_Error_prev = load_from_memory(k,'S_Error')
            
            #Compute variables
            v1 = v1_prev + a1_prev * dt
            x1 = x1_prev + v1_prev * dt
            Ppower1 = np.interp(t,self.look_up_Ppower1[0],self.look_up_Ppower1[1])
            Pmot1 = self.Pmax1*Ppower1
            Pair1 = self.A1*self.c_w1*self.air_dens/2*v1*v1*v1
            Proller1 = self.m1*self.g*self.c_p1*v1
            Pkin1 = Pmot1-Pair1-Proller1
            a1 = np.clip((2*Pkin1)/(self.m1*v1*v1),self.a1_min,self.a1_max)
            v1kmh = v1*3.6
            v2 = v2_prev + a2_prev * dt
            x2 = x2_prev + v2_prev * dt

            #compute the control logic
            S = v2
            SS = v1
            Distance = x1-x2
            SD = Distance*2/(S*3.6) #Rule of thumb: Safety distance in meters is halve your speed in km/h
            dSD = (SD-SD_prev)/dt
            x_fuzzy = self.my_fzz.compute_input(SD,dSD)
            if k > self.averaging_last_x_fuzzy_outputs:
                #average over the last view x_fuzzy steps according to specification
                last = [load_from_memory(k,'x_fuzzy') for i in range(self.averaging_last_x_fuzzy_outputs-1)]
                last.append(x_fuzzy)
                x_fuzzy = np.mean(last)
            S_SP = (self.DS*x_fuzzy+(1-x_fuzzy)*SS)*np.clip(SD*0.8,0,1)
            if self.smart_clipping:
                S_SP = np.clip(S_SP*np.clip(SD*np.clip(SS/S,0,1),0,1),-self.DS,self.DS)
            else:
                S_SP = np.clip(S_SP,-self.DS,self.DS)
            S_Error = S_SP-S
            PID_P = self.K_p * S_Error
            PID_I = np.clip(PID_I_prev + self.K_i * S_Error*dt,-self.cap_i,self.cap_i)
            PID_D = (S_Error-S_Error_prev)/dt * self.K_d
            PID_output = np.clip(PID_P+PID_I+PID_D,-self.controler_cap,self.controler_cap)

            #compute some more variables that depend on the control logic
            Ppower2 = np.clip(PID_output,self.max_breaking_power,self.max_motor_power)
            Pmot2 = self.Pmax2*Ppower2
            Pair2 = self.A2*self.c_w2*self.air_dens/2*v2*v2*v2
            Proller2 = self.m2*self.g*self.c_p2*v2
            Pkin2 = Pmot2-Pair2-Proller2
            a2 = np.clip((2*Pkin2)/(self.m2*v2*v2),self.a2_min,self.a2_max)
            v2kmh = v2*3.6
            
            #Update the results array
            save_to_memory(k,'x1',x1)
            save_to_memory(k,'v1',v1)
            save_to_memory(k,'v1kmh',v1kmh)
            save_to_memory(k,'a1',a1)
            save_to_memory(k,'Ppower1',Ppower1)
            save_to_memory(k,'Pmot1',Pmot1)
            save_to_memory(k,'Pair1',Pair1)
            save_to_memory(k,'Proller1',Proller1)
            save_to_memory(k,'Pkin1',Pkin1)
            
            save_to_memory(k,'x2',x2)
            save_to_memory(k,'v2',v2)
            save_to_memory(k,'v2kmh',v2kmh)
            save_to_memory(k,'a2',a2)
            save_to_memory(k,'Ppower2',Ppower2)
            save_to_memory(k,'Pmot2',Pmot2)
            save_to_memory(k,'Pair2',Pair2)
            save_to_memory(k,'Proller2',Proller2)
            save_to_memory(k,'Pkin2',Pkin2)
            
            save_to_memory(k,'SS',SS)
            save_to_memory(k,'DS',self.DS)
            save_to_memory(k,'S_SP',S_SP)
            save_to_memory(k,'Distance',Distance)
            save_to_memory(k,'SD',SD)
            save_to_memory(k,'dSD',dSD)
            save_to_memory(k,'x_fuzzy',x_fuzzy)
            save_to_memory(k,'S_Error',S_Error)
            save_to_memory(k,'PID_P',PID_P)
            save_to_memory(k,'PID_I',PID_I)
            save_to_memory(k,'PID_D',PID_D)
            save_to_memory(k,'PID_output',PID_output)
            save_to_memory(k,'S',S)
            
            #Increment the helper variables
            k+=1
            t+=dt
        self.simulated_steps = k
        print('Finished simulation')

    def return_results(self,*args):
        '''Function to return an arbitrary amount of simulated parameters.
        INPUT is *args as Strings. If these are simulated variables, they get returned.
        OUTPUT is np.array with first column is head_lines[0] which should be simulated time 't'
        The rest of the results are appended as more columns.'''
        res = [] #Container to hold our search results
        res.append(self.results[:,0]) #Always return the first header index which should be the simulation time 't'
        if len(args)==0: #Check if no arguments were specified, in this case return some default values
            res.append(self.results[:,2]) #Should be v1kmh
            res.append(self.results[:,11]) #Should be v2kmh
        for arg in args: #Toggle through all the specified arguments and try to find them
            try: #Try to find the arg
                res.append(self.results[:,self.column_headers.index(str(arg))]) #If the arg is in the list 'column_headers', return all its values (rows)
            except: #If arg was not found
                print('The requested parameter {} was not found.'.format(arg)) #Tell the user, that the arg was not found and carry on
        return np.array(res).T #Finlay turn the list of list into a np.array and return it. '.T' is for Transpose and switches columns and rows so everything is as we expect it to be.

    def save_results(self):
        '''Function to save the results in an excel file.
        For convenience the numpy array is first converted to a
        Pandas DataFrame and formatted for easier handling.
        Can be called manually after constructing the data container
        with 'build_simulation_enviroment.'.'''
        import pandas as pd #Is only needed for saving purposes, hence only load it upon saving
        import time, datetime #Same thing here
        import os
                           
        df = pd.DataFrame(data=self.results,columns=self.column_headers).set_index('t') #convert the np-array to a pandas DataFrame for simple saving
        doc_name = 'fuzzy_car_simulation_results_from_{}.xlsx'.format(datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S')) #Format the target document name to also hold a time stamp
        try:
            df.to_excel(doc_name)
            print('Results saved in \'{}\{}\''.format(os.getcwd(),doc_name))
        except:
            print('The file \'{}\{}\' seems to be used by another program, cant write to it. Please close the file and try again!'.format(os.getcwd(),doc_name))

    #Now create the result plots
    def show_plots(self,what='all',expand_title = '',return_figure_object=False):
        '''Function to plot results after a simulation was run with 'run_simulation()'.\n
        The results-table can be saved with the function 'save_results()' to examine them more closely.'''
        print('Preparing result-plots')
        #Show plots
        color_car1 = 'g'
        color_car2 = 'b'
        skipp = int(self.simulated_steps*0.05)+1
        
        if str.lower(what) == 'all' or str.lower(what) == str.lower('Fuzzy Controler Diagram'): #only print if asked for
            #Fuzzy Controler Diagram
            fig, ax0 = plt.subplots(figsize=(8, 3))
            ax0.plot(self.results[skipp:,self.column_headers.index('t')], self.results[skipp:,self.column_headers.index('SD')]*100,label='INPUT: Safety distance in %')
            ax0.plot(self.results[skipp:,self.column_headers.index('t')], self.results[skipp:,self.column_headers.index('dSD')]*100,label='INPUT: Rate of change in safety distance in %/s')
            ax0.plot(self.results[skipp:,self.column_headers.index('t')], self.results[skipp:,self.column_headers.index('x_fuzzy')]*100,label='OUTPUT: Fuzzy mixing factor output as %')
            plt.xlabel('time in s')
            plt.ylabel('Fuzzy Controlers internal states')
            plt.title('Fuzzy Controler Diagram, skipped first view seconds for better readability'+' '+str(expand_title))
            plt.grid(True)
            ax0.legend()
            if return_figure_object:
                return fig
            
        if str.lower(what) == 'all' or str.lower(what) == str.lower('PID Controler Diagram'): #only print if asked for
            #PID Controler Diagram
            fig, ax0 = plt.subplots(figsize=(8, 3))
            ax0.plot(self.results[skipp:,self.column_headers.index('t')], self.results[skipp:,self.column_headers.index('PID_P')],label='Contribution of P-Part')
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('PID_I')],label='Contribution of I-Part')
            ax0.plot(self.results[skipp:,self.column_headers.index('t')], self.results[skipp:,self.column_headers.index('PID_D')],label='Contribution of D-Part')
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('PID_output')],label='PID signal-output for motor power')
            plt.xlabel('time in s')
            plt.ylabel('PID internal states')
            plt.title('PID Controler Diagram'+' '+str(expand_title))
            plt.grid(True)
            ax0.legend()
            if return_figure_object:
                return fig

        if str.lower(what) == 'all' or str.lower(what) == str.lower('Speed Setpoint Diagram'): #only print if asked for
            #Speed Setpoint Diagram
            fig, ax0 = plt.subplots(figsize=(8, 3))
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('SS')]*3.6,label='Safety speed')
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('DS')]*3.6,label='Desired speed')
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('S_SP')]*3.6,label='Set point speed')
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('S')]*3.6,label='Actual speed')
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('S_Error')]*3.6,label='Deviation (Set point - actual speed)')
            plt.xlabel('time in s')
            plt.ylabel('speed in km/h')
            plt.title('Speed Setpoint Diagram'+' '+str(expand_title))
            plt.grid(True)
            ax0.legend()
            if return_figure_object:
                return fig

        if str.lower(what) == 'all' or str.lower(what) == str.lower('Motor Power Diagram'): #only print if asked for
            #Motor Power Diagram
            fig, ax0 = plt.subplots(figsize=(8, 3))
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('Pmot1')],label='Motor power car 1',color=color_car1)
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('Pmot2')],label='Motor power car 2',color=color_car2)
            plt.xlabel('time in s')
            plt.ylabel('motor power in W')
            plt.title('Motor Power Diagram'+' '+str(expand_title))
            plt.grid(True)
            ax0.legend()
            if return_figure_object:
                return fig

        if str.lower(what) == 'all' or str.lower(what) == str.lower('SD Diagram'): #only print if asked for
            #SD-Diagram
            fig, ax0 = plt.subplots(figsize=(8, 3))
            ax0.plot(self.results[skipp:,self.column_headers.index('t')], self.results[skipp:,self.column_headers.index('SD')]*100,label='SD')
            plt.xlabel('time in s')
            plt.ylabel('safety distance in %')
            plt.title('SD Diagram'+' '+str(expand_title))
            plt.grid(True)
            plt.ylim((0,np.amax(self.results[skipp:,self.column_headers.index('SD')]*100)))
            ax0.legend()
            if return_figure_object:
                return fig

        if str.lower(what) == 'all' or str.lower(what) == str.lower('Way Diagram'): #only print if asked for
            #Way-Diagram
            fig, ax0 = plt.subplots(figsize=(8, 3))
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('x1')],label='x1',color=color_car1)
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('x2')],label='x2',color=color_car2)
            plt.xlabel('time in s')
            plt.ylabel('position in m')
            plt.title('Way Diagram'+' '+str(expand_title))
            plt.grid(True)
            ax0.legend()
            if return_figure_object:
                return fig

        if str.lower(what) == 'all' or str.lower(what) == str.lower('Speed Diagram'): #only print if asked for
            #Speed-Diagram
            fig, ax0 = plt.subplots(figsize=(8, 3))
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('v1kmh')],label='v1',color=color_car1)
            ax0.plot(self.results[:,self.column_headers.index('t')], self.results[:,self.column_headers.index('v2kmh')],label='v2',color=color_car2)
            plt.xlabel('time in s')
            plt.ylabel('speed in km/h')
            plt.title('Speed Diagram'+' '+str(expand_title))
            plt.grid(True)
            ax0.legend()
            if return_figure_object:
                return fig
                           
        print('Printing requested Diagrams, default = \'all\'. You can specify single names only.')
        plt.show(block=False) #Finally display all the configured diagrams
