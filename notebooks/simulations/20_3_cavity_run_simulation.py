from itertools import combinations
import numpy as np
from oxDNA_analysis_tools.UTILS.oxview import oxdna_conf, from_path
from oxDNA_analysis_tools.UTILS.RyeReader import describe, get_confs, inbox
from pathlib import Path
import os
from ipy_oxdna.dna_structure import DNAStructure, DNAStructureStrand, load_dna_structure, DNABase, strand_from_info
from copy import deepcopy
from ipy_oxdna.oxdna_simulation import Simulation , SimulationManager
import copy
from tqdm.auto import tqdm
 

# create relxation simulation 
path = '/home/azare3/20_3_cavity/structur_file'
file_dir = os.path.join(path,'original_file')

path2 = '/home/azare3/20_3_cavity/structur_file'
sim_dir = sim_dir = os.path.join(path2,'relaxed')

sim = Simulation(file_dir, sim_dir)
sim.build(clean_build='force')      
sim.input.swap_default_input("cpu_MC_relax")
#  Run relaxation simulation
sim.oxpy_run.run(join = True)

________________________________________________________________________________

# create equilibrium simulation
path = '/home/azare3/20_3_cavity/structur_file'
file_dir = os.path.join(path,'relaxed')

path2 = '/home/azare3/20_3_cavity/structur_file'
sim_dir = sim_dir = os.path.join(path2,'eq')

eq_sim = Simulation(file_dir, sim_dir)
eq_steps = 1e7
eq_parameters = {'dt':f'0.003','steps':f'{eq_steps}','print_energy_every': f'1e5', 'interaction_type': 'DNA2',
                           'print_conf_interval':f'1e5', 'fix_diffusion':'false', 'T':f'20C','max_density_multiplier':f'50'}

eq_sim.build(clean_build='force')
eq_sim.input_file(eq_parameters)
eq_sim.oxpy_run.run(join = True)

___________________________________________________________________________________


# create production simulation
path = '/home/azare3/20_3_cavity/structur_file'
file_dir = os.path.join(path,'eq')

path2 = '/home/azare3/20_3_cavity/structur_file'
sim_dir = sim_dir = os.path.join(path2,'prod')

prod_sim = Simulation(file_dir, sim_dir)
prod_steps = 1e9
prod_parameters = {'dt':f'0.003','steps':f'{prod_steps}','print_energy_every': f'1e5', 'interaction_type': 'DNA2',
                           'print_conf_interval':f'1e5', 'fix_diffusion':'false', 'T':f'20C','max_density_multiplier':f'50'}
prod_sim.build(clean_build='force')
prod_sim.input_file(prod_parameters)
prod_sim.oxpy_run.run(join = True)