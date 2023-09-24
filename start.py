from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import pandas as pd
import day_off_solver as dos

def name_selector(solver: dos.day_off_instance, multi: bool):
    people = inquirer.fuzzy(
        message = ('select two or more people' if multi else 'select a person') + ' (you can type to search, press tab to select):',
        choices = solver.data['person'].tolist(),
        multiselect = multi,
        validate = (lambda result: len(result) > 1) if multi else None,
        invalid_message = "choose at least 2 people"
    ).execute()
    return people

def day_selector(solver: dos.day_off_instance):
    day = inquirer.select(
        message = 'select a day:',
        choices = solver.vd
    ).execute()
    return day

def customize_constraint(solver: dos.day_off_instance):
    while True:
        next_action = inquirer.select(
            message = 'choose a custom constraint type:',
            choices = [
                Choice(value = 1, name = "require a specific day for an individual"),
                Choice(value = 2, name = "exclude a specific day for an individual"),
                Separator(),
                Choice(value = 3, name = "enforce two or more individuals to have the same day"),
                Choice(value = 4, name = "enforce two or more individuals to have different days"),
                Choice(value = None, name = "nevermind, I'm done")
            ],
            default = None
        ).execute()

        if next_action == 1:
            person = name_selector(solver, False)
            day = day_selector(solver)
            solver.addconstraint_day(person, day, True)
        elif next_action == 2:
            person = name_selector(solver, False)
            day = day_selector(solver)
            solver.addconstraint_day(person, day, False)
        elif next_action == 3:
            person = name_selector(solver, True)
            solver.addconstraint_group(person, True)
        elif next_action == 4:
            person = name_selector(solver, True)
            solver.addconstraint_group(person, False)
        else:
            return

        
        solver.addconstraint_run()
        print("manually added constraints:")
        for constraint in solver.branchconstraints:
            print(constraint[1])
        

def run_day_off_solver():
    fetch_data = inquirer.select(
        message = 'would you like to see an example or load your own data?',
        choices = ['load sample data', 'load custom data', Choice(value = None, name = "exit")],
        default = 'load sample data'
    ).execute()

    if fetch_data == 'load sample data':
        solver = dos.day_off_instance()
        solver.load_sample_data()
        solver.solve()
    elif fetch_data == 'load custom data':
        print('oops, that feature isn\'t ready yet.')
        return
    else:
        return

    
    stay = inquirer.select(
        message = 'are you satisfied with this assignment?',
        choices = [Choice(value=True, name = 'no, add custom constraints'), Choice(value = False, name = "yes, I'm done")],
        default = None
    ).execute()

    if stay:
        customize_constraint(solver)
        

def main():
    print('flowcamp alpha version 0.1 \n')

    solver = inquirer.select(
        message = 'select an optimizer (more coming soon!):',
        choices = ['day off solver', Choice(value = None, name = 'exit')],
        default = 'day off solver'
    ).execute()

    if solver == 'day off solver':
        run_day_off_solver()

if __name__ == "__main__":
    main()