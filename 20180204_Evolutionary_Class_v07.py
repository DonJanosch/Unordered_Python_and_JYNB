import numpy as np
import pandas as pd
import bisect

class creature: #Creature class
    '''Creature class, that constructs a creature for genetic-optimizing algorithms.
    Each chreature has a fixed set of parameters which are 'id','fitness','generation','mother','father'
    and can have an arbitrary amount of 'chromosomes'.
    Class has helper functions to call or update the creatures parameters.
    
    Current_version: 00 / 2018-02-04'''
    def __init__(self,id_int,chrome,generation = 0, mother = '', father = ''): #Initial constructor to create and set parameters
        '''Function for initial set up of creature class.
        INPUT id_int as integer, will be used as ID (identifyer).
        INPUT chrome as dictionary to initialize the creatures chromosomes like {'age':5,'height':7.25,'name':'David',...}
        NOTE: In a population, all creatures should share the same chromes.'''
        self.id_int = int(id_int) #Accept the specified ID
        self.chrome_names = [] #Containers for the chome names, will be filled from looping through input dictionary
        self.chrome_values = [] #Containers for the chome values, will be filled from looping through input dictionary
        for key,value in chrome.items(): #Loop over the specified dictionary and make lists of the values
            self.chrome_names.append(key) #The key is the chromes name and will be used as column-identifyer
            self.chrome_values.append(value) #The value is the value for the chrome to be used later on
        self.fitness = 0 #Each creature has a fitness value (positive integer) which gets updated regularely, is initialized to 0
        self.generation = generation #Remember the generation, the creature was born, default is 0
        self.mother = mother #Remember the creatures mother, default is ''
        self.father = father #Remember the creatures father, default is ''     

    def get_all_data(self): #Function to generate a pd.DataFrame wich holds all creature data
        '''Function that returns all the creatures attributes as a pandas.DataFrame
        OUTPU: pandas.DataFrame, always includes the columns 'id','fitness','generation','mother','father'
        and as many more rows as there are chromosomes which were specified by 'chrome' in the __init__-function during construction.'''
        header = {'id':[self.id_int],'fitness':[self.fitness],'generation':[self.generation],'mother':[self.mother],'father':[self.father]} #Generates the header as dictionary for the pandas.DataFrame, the header is always consistent
        data = {self.chrome_names[i]:[self.chrome_values[i]] for i in range(len(self.chrome_names))} #Generates the data part (also dictionary) of the creature which holds all the genes (can be arbitrary number)
        crt = pd.DataFrame.from_dict(header) #Turns the just created dictionaries into pandas.DataFrames
        dat = pd.DataFrame.from_dict(data) #Turns the just created dictionaries into pandas.DataFrames
        crt = crt.join(dat) #Joins the two pandas.DataFrames
        crt = crt.set_index('id') #Sets the 'id' column to be the identifier
        return crt #Returns the pandas.DataFrame of the creature, it consists of just one row but is configured with column-names for easy use with other data sets

    def get_fitness(self): #Get-Function for fitness value
        '''Function that returns the creatures current fitness (usually a positive integer)'''
        return self.fitness #Returns the creatures current fitness value (usualy a positive integer)

    def set_fitness(self,fitness): #Set-Function for fitness value
        '''Function that sets the creatures current fitness (usually a positive integer)'''
        self.fitness = fitness #Sets the creatures current fitness value (usualy a positive integer)

