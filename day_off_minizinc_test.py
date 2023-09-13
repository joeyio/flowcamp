import minizinc as mzn
import pandas as pd
import numpy as np
from enum import Enum

# changeable parameters 
vd = {"SUN", "MON", "TUE", "WED", "THU", "FRI"}

# sample data
sample_data = pd.DataFrame(data = {'person' : ['bob', 'sally', 'charlie', 'megan', 'alice', 'zach', 'rich', 'john', 'kristen', 'mark'],
                            'department' : pd.Series(['small class']).repeat(10),
                            'sub_department' : ['atv', 'art', 'stem', 'culinary', 'art', 'bikes', 'bikes', 'culinary', 'atv', 'stem'],
                            'first_choice' : ['SUN', 'TUE', 'FRI', 'THU', 'SUN', 'TUE', 'TUE', 'WED', 'FRI', 'TUE'],
                            'second_choice' : ['MON', 'SUN', 'SUN', 'TUE', 'WED', 'THU', 'SUN', 'FRI', 'SUN', 'WED'],
                            'third_choice' : ['WED', 'THU', 'MON', 'FRI', 'TUE', 'MON', 'WED', 'THU', 'THU', 'SUN'],
                            'same_day_as': [['sally'],['bob'],['alice', 'bob', 'zach'],['mark', 'alice'],['kristen', 'megan', 'sally'],['john'],['john', 'mark'],['alice', 'rich'],['charlie'],['john']],
                            'strong_pref_ppl' : [1,0,1,1,0,0,1,0,1,1]
                            }).reset_index(drop=True)

print(sample_data)

preference_data = sample_data

# intermediate processing steps

# day preferences
pref_table = preference_data[['first_choice', 'second_choice', 'third_choice']].to_numpy()

# preferences to have the same day off with others
length_vector = preference_data['same_day_as'].str.len()
print(length_vector)

# initialize the minizinc model from file
model = mzn.Model("day_off_python.mzn")
instance = mzn.Instance(mzn.Solver.lookup("gecode"), model)

# load data into the instance
instance["DAYS"] = Enum("Days", list(vd))
instance["People"] = Enum("People", (preference_data['person']).tolist())
instance["preferences"] = pref_table
instance["dept"] = Enum("dept", preference_data['sub_department'].unique().tolist())
instance["dept_list"] = preference_data['sub_department'].tolist()

# show results
result = instance.solve()
print(result)

print(result.solution.assignment)

result_table = pd.DataFrame({'name' : preference_data.person, 
                             'assignment' : result.solution.assignment})

print(result_table)
