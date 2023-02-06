# ArchPLC

**1. Generate parser (ST & SCL):**
   python iec2peg.py > iec_grammar.py

**2. Generate AST:**
   python iec2xml.py -o ft.xml ft.scl (For FischerTechnik)
   For Chemical plant (https://github.com/Fortiphyd/GRFICSv2/tree/master/workstation_vm):
   python iec2xml.py -o chemical_plant.xml chemical_plant.st

**3. Generate IR (modify the AST file name in the variable input_file) the output IR.txt will be generated:**
   python genIR_iter.py
   For chemical plant:
   python genIR_chemical_plant.py

**4. (ONLY REQUIRED FOR FT) Add the global direct variables (sensors, actuators and configuration variables) to the IR.txt, output file is IR_directVars.txt:**
   python genDirectVars.py

**5. Generate graphs, output file is PLCprog_SDG.dot:**
   python genGraphs.py   
   For chemical plant:
   python genGraphs_chemical_plant.py

**6. Extract physical model:**
   python genModelGraph.py    (output physical model is in output\physicalModel.txt)
   For chemical plant:        (physical model will be printed out on terminal and in output folder under 4 files with the name vars_stmt_*)
   python genModelGraph_chemical_plant.py


![image_2023_02_01T04_34_14_424Z](https://user-images.githubusercontent.com/102813392/215954369-53db5a14-0d9d-403a-bc9c-0c4d042d9ca3.png)

**Please refer following YouTube links for attack videos according to above given table:** </br>
**[Normal Operation]:** https://youtu.be/TLJ9UPOcdjw </br>
**[F-1]:** https://youtu.be/SSySD6sn5e4 </br>
**[F-2]:** https://youtu.be/e-n27kRyAwM </br>
**[F-3]:** https://youtu.be/iHOU-TXWWKA </br>
**[F-4]:** https://youtu.be/47yGipwV-ao </br>
**[F-5]:** https://youtu.be/foB-hyJYkRw </br>
**[F-6]:** https://youtu.be/2Rp5Kiqs7yA </br>
**[F-7]:** https://youtu.be/BHqrOTZr7-w </br> 
**[C-1]:** https://youtu.be/N7UeAjE6V80 </br>
**[C-2]:** https://youtu.be/VpKsNrisTYU </br>
**[C-3]:** https://youtu.be/Y-SHBmU7U5Q </br>

**Complete YouTube playlist is here:** </br>
https://www.youtube.com/watch?v=SSySD6sn5e4&list=PLT1QolCLdp7GoLjwi3HT9gr0cxKc_mTRu&index=1
