import minizinc as mzn
import pandas as pd
from enum import Enum


model = mzn.Model("day_off_python.mzn")
instance = mzn.Instance(mzn.Solver.lookup("gecode"), model)

instance["DAYS"] = Enum("DAYS", ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri"])
instance["People"] = Enum("People", ['bob', 'sally', 'charlie', 'megan'])
instance["preferences"] = [["Sun", "Tue", "Fri"],
                           ["Mon", "Sun", "Tue"],
                           ["Wed", "Thu", "Mon"],
                           ["Sun", "Wed", "Tue"]]

result = instance.solve()

print(result)