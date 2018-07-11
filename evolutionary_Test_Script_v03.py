import evolutionary as evo

#Set up a Test-Population
print('\nTesting population class...')
ID = 'Cars'
population_size = 50
chrome_template = {'year of manufacturing':(1945,2018),'Motorpower':(10,420),'Price':(2000,2000000),'color_r':(0,255),'color_g':(0,255),'color_b':(0,255)}
Cars = evo.population(ID,population_size,chrome_template)
Cars.initialize_make_population()

#Propagate some generations for the population
max_generations = 10
recreation_per_generation = 0.25
for gen in range(max_generations):
    print('\n###############\
           \nGeneration {}\
           \n###############'.format(gen))
    #print(Cars.get_all_creature_attributes(only_alive=True)) #In each step list the current existing population
    print('\nNewly generated creature(s) in generation {}:'.format(gen))
    #print(Cars.get_next_generations_children())
    print(Cars.get_creatures_without_fitness_rating())
    #Here you would do the fitness-evaluation of the newly generated creatures
    Cars.move_to_next_generation(int(population_size*recreation_per_generation)) #We can specify to generate more than 1 new creature in each generation
    
#Afterwards dump the population to a .csv-file
#Cars.dump_population_to_csv(csv_german=False)
