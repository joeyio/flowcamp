import minizinc as mzn
import pandas as pd
import numpy as np
import itertools
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
                            'same_day_as': ['sally', 'bob', 'alice, bob, zach', 'mark, alice' , 'kristen, megan, sally', 'john', 'john, mark', 'alice, rich', 'charlie', 'john'],
                            # 'same_day_as': ['sally, alice', 'bob, zach', 'alice, bob', 'mark, alice' , 'kristen, megan', 'john, rich', 'john, mark', 'alice, rich', 'charlie, megan', 'john, kristen'],
                            'strong_pref_ppl' : [1,0,1,1,0,0,1,0,1,1]
                            }).reset_index(drop=True)

print(sample_data)

preference_data = sample_data

# intermediate processing steps

# day preferences
pref_table = preference_data[['first_choice', 'second_choice', 'third_choice']].to_numpy()

# preferences to have the same day off with others
# minizinc does not allow jagged multi-dim arrays. must create dummy values to fill array, up to # columns = max_number

same_day_array = preference_data['same_day_as'].str.split(', ', expand=True)
max_number = same_day_array.shape[1]
# print(max_number)
for i in range(1,max_number):
    same_day_array.loc[:,i].fillna(value = preference_data.person, inplace=True)
#.to_numpy()
# 


#np.array(list(itertools.zip_longest(preference_data['same_day_as'].tolist(), fillvalue='')), dtype=object)

# print(same_day_array)

# people list
# ppl_list = preference_data['person'].tolist()
# ppl_list.append('null_val')

# print("people list:")
# print(ppl_list)


# initialize the minizinc model from file
model = mzn.Model("day_off_python.mzn")
instance = mzn.Instance(mzn.Solver.lookup("gecode"), model)

# load data into the instance
instance["DAYS"] = Enum("Days", list(vd))
#instance["People"] = Enum("People", (preference_data['person']).tolist())
instance["People"] = preference_data['person'].tolist()
instance["preferences"] = pref_table
instance["dept"] = Enum("dept", preference_data['sub_department'].unique().tolist())
instance["dept_list"] = preference_data['sub_department'].tolist()
instance["max_same_day_as"] = max_number
instance["same_day_as_array"] = same_day_array.to_numpy()
instance["strong_pref_ppl"] = preference_data['strong_pref_ppl'].to_numpy()

# show results
result = instance.solve()
print(result)

print(result.solution.assignment)

result_table = pd.DataFrame({'name' : preference_data.person, 
                             'assignment' : result.solution.assignment})

print(result_table)
