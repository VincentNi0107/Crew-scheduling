from gurobipy import *
import numpy as np

flightTime=[4,2,2,2,2,2,2,2]#time for the eight flights
initialPairings=np.identity(8)

rmp=Model()#main problem
sub=Model()#sub problem
dual=Model()#dual of main problem
#ignore output
rmp.setParam("OutputFlag",0)
sub.setParam("OutputFlag",0)
dual.setParam("OutputFlag",0)


#setup main problem and check
y = rmp.addMVar(8, name = 'p_init',lb=0,ub=1,vtype=GRB.INTEGER)
cost=np.array(flightTime)+5    
rmp.setObjective(cost@y, GRB.MINIMIZE)
rmpConstr=rmp.addConstr(initialPairings@y >= np.ones((8)), name='c')
rmp.optimize()

print("--------------initial----------------------")
print("initial cost:",rmp.objVal)
print("initial pairing", rmp.x)

#setup dual problem to obtain dual variables
pai = dual.addMVar(8, name = 'pi',lb=0,vtype=GRB.CONTINUOUS)
dual.setObjective(np.ones((8))@pai,GRB.MAXIMIZE)
dualConstr=dual.addConstr(initialPairings@pai<=cost)
dual.optimize()

print("--------------dual----------------------")
print("dual obj:",dual.objVal)
print("pi:",dual.x)

#check the ppt of column generation for the meanings of xi, xsi and xti 
xs=[]
x=[]
xt=[]
for i in range(1,9):
    xs.append(sub.addVar(obj=0,name = 'xs'+str(i),lb=0,ub=1,vtype=GRB.INTEGER))
    xt.append(sub.addVar(obj=0,name = 'xt'+str(i),lb=0,ub=1,vtype=GRB.INTEGER))
    x.append(sub.addVar(obj=-dual.x[i-1],name = 'x'+str(i),lb=0,ub=1,vtype=GRB.INTEGER))

for i in range(9,13):
    x.append(sub.addVar(obj=0,name = 'x'+str(i),lb=0,ub=1,vtype=GRB.INTEGER))

sub.setAttr(GRB.Attr.ModelSense, 1)

#cost of the pairing
c=sub.addVar(obj=1.0,name='C')
sub.addConstr(4*x[0]+2*x[1]+2*x[2]+2*x[3]+2*x[4]+2*x[5]+2*x[6]+2*x[7]+5==c,'c0')

#constrains for the longest path problem
sub.addConstr( xs[0]+xs[1]+xs[2]+xs[3]+xs[4]+xs[5]+xs[6]+xs[7] ==1, 'c1')
sub.addConstr( xt[0]+xt[1]+xt[2]+xt[3]+xt[4]+xt[5]+xt[6]+xt[7] ==1, 'c2')
sub.addConstr( x[0]+x[1]+x[2]+x[3]+x[4]+x[5]+x[6]+x[7] >=2, 'c3')

sub.addConstr( xs[0]==x[0], 'c4')#start of 1
sub.addConstr( xs[1]+x[0]==x[1]+x[8]+xt[0], 'c5')#start of 2/terminal of 1
sub.addConstr( x[1]==x[9]+xt[1], 'c6')#end of 2
sub.addConstr( xs[2]+x[6]+x[10]==x[2]+x[10]+xt[6], 'c7')#start of 3/end of 7
sub.addConstr( x[2]+x[7]==x[11]+xt[2]+xt[7], 'c8')#end of 3/end of 8
sub.addConstr( xs[3]+x[10]==x[3], 'c9')#start of 4
sub.addConstr( x[3]==xt[3], 'c9')#end of 4
sub.addConstr( xs[4]+xs[5]+x[11]==x[4]+x[5], 'c10')#start of 5/start of 6
sub.addConstr( x[4]==xt[4], 'c11')#end of 5
sub.addConstr( x[5]==xt[5], 'c11')#end of 6
sub.addConstr( xs[6]+x[8]==x[6], 'c12')#start of 7
sub.addConstr( xs[7]==x[7], 'c12')#start of 8

sub.optimize()

print("--------------initial longest path----------------------")
print(sub.objVal)
for v in sub.getVars():
    print('%s: %s' % (v.varName, v.x))


while sub.objVal<0:
    #update the dual problem and solve
    dual.addConstr(x[0].x*pai[0]+x[1].x*pai[1]+x[2].x*pai[2]+x[3].x*pai[3]+x[4].x*pai[4]+x[5].x*pai[5]+x[6].x*pai[6]+x[7].x*pai[7]<=c.x)
    dual.optimize()
    #update the main problem for final results
    newpairing=[]
    pairingname='p'
    for i in range(8):
        newpairing.append(x[i].x)
        pairingname=pairingname+'-'+str(int(x[i].x))#name the new variable shows what is the pairing

    print("--------------newpairing----------------------")
    print(newpairing)

    #update subproblem and solve
    column=Column(newpairing, rmp.getConstrs())
    rmp.addVar(obj=c.x,lb=0,ub=1,vtype=GRB.INTEGER, name=pairingname, column=column)
    for i in range(8):
        x[i].obj=-dual.x[i]
    sub.optimize()
    
#get the final results
rmp.optimize()
print("--------------result----------------------")
print("total cost:",rmp.objVal)
for v in rmp.getVars():
    if v.X != 0.0:
        print('%s %g' % (v.VarName, v.X))










