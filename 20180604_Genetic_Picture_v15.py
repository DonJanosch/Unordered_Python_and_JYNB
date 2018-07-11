import os, copy
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
from skimage.color import rgb2lab, deltaE_cie76
from math import exp
import evolutionary as evo

#Set parameters
my_path = 'C:\\Users\MacenkaJ\\Desktop\\_Aufgeräumt\\PY_Test\\WinPython-64bit-3.5.4.1Qt5\\notebooks\\dev_Evolutionary_algorithm'
picture_name = 'cloud.jpg'
picture_name = 'images.jpg'

os.chdir(my_path)

original_picture = misc.imread(picture_name)
original_picture_squared = np.square(original_picture)
max_color_distance = np.sum(np.sum(original_picture_squared,axis = 2))
empty_picture = np.ones_like(original_picture)*255
y_max = original_picture.shape[0]-1
x_max = original_picture.shape[1]-1

genetic_pictures = []
genetic_pictures.append(np.ones_like(original_picture)*255)

#Define parameters
ID = 'Pictures'
population_size = 10
max_generations = 20
recreation_per_generation = 0.2
mutation_rate = 0.05
max_shapes = 2000
draw_all = False
chrome_template = {'x_pos':(1,x_max),'y_pos':(1,y_max),'height':(1,max(x_max,y_max)),'width':(1,max(x_max,y_max)),'r_val':(0,255),'g_val':(0,255),'b_val':(0,255),'opaqueness':(0,1)}

#Create the population

Pictures = evo.population(ID,population_size,chrome_template)
Pictures.set_mutation_rate(mutation_rate)
Pictures.initialize_make_population()

#Define fitness-evaluation-function

def get_color_distance(canvas):
    '''Takes a [x,y,3] matrix of RGB-Color-Values between 0 and 255.
    Returns a [x,y,1] matrix with the scalar length value of th color distance-vector.
    With color-distance 0 in every pixel, both pictures are identical.'''
    global original_picture_squared
    canvas_squared = np.square(canvas)
    color_distance_vector = original_picture_squared - canvas_squared
    return color_distance_vector.sum(axis=2)    

def draw_picture(creature_object,canvas):
    current_picture = copy.copy(canvas)
    x_low = max(int(creature_object['x_pos']-creature_object['width']/2),1)
    x_high = min(int(creature_object['x_pos']+creature_object['width']/2),x_max-1)
    y_low = max(int(creature_object['y_pos']-creature_object['width']/2),1)
    y_high = min(int(creature_object['y_pos']+creature_object['width']/2),y_max-1)
    overlapColoring = np.array([creature_object['r_val']*creature_object['opaqueness'],creature_object['g_val']*creature_object['opaqueness'],creature_object['b_val']*creature_object['opaqueness']], dtype=np.uint8)
    current_picture[y_low:y_high,x_low:x_high,:] = np.array(current_picture[y_low:y_high,x_low:x_high,:]*(1-creature_object['opaqueness']),dtype=np.uint8)+overlapColoring
    return current_picture

def eval_fitness(creature_object,canvas):
    global original_picture, max_color_distance
    treshholds = [(1000,0),(200,1),(150,2),(100,5),(80,8),(50,10),(20,20),(10,50),(0,500)]#[(20,10),(0,100)]#
    eval_picture = draw_picture(creature_object,canvas)
    color_distance = get_color_distance(eval_picture)
    fitness_array = np.zeros_like(color_distance)
    for pair in treshholds:
        fitness_array[color_distance<pair[0]]=pair[1]
    fitness = np.sum(fitness_array)
    return int(fitness)

plt.ion() #Turn on interactive Matplotlyb-Mode
fig, ax = plt.subplots(2,1) #Generate subplot

ax[0].imshow(original_picture)

best_health = [1]

#Propagate some generations for the population
for shape in range(max_shapes):
    canvas = genetic_pictures[-1]
    health = 0
    iiter = 0
    while health < best_health[-1] or iiter < max_generations:
        iiter+=1
    #for gen in range(max_generations):
        #print('\nNewly generated creature(s) in generation {}:'.format(gen))
        Pictures.move_to_next_generation(int(population_size*recreation_per_generation)) #We can specify to generate more than 1 new creature in each generation
        new_creatures = Pictures.get_creatures_without_fitness_rating()
        for idx,creature in Pictures.get_all_creature_attributes(only_alive=True).iterrows():
            evaluated_fitness = eval_fitness(Pictures.get_creature_attributes_by_id(ID=idx),canvas)
            if evaluated_fitness > health: health = evaluated_fitness
            Pictures.set_creature_fitness(idx,evaluated_fitness)
        best_picture_creature = draw_picture(Pictures.get_best_creature_attributes(),canvas)
        if draw_all:
            print('Calculating Generation {} // {}'.format(gen,Pictures.get_best_and_average_population_fitness()))
            ax[1].clear()
            ax[1].imshow(best_picture_creature)
            plt.show()
            plt.pause(0.0001)
    print('Done evolving shape {}/{} // {}'.format(shape,max_shapes,Pictures.get_best_and_average_population_fitness()))
    best_health.append(health)
    genetic_pictures.append(best_picture_creature)
    ax[1].clear()
    ax[1].imshow(genetic_pictures[-1])
    plt.show()
    plt.pause(0.01)
    Pictures.reinitialize_population()
    #print('Best creature in {} is \n{}'.format(ID,Pictures.get_best_creature_attributes()))

plt.ioff() #Turn off interactive Matplotlyb-Mode

print('done')
