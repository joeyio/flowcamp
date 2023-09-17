import minizinc as mzn
import pandas as pd
import numpy as np
import itertools
from enum import Enum

# loads parameters from a text (.txt or .data) file where each item is on a separate line into a list
def load_parameters(filename: str):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines

# load sample data
def load_sample_data():
    return pd.read_json('sample_data.json')

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
    instance["DAYS"] = Enum("Days", list(config_params))
    instance["People"] = data['person'].tolist()
    instance["preferences"] = intermediate_data[0]
    instance["dept"] = Enum("dept", data['sub_department'].unique().tolist())
    instance["dept_list"] = data['sub_department'].tolist()
    instance["max_same_day_as"] = intermediate_data[2]
    instance["same_day_as_array"] = intermediate_data[1].to_numpy()
    instance["strong_pref_ppl"] = data['strong_pref_ppl'].to_numpy()

# show results
def show_results(instance: mzn.Instance, data: pd.DataFrame):
    result = instance.solve()
    print(result)
    print(result.solution.assignment)
    result_table = pd.DataFrame({'name' : data.person, 
                                'assignment' : result.solution.assignment})
    print(result_table)

def main():
    vd = set(load_parameters('valid_days.data'))
    preference_data = load_sample_data()
    intermediate_data = intermediate_processing(preference_data)
    print(preference_data)

    instance = initialize_model('day_off_python.mzn')
    populate_model(instance, preference_data, intermediate_data, vd)
    show_results(instance, preference_data)

if __name__ == '__main__':
    main()

