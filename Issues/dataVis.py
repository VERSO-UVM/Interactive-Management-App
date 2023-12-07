# data vis work

from pyflowchart import *
st = StartNode('Flowchart')
op = OperationNode('Setbacks')
cond = ConditionNode('Weight factor')
io = InputOutputNode(InputOutputNode.OUTPUT, 'Solution')
sub = SubroutineNode('SubGoal')
e = EndNode('FLOWCHART')

st.connect(op)
op.connect(cond)
cond.connect_yes(io)
cond.connect_no(sub)
sub.connect(op, "right")  # sub->op line starts from the right of sub
io.connect(e)
 
fc = Flowchart(st)
print(fc.flowchart())

# Using schemedraw
import matplotlib
import schemdraw
import schemdraw.elements as elm
from schemdraw import flow

with schemdraw.Drawing() as d:
    d.config(fontsize=11)
    d += (b := flow.Start().label('START'))
    d += flow.Arrow().down(d.unit/2)
    d += (d1 := flow.Decision(w=5, h=3.9, E='5', S='23').label('Goal 1'))
    d += flow.Arrow().length(d.unit/2)
    d += (d2 := flow.Decision(w=5, h=3.9, E='90', S='78').label('Goal 2'))
    d += flow.Arrow().length(d.unit/2)
    d += (d3 := flow.Decision(w=5.2, h=3.9, E='4', S='5').label('Goal 3'))

    d += flow.Arrow().right(d.unit/2).at(d3.E)
    d += flow.Box(w=2, h=1.25).anchor('W').label('Setback')
    d += flow.Arrow().down(d.unit/2).at(d3.S)
    d += (listen := flow.Box(w=2, h=1).label('Setback'))
    d += flow.Arrow().right(d.unit/2).at(listen.E)
    d += (hate := flow.Box(w=2, h=1.25).anchor('W').label('Solution'))

    d += flow.Arrow().right(d.unit*3.5).at(d1.E)
    d += (good := flow.Box(w=2, h=1).anchor('W').label('Setback'))
    d += flow.Arrow().right(d.unit*1.5).at(d2.E)
    d += (d4 := flow.Decision(w=5.3, h=4.0, E='6', S='4').anchor('W').label('Setback'))

    d += flow.Wire('-|', arrow='->').at(d4.E).to(good.S)
    d += flow.Arrow().down(d.unit/2).at(d4.S)
    d += (d5 := flow.Decision(w=5, h=3.6, E='8', S='7').label('Setback'))
    d += flow.Arrow().right().at(d5.E)
    d += (question := flow.Box(w=3.5, h=1.75).anchor('W').label("Solution"))
    d += flow.Wire('n', k=-1, arrow='->').at(d5.S).to(question.S)
    d += flow.Line().at(good.E).tox(question.S)
    d += flow.Arrow().down()
    d += (drink := flow.Box(w=2.5, h=1.5).label("Factors"))
    d += flow.Arrow().right().at(drink.E).label('44')
    d += flow.Box(w=3.7, h=2).anchor('W').label('Final')
    d += flow.Arrow().up(d.unit*.75).at(question.N)
    d += (screw := flow.Box(w=2.5, h=1).anchor('S').label('Setback'))
    d += flow.Arrow().at(screw.N).toy(drink.S)