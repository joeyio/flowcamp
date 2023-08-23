# flowcamp

flowcamp is an experimental Artificial Intelligence optimization project that represents many logistical and scheduling tasks at summer camp as Constraint Optimization Problems (COPs) to generate an AI solution. It utilizes the MiniZinc constraint modelling language and integrates into Python using the MiniZinc Python library. 

# motivation 

Investing in young people is a significant emphasis of the Seventh-day Adventist Church, which owns and operates over 60 summer camps in North America. While camp is a valuable and effective ministry tool, a natural consequence of its high-pace environment and rapid turnover are grossly inefficient processes that often lead to burnout. Camp poses a unique and complex logistical problem because it involves many moving parts that are highly variable from week to week, making it difficult to create established institutional routines. Problem solving and scheduling create a significant administrative burden that absorbs valuable time. To ease this problem, logistical questions can be represented as an Integer Linear Programming (ILP) problem, which is a well-studied domain. 

# roadmap

This project is a candidate project for my undergraduate senior honors thesis and may be developed sporadically. Here is an approximate roadmap for development:
- Proof of concept: develop a COP solver for scheduling days off among departments
- Main project: develop a full COP solver for weekly cabin assignments, classes, subs, and other duties
- Establish API integration with Google Sheets for efficient data entry 
- Develop a flexible initial setup routine that allows broad one-time customization for various organizations 
- Integrate a Large Language Model with named entity recognition to allow user feedback and user-added constraints to the solution. 
- Bundle all programs into a streamlined GUI

# installation 
1. Visit the minizinc website https://www.minizinc.org/ and follow the installation guide to download and install the compiler. 
2. Run ```console  
pip install -r requirements.txt
python day_off_minizinc_test.py
```