class population: #Population class, that manages a population of creatures, evaluates their fitness and creates offspring
    '''Population class for genetic optimizer which manages the population and evolves it.
    The populaion consits of a specified number of creatures (another class) which have certain attributs called chromosomes.
    Chromosomes are the parameters, you want to have optimized for your problem.
    Initially the creatures are initialized with random values for the coromosomes within chromosome specific min/max values.
    The evolutionary process consists of the following steps:
        0. Initialize the population
        1. Measure each creatures fitness with a fitness function (usually by 'observing' the behaviour of each creature in a simulation and rating it with a fitness score (positive integer), this has to be done outside of this class by your specification)
        2. Select two parents from the population to 'produce' an offspring, the chance of getting picked scales with the creatures fitness-value
        3. Cros-Over the chromosomes of the 'mother' and 'father' creature to generate the offspring
        4. Randomly apply mutation (add or subtract random value) to the childs chomosomes
        5. Replace a creature from the current population, lower fittnes-value creatures have higher chances of getting picked
    Repeat step 1-5 until the best creature either is fit enough to meet your criteria or the set amount of evolution-epocs is over.
    Finally pick the best creatures chromosomes, these are your optimized values.
    
    Current_version: 00 / 2018-02-04'''
    def __init__(self,name,population_count,chromosomes,*creatures, chromosome_min_values=[],chromosome_max_values=[],mutation_rate = 0.05):
        self.name = name
        self.population_count = population_count
        self.chromosomes = chromosomes
        self.mutation_rate = mutation_rate
        self.chromosome_min_values = list(np.zeros(len(chromosomes)))
        if len(chromosome_min_values)== len(chromosomes):
            self.chromosome_min_values = chromosome_min_values
        self.chromosome_max_values = list(np.ones(len(chromosomes)))
        if len(chromosome_max_values)== len(chromosomes):
            self.chromosome_max_values = chromosome_max_values
        self.creatures = [] #Container to hold the creatures
        for creature in creatures: #Fill the container with the creatures that have been specified to the class constructor, loop over the list
            self.creatures.append(creature) #Append the creatures to the container
        for idx in range(len(self.creatures),int(self.population_count)):
            self.creatures.append(self.make_new_creature(idx))
        self.initialize_creatures_chromes()
        simulation_result_parameters = ['epoc','best_creatures_fitness','average_population_fitness','best_creatures_id','worst_creatures_id','mother_id','father_id','replaced_creatures_id','best_creatures_genes']
            #TO BE DEVELOPED: Make a function that memorizes the simulation_result_parameters as a pd.DataFrame and another one that saves them to a .csv file
        self.update_population_state() #Call function to initially update the internal memory
 
    def initialize_creatures_chromes(self,enforce_reset = False):
        '''Function to initialize all chromosomes of each creature in the population.
        By default, only creatures with chromosome-values of None are initialized. This way you can input special creatures when
        initializing your population and these are not change. You can force the re-initialization of ALL creatures by setting the
        enforce_reset-flag to True.'''
        for idx, creature in enumerate(self.creatures):
            for idy, value in enumerate(creature.chrome_values):
                if value == ['None'] or enforce_reset: #Spare specific inputted creatures (eg. at first initialization) from the randomization if not the enfoce_reset flag is set
                    chr_min = self.chromosome_min_values[idy]
                    chr_max = self.chromosome_max_values[idy]
                    chr_delta = chr_max-chr_min
                    self.creatures[idx].chrome_values[idy] = chr_min+chr_delta*np.random.random() #TO BE DEVELOPED: Take into consideraton the min/max values of the creatures chromosome

    def make_new_creature(self, id_int):
        return creature(id_int, {chrome:['None'] for chrome in self.chromosomes})
        
    def update_population_state(self):
        '''Function updates the internal pd.DataFrame which holds all the creatures parameters.
        Used internaly for determining best and worst creatures.'''
        self.memory = pd.DataFrame()
        for creature in self.creatures:
            self.memory = self.memory.append(creature.get_all_data())

    def cross_over(self,mother_id,father_id,mutation_rate = None,co_method='single point crosover'):
        if mutation_rate == None:
            mutation_rate = self.mutation_rate

    def cdf(weights):
        total = sum(weights)
        result = []
        cumsum = 0
        for w in weights:
            cumsum += w
            result.append(cumsum / total)
        return result
    
    def choice(population, weights):
        assert len(population) == len(weights)
        cdf_vals = cdf(weights)
        x = np.random.random()
        idx = bisect.bisect(cdf_vals, x)
        return population[idx]

    def choiceID(population, weights):
        assert len(population) == len(weights)
        cdf_vals = cdf(weights)
        x = np.random.random()
        idx = bisect.bisect(cdf_vals, x)
        return idx


        

#np.random.seed(0) #Seeding random values
population_name = 'Females on earth'
population_count = 30
chromes = ['Alter','Schönheit']
chr_min = [20,1]
chr_max = [35,10]
females = []

for idx in range(population_count):
    age = np.random.randint(1,100)
    beauty = np.random.randint(1,10)
    attributes = {chromes[0]:age,chromes[1]:beauty}
    females.append(creature(idx,attributes))

population_count = 40

females_on_earth = population(population_name,population_count,chromes,*females,chromosome_max_values=chr_max,chromosome_min_values=chr_min,mutation_rate = 0.7)
print(females_on_earth.creatures[0].get_all_data())
print(females_on_earth.memory)
females_on_earth.initialize_creatures_chromes(enforce_reset = True)
females_on_earth.update_population_state()
print(females_on_earth.memory)
