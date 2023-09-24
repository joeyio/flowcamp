import minizinc as mzn
import pandas as pd
import numpy as np
from enum import Enum

class day_off_instance:
    def __init__(self):
        self.data = None
        self.vd = None
        self.intermediate_data = None
        self.instance = None
        self.branchconstraints = []
        self.result = None
    
    # load sample data from file
    def load_sample_data(self):
        # load preference data
        self.data = pd.read_json('./sample_data/sample_data.json')
        # load valid days
        with open('./sample_data/valid_days.data') as file:
            self.vd = [line.rstrip() for line in file]
        
    # intermediate processing steps for the day off optimizer
    def intermediate_processing(self):
        # stores a 2d array of day preferences only
        pref_table = self.data[['first_choice', 'second_choice', 'third_choice']].to_numpy()

        # preferences to have the same day off with others
        # minizinc does not allow jagged multi-dim arrays. must create dummy values to fill array, up to # columns = max_number
        same_day_array = self.data['same_day_as'].str.split(', ', expand=True)
        max_number = same_day_array.shape[1]
        
        # fill empty values with self-references as dummy values
        for i in range(1,max_number):
            same_day_array.loc[:,i].fillna(value = self.data.person, inplace=True)

        self.intermediate_data = (pref_table, same_day_array, max_number)

    # initialize the minizinc model from file
    def initialize_model(self, filename: str):
        model = mzn.Model(filename)
        self.instance = mzn.Instance(mzn.Solver.lookup("gecode"), model)

    # load data into the instance
    def populate_model(self):
        self.instance["DAYS"] = list(self.vd)
        self.instance["People"] = self.data['person'].tolist()
        self.instance["preferences"] = self.intermediate_data[0]
        self.instance["dept"] = self.data['sub_department'].unique().tolist()
        self.instance["dept_list"] = self.data['sub_department'].tolist()
        self.instance["max_same_day_as"] = self.intermediate_data[2]
        self.instance["same_day_as_array"] = self.intermediate_data[1].to_numpy()
        self.instance["strong_pref_ppl"] = self.data['strong_pref_ppl'].to_numpy()

    # add constraints during runtime
    def addconstraint_run(self):
        with self.instance.branch() as child:
            for constraint in self.branchconstraints:
                child.add_string(constraint[0])
            self.show_results(child)
            # TODO: additional constraints need to be cached in a buffer, then loaded simultaneously into a branch

    # def solve_branch(self):

    # enforce a specific day for an individual (or specify NOT)
    def addconstraint_day(self, person: str, day: str, positive: bool):
        # ensure the person and day are valid
        if person in self.data['person'].to_list() and day in self.vd:
            # the require case
            if positive:
                self.branchconstraints.append((f'constraint assignment[{person}] = {day};\n', '{person} must have {day}'))
                print(self.branchconstraints[0][0])
            # the prohibit case
            else:
                self.branchconstraints.append((f'constraint assignment[{person}] != {day};\n', '{person} cannot have {day}'))
        else: 
            print("that combination is invalid. please try again")
         
    # enforce given individuals to have the same day as each other (and specify different)
    def addconstraint_group(self, people: list, positive: bool):
        length = len(people)
        # ensure the people exist
        if set(people).issubset(self.data['person']) and length > 1:
            people_str = '[%s]' % ', '.join(map(str, people))
            # the same day case
            if positive:
                self.branchconstraints.append((f'array[1..{length}] of People: branch_people = {people_str};\nconstraint forall(b, c in branch_people) (assignment[b] = assignment[c]);\n',
                                               '{people_str} all have the same day'))
                print(self.branchconstraints[0][0])
            else:
                self.branchconstraints.append((f'array[1..{length}] of People: branch_people = {people_str};\nconstraint forall(b, c in branch_people where b != c) (assignment[b] != assignment[c]);\n',
                                               '{people_str} all have different days'))


    # show results
    def show_results(self, instance: mzn.Instance):
        result = instance.solve()
        print("\n")
        
        result_table = pd.DataFrame({'name' : self.data.person, 
                                    'assignment' : result.solution.assignment})
        print(result_table)
        print("\nscore: %s" %result.solution.objective)

        self.result = result_table
        

    def solve(self):
        self.intermediate_processing()
        print(self.data)

        self.initialize_model('day_off_python.mzn')
        self.populate_model()
        self.show_results(self.instance)

