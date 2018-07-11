from car_fuzzy_controler import car_fuzzy_controler as ctrl
import numpy as np
import pandas as pd

a = ctrl('Just some identifyer')

SD_steps = 50
dSD_steps = 50

SD_min = 0.1
SD_max = 10
range_SD = np.logspace(-1,1,SD_steps,base=10)

dSD_min = -0.2
dSD_max = 0.2

SD_step_size = (SD_max-SD_min)/(SD_steps-1)
dSD_step_size = (dSD_max-dSD_min)/(dSD_steps-1)

res = np.zeros([SD_steps+1,dSD_steps+1])

for i_SD in range(SD_steps):
    for i_dSD in range(dSD_steps):
        x_SD = range_SD[i_SD] #SD_min+SD_step_size*i_SD
        x_dSD = dSD_min+dSD_step_size*i_dSD
        res[i_SD+1,0] = x_SD
        res[0,i_dSD+1] = x_dSD
        res[i_SD+1,i_dSD+1] = np.clip(a.compute_input(x_SD,x_dSD),0,1)


df = pd.DataFrame(res)
doc_name = 'results.xlsx'
try:
    df.to_excel(doc_name)
    print('Done!')
except:
    print('The file \'{}\' seems to be used by another program, cant write to it. Please close the file and try again!'.format(doc_name))
