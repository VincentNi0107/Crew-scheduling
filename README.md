# Crew Scheduling Problem with Column generation

Course project of SJTU BUSS3528.  
You need to install following packages in order to run the code:  
- [Numpy](https://numpy.org/)  
- [Gurobi](https://www.gurobi.com/)

**To get the basic results:**
```bash
python crew_schdule.py
```
**To add constrains on the work time of each crew:**
```bash
python crew_schdule.py -ub <max_worktime>
```
The parameter <max_worktime> should be no less than 11.
## Task Description

Consider the aircrew scheduling problem discussed in class. There are 8 flights serving 4 places. The following graph shows the flight schedule. Each node represents an airport, and each edge represents a flight and is labeled with the departure and arrival times. A series of flights could be serviced by a crew. In one series of flights, the departure time of a flight must be no earlier than the arrival time of the previous flight. For example, a series of flights 3 − 5 − 2 is impossible because flight 2′ departure time is earlier than the last flight 5′ arrival time.

Our task is to assign aircrews to different series of flights to cover the 8 flights and 4 places. We assume that each crew must serve at least two flights for efficiency. That is to say, any series of flights should contain no less than two flights. We can assign multiple crews to one flight if necessary to transport a crew to another airport. The pairing cost is expressed as the time interval between the first departure and last arrival, adding 5 hours. For example, the time cost of a series of flights 7 − 3 − 5 is 21 − 14 + 5 = 12 hours. Our objective is to minimize the total time cost. Please model and solve this problem.


![problem_define](./imgs/problem_define.png)
## Problem Definition
### Master problem
Note that dual variables of the master problem are not available in an integer programming problem.
You need to solve the dual problem to calculate reduced costs.
![main](./imgs/main.png)

### Subproblem
It's a shortest path problem that aims at finding a 
feasible pairing with the least reduced cost. It is defined 
over an acyclic time-space network.

![longestpath](./imgs/longestpath.png)
![sub](./imgs/sub.png)

To balance the workload of every crew, we can also add maximum working time in the subproblem:  

$$
C \leq maxtime
$$  

Since the minimum cost of a pairing including flight 1 is 11 hours, maxtime should be no less than 11.

## Results
For the basic problem:
```bash
>python crew_schdule.py
Set parameter Username
Academic license - for non-commercial use only - expires 2022-02-08
Total Cost: 37
The Combination of Following Pairings is Optimal:
pairing 8: flight7 flight8 ,costing 10 hours
pairing 10: flight1 flight2 flight4 ,costing 15 hours
pairing 11: flight3 flight5 flight7 ,costing 12 hours
```
Set the maximum work time to 12 hours:
```bash
>python crew_schdule.py -ub 12
Set parameter Username
Academic license - for non-commercial use only - expires 2022-02-08
maximum work time for a crew: 12
total cost: 41
The Combination of Following Pairings is Optimal
pairing 1: flight1 flight2 ,costing 11 hours
pairing 2: flight4 flight7 ,costing 10 hours
pairing 6: flight3 flight5 ,costing 10 hours
pairing 8: flight7 flight8 ,costing 10 hours
```
