# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:26:35 2019

@author: Sanket Pandilwar
"""

#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: Amogh Batwal(abatwal), Anuj Godase(abgodase), Sanket Pandilwar(spandilw)
#
# Based on skeleton code by D. Crandall, September 2019
#
import sys
import time
import queue

def load_people(filename):
    people={}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people[l[0]] = [ float(i) for i in l[1:] ] 
    return people

    


def approx_solve_using_dynamic_programming(people, budget):

    solution=()
    for (person, (skill, cost)) in sorted(people.items(), key=lambda x: x[1][0]/x[1][1]):
        if budget - cost > 0:
            solution += ( ( person, 1), )
            budget -= cost
#    print(people)
    solution=()    

    names=[]
    skills=[]
    rate=[]
    for name in people.keys():
        names.append(name)
    for item in people.values():
        skills.append(int(item[0]))
        rate.append(int(item[1]))

#    print(len(skills),len(rate),len(names))
#    print(skills,rate)
#    print(len(names),rate[5])
    table=[[0 for j in range(int(budget)+1)] for i in range(len(names)+1)]
    for item in range(len(names)+1):
        for b in range(int(budget)+1):
            if (item==0 or b==0) :
                table[item][b] = 0
            elif(b<rate[item-1]):
                table[item][b]=table[item-1][b]
            else:
                table[item][b]= max(skills[item-1]+table[item-1][b-rate[item-1]], table[item-1][b])

    b=int(budget)
    for item in range(len(names)-1,-1,-1):
        print(item)
        if(item==0 and table[item][b]==0):
            break;
        elif (table[item][b] == table[item-1][b]):
            continue;
        else:
            return solution + ( ( person, budget/cost ), )

            print(names[item])
            solution+=((names[item],1),)
            b=b-rate[item]
        print(b)

    print(solution)
    print(table[len(names)][int(budget)])        
    return solution

if __name__ == "__main__":
    start_time=time.time();
    if(len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')
    budget = float(sys.argv[2])
    people = load_people(sys.argv[1])
    solution=approx_solve_using_dynamic_programming(people,budget)
#    print(solution)
    print("Found a group with %d people costing %f with total skill %f" % \
               ( len(solution), sum(people[p][1]*f for p,f in solution), sum(people[p][0]*f for p,f in solution)))
    for s in solution:
        print("%s %d" % s)    
#    print("seconds:", time.time()-start_time)

