% parameters
enum DAYS; 
enum People; 
set of int: Choices = 1..3;
array[People, Choices] of DAYS: preferences; 
% int Score = 0;

% variables
array[People] of var DAYS: assignment;
 

% constraints

include "alldifferent.mzn";
constraint alldifferent(assignment);
% constraint score = 

% objective
solve maximize product (p in People) ((assignment[p] == preferences[p, 1])*3 + (assignment[p] == preferences[p, 2])*2 + (assignment[p] == preferences[p, 3])*1)