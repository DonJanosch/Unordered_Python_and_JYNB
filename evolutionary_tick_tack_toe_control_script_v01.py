import evolutionary as evo

#Set up a Test-Population
print('\nTesting population class...')
ID = 'Tick_Tack_Toe_AI'
population_size = 50
chrome_template = {'year of manufacturing':(1945,2018),'Motorpower':(10,420),'Price':(2000,2000000),'color_r':(0,255),'color_g':(0,255),'color_b':(0,255)}
Cars = evo.population(ID,population_size,chrome_template)
Cars.initialize_make_population()

def eval_fitness(year_of_manufacturing,motorpower,price,reporting=False):
    fitness = int((motorpower*10000/price)*(1+(year_of_manufacturing-1945)**0.5))
    if reporting: print('Motorpower {}, YOM {}, Price {}, Fitness {}'.format(motorpower,year_of_manufacturing,price,fitness))
    return fitness

#Propagate some generations for the population
max_generations = 10
recreation_per_generation = 0.25
for gen in range(max_generations):
    print('\n###############\
           \nGeneration {}\
           \n###############'.format(gen))
    print('\nNewly generated creature(s) in generation {}:'.format(gen))
    new_creatures = Cars.get_creatures_without_fitness_rating()
    for idx,creature in new_creatures.iterrows():
        evaluated_fitness = eval_fitness(creature['year of manufacturing'],creature['Motorpower'],creature['Price'])
        Cars.set_creature_fitness(idx,evaluated_fitness)
    Cars.move_to_next_generation(int(population_size*recreation_per_generation)) #We can specify to generate more than 1 new creature in each generation
    
#Afterwards dump the population to a .csv-file
Cars.dump_population_to_csv(csv_german=False)
