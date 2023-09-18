from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import pandas as pd
import day_off_solver as dos

def run_day_off_solver():
    fetch_data = inquirer.select(
        message = 'would you like to see an example or load your own data?',
        choices = ['load sample data', 'load custom data', Choice(value = None, name = "exit")],
        default = 'load sample data'
    ).execute()

    if fetch_data == 'load sample data':
        vd, preference_data = dos.load_sample_data()
        results = dos.day_off_solver(vd, preference_data)

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