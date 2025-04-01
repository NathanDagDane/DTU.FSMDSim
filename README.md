<div align="center">
  <h2>Finite State Machine with Datastream Simulation</h2>
  <a href="">
    <img src="https://github.com/user-attachments/assets/e21f2d45-6775-48d8-bf8b-9b1cb99d22e5" alt="Logo" height="80">
  </a>
  <h3>For DTU Cyber Systems Intro</h3>
</div>

## Prerequisites
### VENV:
If you use *Conda*, use the following command:  
```conda create -n fsmd-sim python=3.12.9 xmltodict```

Otherwise, make sure your environment has `python 3.12.9` and `xmltodict` package.

## Usage
### Test 1 - Simple counter:
Run the following command in the base folder of the repository:  
```python3 fsmd-sim.py 100 test_1/test_desc.xml;```  

### Test 2 - Euclidian algorithm:
Run the following command in the base folder of the repository:  
```python3 fsmd-sim.py 100 test_2/gcd_desc.xml test_2/gcd_stim.xml```  
The final `var_A` and `var_B` variables will show the greatest common denominator.  
Input numbers can be configured on line 5 and 10 in _/test_2/gcd_stim.xml_.  

### Test 3 - Largest prime factor algorithm:
Run the following command in the base folder of the repository:  
```python3 fsmd-sim.py 100 test_3/fact_desc.xml test_3/fact_stim.xml```  
The final `prime` variable will show the greatest prime factor.  
Input number can be configured on line 5 in _/test_3/fact_stim.xml_.  

---
In any test, replace `100` with your desired maximum iterations before simulation termination.  
### Output
The simulator will output its current state at the beginning and end of each cycle.  
Each cycle is separated clearly with a line: '------...'
