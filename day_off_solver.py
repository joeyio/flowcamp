import minizinc as mzn
import pandas as pd
import numpy as np
from enum import Enum

# load sample data from file
def load_sample_data():
    # load preference data
    sample_data = pd.read_json('./sample_data/sample_data.json')
    # load valid days
    with open('./sample_data/valid_days.data') as file:
        lines = [line.rstrip() for line in file]
    return lines, sample_data

# intermediate processing steps for the day off optimizer
def intermediate_processing(data: pd.DataFrame):
    # stores a 2d array of day preferences only
    pref_table = data[['first_choice', 'second_choice', 'third_choice']].to_numpy()

    # preferences to have the same day off with others
    # minizinc does not allow jagged multi-dim arrays. must create dummy values to fill array, up to # columns = max_number
    same_day_array = data['same_day_as'].str.split(', ', expand=True)
    max_number = same_day_array.shape[1]
    
    # fill empty values with self-references as dummy values
    for i in range(1,max_number):
        same_day_array.loc[:,i].fillna(value = data.person, inplace=True)

    return pref_table, same_day_array, max_number

# initialize the minizinc model from file
def initialize_model(filename: str):
    model = mzn.Model(filename)
    return mzn.Instance(mzn.Solver.lookup("gecode"), model)

# load data into the instance
def populate_model(instance: mzn.Instance, data: pd.DataFrame, intermediate_data: tuple, config_params: set):
    instance["DAYS"] = list(config_params)
    instance["People"] = data['person'].tolist()
    instance["preferences"] = intermediate_data[0]
    instance["dept"] = data['sub_department'].unique().tolist()
    instance["dept_list"] = data['sub_department'].tolist()
    instance["max_same_day_as"] = intermediate_data[2]
    instance["same_day_as_array"] = intermediate_data[1].to_numpy()
    instance["strong_pref_ppl"] = data['strong_pref_ppl'].to_numpy()

# show results
def show_results(instance: mzn.Instance, data: pd.DataFrame):
    result = instance.solve()
    print("\n")
    
    result_table = pd.DataFrame({'name' : data.person, 
                                'assignment' : result.solution.assignment})
    print(result_table)
    print("\nscore: %s" %result.solution.objective)
    return result_table

def day_off_solver(vd: list, preference_data: pd.DataFrame):
    intermediate_data = intermediate_processing(preference_data)
    print(preference_data)

    instance = initialize_model('day_off_python.mzn')
    populate_model(instance, preference_data, intermediate_data, vd)
    return show_results(instance, preference_data)

