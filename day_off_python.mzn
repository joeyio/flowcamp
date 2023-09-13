% parameters
enum DAYS; 
enum People::add_to_output; 
enum dept;
set of int: Choices = 1..3;
array[People, Choices] of DAYS: preferences; 
array[People] of dept: dept_list;
% int Score = 0;

% variables
array[People] of var DAYS: assignment::add_to_output;
 

% constraints

include "alldifferent.mzn";
% constraint alldifferent(assignment);

% no more than 1 person in a sub dept can take the same day off
constraint forall (q, r in People where dept_list[q] == dept_list[r] /\ q != r) (assignment[q] != assignment[r]);

% objective
solve maximize product (p in People) ((assignment[p] == preferences[p, 1])*3 + (assignment[p] == preferences[p, 2])*2 + (assignment[p] == preferences[p, 3])*1)

%output ["\(p\)     \(assignment[p]\)" | p in People];