% parameters
enum DAYS = {Sun, Mon, Tue, Wed, Thu, Fri};
enum People = {bob, sally, charlie, megan, alice, zach, rich, john, kristen, mark};
set of int: Choices = 1..3;
array[People, Choices] of DAYS: preferences = [|Sun, Tue, Fri,
                                               |Mon, Sun, Tue,
                                               |Wed, Thu, Mon,
                                               |Sun, Wed, Tue |];

                                               [|SUN, TUE, FRI, THU, SUN, TUE, TUE, WED, FRI, TUE], 
                                               [MON, SUN, SUN, TUE, WED, THU, SUN, FRI, SUN, WED], 
                                               [WED, THU, MON, FRI, TUE, MON, WED, THU, THU, SUN]]
% array[People, Choices] of 0..1: matches;

% variables
array[People] of var DAYS: assignment;
% array[People] of var int: score;

% constraints
% constraint score = product (p in People) ((assignment[p] == preferences[p, 1])*3 + (assignment[p] == preferences[p, 2])*2 + (assignment[p] == preferences[p, 3])*1)
include "alldifferent.mzn";
constraint alldifferent(assignment);

% objective
solve maximize product (p in People) ((assignment[p] == preferences[p, 1])*3 + (assignment[p] == preferences[p, 2])*2 + (assignment[p] == preferences[p, 3])*1)

output ["\(p\)     \(assignment[p]\)" | p in People];