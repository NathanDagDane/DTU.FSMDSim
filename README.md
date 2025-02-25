<h2 align="center">Finite State Machine with Datastream Simulation</h2>
<h3 align="center">For DTU Cyber Systems Intro</h3>

## Prerequisites
### VENV:
If you use *Conda*, use the following command:  
```conda create -n fsmd-sim python=3.12.9 xmltodict```

Otherwise, make sure your environment has `python 3.12.9` and `xmltodict` package.

## Usage
### Test 2:
Run the following command in the base folder of the repository:  
```python3 fsmd-sim.py 100 test_2/gcd_desc.xml test_2/gcd_stim.xml```
### Test 3:
Run the following command in the base folder of the repository:  
```python3 fsmd-sim.py 100 test_3/gcd_desc.xml test_3/gcd_stim.xml```
---
In either test, replace `100` with your desired maximum iterations before simulation termination.  
### Output
The simulator will output its current state at the beginning and end of each cycle.  
Each cycle is separated clearly with a line: '------...'