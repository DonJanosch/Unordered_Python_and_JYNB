'''
Description and Disclaimer: ... to be written :-P
'''

import numpy as np
import pandas as pd
import random

class creature:
    '''Creature class which contains a fixed amout of attributes which are 'ID','fitness','generation','mother_ID' and 'father_ID'.
    Also holds an arbitrary amount of chormosomes which are a dictionary like {'name':brutus,'age':5,'legs':4,...}
    Has some helper-functions to update or load stats'''
    def __init__(self,ID_int,chromes,fitness = 0,birth_generation = 0,mother='',father='',extinct = False):
        '''Function to initialize the Creature and set parameters
        INPUT ID_int: Accepts an integer as creatures ID, should be unique within a population
        INPUT chromes: Accepts a dictionary of arbitrary length like {'name':brutus,'age':5,'legs':4,...}, the governing population class needs to make sure each creature within the population has the same attributes'''
        self.flag_not_set = ''
        self.id = int(ID_int)
        self.fitness = fitness
        self.birth_generation = birth_generation        
        self.extinct_generation = self.flag_not_set
        self.mother = mother
        self.father = father
        self.chromes = chromes
        self.extinct = extinct
        self.fitness_evaluated = False

    def get_id(self):
        '''Get function which returns ID as integer.'''
        return self.id

    def get_fitness(self):
        '''Get function which returns fitness as integer.'''
        return self.fitness

    def get_all_parameters(self):
        '''Get function which returns a pandas-DataFrame with parameters and chromes as column-headers and values as first row.'''
        fixed_parameters = pd.DataFrame.from_dict({'id':[self.id],'fitness':[self.fitness],'fitness_evaluated':[self.fitness_evaluated],'birth_generation':[self.birth_generation],'extinct_generation':[self.extinct_generation],'mother':[self.mother],'father':[self.father],'extinct':[self.extinct]})
        variable_parameters = pd.DataFrame.from_dict({a:[b] for a,b in self.chromes.items()})
        df = fixed_parameters.join(variable_parameters)
        df= df.set_index('id')
        return df

    def get_chromes(self):
        '''Get function which returns the creatures chromes as a dictionary.'''
        return self.chromes

    def set_fitness(self,fitness_int,reset_fitness_evaluated=False):
        '''INPUT fitness_int: Accepts an non negative integer as new fitness value.
        Additionally sets the fitness_evaluated flag to True, first time the Fitness is evaluated.
        This can be reversed with the functions optional input-flag reset_fitness_evaluated=True'''
        self.fitness = max(0,int(fitness_int))
        if reset_fitness_evaluated:
            self.fitness_evaluated = False
        else:
            self.fitness_evaluated = True
        
    def set_creature_extinct(self,extinct_generation,inverse=False):
        '''Function which accepts the current generation as integer, to set the creatures state-flag to extinct. To distinguishe alive from dead creatures.'''
        self.extinct = True
        self.extinct_generation = int(extinct_generation)
        if inverse:
            self.extinct = False
            self.extinct_generation = self.flag_not_set

