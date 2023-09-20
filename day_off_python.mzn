% parameters
enum DAYS; 
enum People; 
enum dept;
set of int: Choices = 1..3;
array[People, Choices] of DAYS: preferences; 
array[People] of dept: dept_list;
int: max_same_day_as;
set of int: same_day_set = 1..max_same_day_as;
array[People, same_day_set] of People: same_day_as_array;
array[People] of int: strong_pref_ppl;

% int Score = 0;

% variables
array[People] of var DAYS: assignment::add_to_output;
 

% constraints

include "alldifferent.mzn";
% constraint alldifferent(assignment);

% TODO: add global constraint that no more people can take the same day off in the small class dept than there are subs

% TODO: modify this constraint to specify maximum numbers of people in a sub department that can take a day off at the same time, instead of a hard coded 1
% no more than 1 person in a sub dept can take the same day off
constraint forall (q, r in People where dept_list[q] == dept_list[r] /\ q != r) (assignment[q] != assignment[r]);

% objective
var int: pref_score = sum (p in People) (((assignment[p] == preferences[p, 1])*3 + (assignment[p] == preferences[p, 2])*2 + (assignment[p] == preferences[p, 3])*1) + (1 - strong_pref_ppl[p]) );
var int: ppl_score = sum (p in People, n in same_day_set) ((if p != same_day_as_array[p, n] then 2*(assignment[p] == assignment[same_day_as_array[p, n]]) else 1 endif) + (strong_pref_ppl[p]) );

solve maximize pref_score + ppl_score;

%output ["\(p\)     \(assignment[p]\)" | p in People];