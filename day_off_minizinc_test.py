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
                            'third_choice' : ['WED', 'THU', 'MON', 'FRI', 'TUE', 'MON', 'WED', 'THU', 'THU', 'SUN']}).reset_index(drop=True)

print(sample_data)

preference_data = sample_data

# pivoted table to day preferences
pref_table = preference_data[['first_choice', 'second_choice', 'third_choice']].to_numpy()
print(pref_table)

# initialize the minizinc model from file
model = mzn.Model("day_off_python.mzn")
instance = mzn.Instance(mzn.Solver.lookup("gecode"), model)

# load data into the instance
instance["DAYS"] = Enum("Days", list(vd))
instance["People"] = Enum("People", (preference_data['person']).tolist())
instance["preferences"] = pref_table

# show results
result = instance.solve()
print(result.solution.assignment)

result_table = pd.DataFrame({'name' : preference_data.person, 
                             'assignment' : result.solution.assignment})

print(result_table)