class population:
    def __init__(self,ID,population_size_int,chromosome_template,mutation_rate = 0.05):
        self.id = ID
        self.creature_id_counter = -1
        self.generation = 0
        self.population_size = int(population_size_int)
        self.chromosome_template = chromosome_template
        self.mutation_rate = mutation_rate
        self.avaliable_cross_over_methods = {'SPCO':'Single point cross over at random point in genomes','H2H':'Half and half, first genome of mother, second of father, third of mother and so on.'}
        self.cross_over_method = 'SPCO'
        self.extinct_selection_method = 'random'
        template_creature = creature(-1,{key:0 for key,value in chromosome_template.items()})
        template_creature = template_creature.get_all_parameters()
        self.creature_attribute_list = template_creature.drop(template_creature.index)
        self.creatures = []
        self.flag_not_set = ''

    def initialize_make_population(self):
        '''Function without input parameter which initially generates the generation 0 population from the chromosome template. No return values, just internals for the class.'''
        for idx in range(len(self.creatures),self.population_size):
            chromes = {a:random.uniform(b[0],b[1]) for a,b in self.chromosome_template.items()}
            ID = self.generate_next_creature_id()
            next_creature = creature(ID,chromes,father=None,mother=None)
            self.append_creature_to_population(next_creature)

    def initialize_fill_population(self):
        '''Function wich fills a population with random creatures up to the specified population sice, asuming that some "handcrafted" creatures were inserted into the population already.'''
        self.creature_attribute_list = self.creature_attribute_list.drop(self.creature_attribute_list.index) #Drops the current creature_attribute_list
        self.creatures = [] #Drops all current existing creatures
        for idx in range(self.population_size):
            chromes = {a:random.uniform(b[0],b[1]) for a,b in self.chromosome_template.items()}
            ID = self.generate_next_creature_id()
            next_creature = creature(ID,chromes,father=None,mother=None)
            self.append_creature_to_population(next_creature)
            
    def append_creature_to_population(self,creature_to_append):
        '''Accepts a creature-object and appends it to the population-object. No return value.'''
        self.creatures.append(creature_to_append)
        self.creature_attribute_list = self.creature_attribute_list.append(creature_to_append.get_all_parameters())

    def generate_next_creature_id(self):
        '''Helperfunction that increases a counter and '''
        self.creature_id_counter +=1
        return self.creature_id_counter

    def increment_generation(self):
        self.generation +=1

    def get_all_creature_attributes(self,only_alive=False):
        '''Returns a pandas.DataFrame with all the information of the population.
        Accepts optional \'only_alive\'-Flag wich can be se to True if you are only interested in a list of currently alive creatures.'''
        if only_alive:
            return self.creature_attribute_list[self.creature_attribute_list['extinct']==False]
        else:
            return self.creature_attribute_list

    def get_best_creature_attributes(self,attribute = 'fitness',only_id = False,only_alive=False):
        '''Accepts optional attribute as string which must be a creatures parameter like 'fitness' or a chromosome-name.'''
        if only_alive: choice = self.creature_attribute_list[self.creature_attribute_list['extinct']==False]
        else: choice = self.creature_attribute_list
        idx = choice[str(attribute)].idxmax()
        if only_id:
            return idx
        else:
            return  self.creature_attribute_list.iloc[idx]

    def get_worst_creature_attributes(self,attribute = 'fitness',only_id = False,only_alive=False):
        '''Accepts optional attribute as string which must be a creatures parameter like 'fitness' or a chromosome-name.'''
        if only_alive: choice = self.creature_attribute_list[self.creature_attribute_list['extinct']==False]
        else: choice = self.creature_attribute_list
        idx = choice[str(attribute)].idxmin()
        if only_id:
            return idx
        else:
            return  self.creature_attribute_list.iloc[idx]

    def get_parent_id(self, list_of_exclusions = ''):
        '''Accepts optional IDs that shal be excluded as list of integers.'''
        creature_pool = self.creature_attribute_list
        if len(list_of_exclusions) >0:
            creature_pool = creature_pool.drop(list_of_exclusions)
        return np.random.choice(creature_pool.index.values.tolist(),1,creature_pool['fitness'].tolist())[0]

    def get_creature_by_id(self,creature_id):
        '''Accepts a creature ID as integer and returns the creature-object from the population.'''
        return self.creatures[int(creature_id)]

    def set_mutation_rate(self,mutation_rate):
        '''Accepts a new mutation rate as float number for the entire population.'''
        self.mutation_rate = float(mutation_rate)

    def set_extinct_selection_method(self,extinct_selection_method):
        '''Accepts a new selection method for the extinct creature as string, if this is not defined in the population-class, a default method will be used.'''
        self.extinct_selection_method = str(extinct_selection_method)

    def set_crossover_method(self,cross_over_method_as_string):
        '''Accepts a new cross over method as string, if this is not defined in the population-class, a default method will be used.'''
        self.cross_over_method = str(cross_over_method_as_string)

    def get_population_metadata(self):
        '''No input required, returns a dictionary with primary parameters of the population.'''
        return {'Population name':self.id,'Population size':self.population_size,'Generated Creatures':self.creature_id_counter+1,'Current generation':self.generation,'Mutation rate':self.mutation_rate,'Best creature fitness':self.get_best_creature_attributes()['fitness'],'Best creature ID':self.get_best_creature_attributes(only_id=True)}

    def generate_child(self,mother_id_int,father_id_int):
        '''Accepts two creature IDs as integer which will be mother and father.
        Returns a new creature object.'''
        ID = self.generate_next_creature_id()
        new_keys, new_params = [],[]
        #Get all relevant set of chromes
        mother_chromes = self.creatures[int(mother_id_int)].get_chromes()
        father_chromes = self.creatures[int(father_id_int)].get_chromes()
        random_chromes = {a:random.uniform(b[0],b[1]) for a,b in self.chromosome_template.items()}
        #Interlace the chromes with application of mutation
        counter = 0
        for key,_ in random_chromes.items():
            counter+=1
            if np.random.rand()<=self.mutation_rate:
                new_params.append(random_chromes[key])
            elif counter%2==0:
                new_params.append(mother_chromes[key])
            else:
                new_params.append(father_chromes[key])
            new_keys.append(key)            
        #Generate child from new chromes
        new_chromes = dict(zip(new_keys,new_params))
        new_creature = creature(ID,new_chromes,birth_generation=self.generation,mother=mother_id_int,father=father_id_int)
        return new_creature

    def set_creature_fitness(self,creature_id_int,fitness_int):
        '''Accepts an creature ID as integer aswell as a new fitness-value as integer (non-negative) and updates the creature. No return value.'''
        idx = int(creature_id_int)
        self.creatures[idx].set_fitness(fitness_int)
        self.creature_attribute_list.at[idx,'fitness']=fitness_int
        self.creature_attribute_list.at[idx,'fitness_evaluated']=True
        
    def set_creature_extinct(self,creature_id_int,inverse=False):
        '''Accepts an creature ID as integer aswell as a new fitness-value as integer (non-negative) and updates the creature. No return value.'''
        idx = int(creature_id_int)
        if inverse:
            self.creatures[idx].set_creature_extinct(self.generation,inverse=True)
            self.creature_attribute_list.at[idx,'extinct']=False
            self.creature_attribute_list.at[idx,'extinct_generation']=self.flag_not_set
        else:
            self.creatures[idx].set_creature_extinct(self.generation)
            self.creature_attribute_list.at[idx,'extinct']=True
            self.creature_attribute_list.at[idx,'extinct_generation']=self.generation

    def get_list_of_creatures_alive(self):
        '''Function that returns a list with the indexes of currently alive creatures in the population.'''
        return self.creature_attribute_list[self.creature_attribute_list['extinct']==False].index.values

    def move_to_next_generation(self,number_of_children_to_generate_int=1):
        '''Accepts optionaly a number of children to generate per generation.'''
        self.generation+=1
        new_children = []
        for _ in range(number_of_children_to_generate_int):
            mother_id = self.get_parent_id()
            father_id = self.get_parent_id([mother_id])
            if self.extinct_selection_method == 'worst':
                extinct_id = self.get_worst_creature_attributes(only_id=True,only_alive=True)
            elif self.extinct_selection_method == 'random':
            else:
                extinct_id = random.choice(self.get_list_of_creatures_alive())
            self.set_creature_extinct(extinct_id)
            new_children.append(self.generate_child(mother_id,father_id))
        for child in new_children: 
            self.append_creature_to_population(child)

    def get_next_generations_children(self):
        '''Function that returns a DataFrame with the information of the creatures which have recentily been generated.'''
        return self.get_all_creature_attributes()[self.get_all_creature_attributes()['birth_generation']==self.generation]

    def get_creatures_without_fitness_rating(self):
        '''Function that returns a DataFrame with the information of the creatures which have the fitness_evaluated flat set to False.'''
        return self.get_all_creature_attributes()[self.get_all_creature_attributes()['fitness_evaluated']==False]

    def get_best_and_average_population_fitness(self):
        '''Function that returns a tupel with (best_creature_fitness, average_population_fitness).'''
        return (self.get_best_creature_attributes(only_alive=True)['fitness'],self.get_all_creature_attributes(only_alive=True)['fitness'].mean())
    
    def dump_population_to_csv(self,only_alive=False,csv_separator=',',csv_decimal='.',csv_german=False):
        '''Function that generates a .csv-file from the current population-DataFrame (not the actual creature-objects).
        Will prompt where the file was written.'''
        from datetime import datetime
        import os
        path = os.getcwd()
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = timestamp+'_Genetic_simulation_of_{}.csv'.format(self.id)
        entire_path = path + '\\' +file_name
        if bool(csv_german):
            csv_separator=';'
            csv_decimal=','
        with open(entire_path,'w') as f:
            self.get_all_creature_attributes(only_alive=only_alive).to_csv(f,sep=csv_separator,decimal = csv_decimal,index=True, header=True,encoding='utf-8')
        print('The file \'{}\' was generated from the current population and safed to location \'{}\'.'.format(file_name,entire_path))
