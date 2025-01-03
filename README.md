# **Critical Path Analysis Tool**

This project analyzes the critical path of a digital circuit described in a text file. It calculates the longest path (in terms of delay) through the circuit and outputs the result.

---

## **Installation Instructions**

### Clone the Repository
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

2. #Set Up Environment
(Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. #Install required Python packages:

   ```bash
   pip install -r requirements.txt

   
4. #Usage Instructions
#Run the Tool
To analyze a circuit file, use:

      ```bash
      python main.py circuit1.txt

Replace circuit1.txt with the name of the circuit file you'd like to analyze.

#Example:

Input file: circuit1.txt

      INPUT in1
      INPUT in2
      ADD add1 in1 in2
      MUL mul1 in1 add1
      REG reg1 mul1
      ADD add2 reg1 in2
      OUTPUT out1 add2


Command:
      ```bash
      
      python main.py circuit1.txt
      Output:
      less
      Copy code
      Parsed Graph:
      Nodes: ['in1', 'in2', 'add1', 'mul1', 'reg1', 'add2', 'out1']
      Edges: [('in1', 'add1'), ('in2', 'add1'), ('add1', 'mul1'), ...]
      
      Critical Path: ['in1', 'add1', 'mul1', 'reg1', 'add2', 'out1']
      Total Delay: 1.6




##Run Unit Tests
To validate the implementation, run the unit tests:
      ```bash
      
      python -m unittest test_critical_path_analysis.py
      Example Inputs and Outputs
      Input File (circuit1.txt)
      arduino
      Copy code
      INPUT in1
      INPUT in2
      ADD add1 in1 in2
      MUL mul1 in1 add1
      REG reg1 mul1
      ADD add2 reg1 in2
      OUTPUT out1 add2
      Output
      less
      Copy code
      Parsed Graph:
      Nodes: ['in1', 'in2', 'add1', 'mul1', 'reg1', 'add2', 'out1']
      Edges: [('in1', 'add1'), ('in2', 'add1'), ('add1', 'mul1'), ...]
      
      Critical Path: ['in1', 'add1', 'mul1', 'reg1', 'add2', 'out1']
      Total Delay: 1.6


##File Structure
      ```bash
      
      .
      ├── main.py                      # Core functionality
      ├── test_critical_path_analysis.py  # Unit tests
      ├── circuit1.txt                 # Example circuit file
      ├── circuit2.txt                 # Example circuit file
      ├── circuit3.txt                 # Example circuit file
      ├── README.md                    # Documentation
      ├── requirements.txt             # Python dependencies


      
Design Decisions and Assumptions
Graph Representation:

Used a directed graph to model the circuit, where nodes represent components (e.g., ADD, MUL, REG) and edges represent data dependencies.
Delay Calculation:

Each component type has a fixed delay:
INPUT, OUTPUT: 0.0
ADD, MUL: 0.5
REG: 0.1
Unknown types default to 1.0.
Parsing Assumption:

Circuit files follow a structured format:
      ```
      
      COMPONENT_NAME COMPONENT_ID INPUT1 INPUT2
      
Components with one input (e.g., REG, OUTPUT) use only the first input.
Critical Path:

Assumes the critical path is the longest path (in terms of delay) through the directed graph.
Example Circuit Files
circuit1.txt: A basic sequential circuit with simple arithmetic operations.
circuit2.txt: Includes registers to demonstrate delays in sequential circuits.
circuit3.txt: A complex circuit with multiple paths and components.
License
This project is licensed under the MIT License. See the LICENSE file for details.

      `abdullahdevorbit` and `DSD-Assignment-3`