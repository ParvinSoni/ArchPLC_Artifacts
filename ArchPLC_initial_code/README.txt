1- Generate parser (ST & SCL):
python iec2peg.py > iec_grammar.py

2- Generate AST:
python iec2xml.py -o ft.xml ft.scl (For FischerTechnik)
for Chemical plant (https://github.com/Fortiphyd/GRFICSv2/tree/master/workstation_vm):
python iec2xml.py -o chemical_plant.xml chemical_plant.st

3- Generate IR (modify the AST file name in the variable input_file) the output IR.txt will be generated:
python genIR_iter.py
For chemical plant:
python genIR_chemical_plant.py

4- (ONLY REQUIRED FOR FT) Add the global direct variables (sensors, actuators and configuration variables) to the IR.txt, output file is IR_directVars.txt:
python genDirectVars.py

5- Generate graphs, output file is PLCprog_SDG.dot:
python genGraphs.py   
For chemical plant:
python genGraphs_chemical_plant.py

6- Extract physical model:
python genModelGraph.py    (output physical model is in output\physicalModel.txt)
For chemical plant:        (physical model will be printed out on terminal and in output folder under 4 files with the name vars_stmt_*)
python genModelGraph_chemical_plant.py