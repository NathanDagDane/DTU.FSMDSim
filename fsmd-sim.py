#!/usr/bin/env python3

import sys
import xmltodict

print("Welcome to the FSMD simulator! - Version 1 - Designed by the lads")

if len(sys.argv) < 3:
    print('Too few arguments.')
    sys.exit(-1)
elif (len(sys.argv) >4):
    print('Too many arguments.')
    sys.exit(-1)

# Define variables
iterations = int(sys.argv[1])
cycle = 0

#Parsing the FSMD description file
with open(sys.argv[2]) as fd:
    fsmd_des = xmltodict.parse(fd.read())

#Parsing the stimuli file
fsmd_stim = {}
if len(sys.argv) == 4:
    with open(sys.argv[3]) as fd:
        fsmd_stim = xmltodict.parse(fd.read())

print("\n--FSMD description--")

states = fsmd_des['fsmddescription']['statelist']['state']
print("States:")
for state in states:
    print('  ' + state)

initial_state = fsmd_des['fsmddescription']['initialstate']
print("Initial state:")
print('  ' + initial_state)

try:
    end_state = fsmd_stim['fsmdstimulus']['endstate']
except:
    end_state = fsmd_des['fsmddescription']['statelist']['state'][-1]

# List of input variables
inputs = {}
if(fsmd_des['fsmddescription']['inputlist'] is None):
    inputs = {}
    #No elements
else:
    if type(fsmd_des['fsmddescription']['inputlist']['input']) is str:
        # One element
        inputs[fsmd_des['fsmddescription']['inputlist']['input']] = 0
    else:
        # More elements
        for input_i in fsmd_des['fsmddescription']['inputlist']['input']:
            inputs[input_i] = 0
print("Inputs:")
for input_i in inputs:
    print('  ' + input_i)

# List of variables
variables = {}
if(fsmd_des['fsmddescription']['variablelist'] is None):
    variables = {}
    #No elements
else:
    if type(fsmd_des['fsmddescription']['variablelist']['variable']) is str:
        # One element
        variables[fsmd_des['fsmddescription']['variablelist']['variable']] = 0
    else:
        # More elements
        for variable in fsmd_des['fsmddescription']['variablelist']['variable']:
            variables[variable] = 0
print("Variables:")
for variable in variables:
    print('  ' + variable)

# List of all defined operations
operations = {}
if(fsmd_des['fsmddescription']['operationlist'] is None):
    operations = {}
    #No elements
else:
    for operation in fsmd_des['fsmddescription']['operationlist']['operation']:
        if type(operation) is str:
            # Only one element
            operations[fsmd_des['fsmddescription']['operationlist']['operation']['name']] = \
                fsmd_des['fsmddescription']['operationlist']['operation']['expression']
            break
        else:
            # More than 1 element
            operations[operation['name']] = operation['expression']
print("Operations:")
for operation in operations:
    print('  ' + operation + ' : ' + operations[operation])

# List of all possible conditions
conditions = {}
if(fsmd_des['fsmddescription']['conditionlist'] is None):
    conditions = {}
    #No elements
else:
    for condition in fsmd_des['fsmddescription']['conditionlist']['condition']:
        if type(condition) is str:
            #Only one element
            conditions[fsmd_des['fsmddescription']['conditionlist']['condition']['name']] = fsmd_des['fsmddescription']['conditionlist']['condition']['expression']
            break
        else:
            #More than 1 element
            conditions[condition['name']] = condition['expression']
print("Conditions:")
for condition in conditions:
    print('  ' + condition + ' : ' + conditions[condition])

# List of states and their transitions
fsmd = {}
for state in states:
    fsmd[state] = []
    for transition in fsmd_des['fsmddescription']['fsmd'][state]['transition']:
        if type(transition) is str:
            #Only one element
            fsmd[state].append({'condition': fsmd_des['fsmddescription']['fsmd'][state]['transition']['condition'],
                                'instruction': fsmd_des['fsmddescription']['fsmd'][state]['transition']['instruction'],
                                'nextstate': fsmd_des['fsmddescription']['fsmd'][state]['transition']['nextstate']})
            break
        else:
            #More than 1 element
            fsmd[state].append({'condition' : transition['condition'],
                                'instruction' : transition['instruction'],
                                'nextstate' : transition['nextstate']})
print("FSMD transitions table:")
for state in fsmd:
    print('  ' + state)
    for transition in fsmd[state]:
        print('    ' + 'nextstate: ' + transition['nextstate'] + ', condition: ' + transition['condition'] + ', instruction: ' + transition['instruction'])


# -- Util Functions --
def execute_setinput(operation):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    inputs[target] = eval(expression, {'__builtins__': None}, inputs)
    return

def execute_operation(operation):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    variables[target] = eval(expression, {'__builtins__': None}, merge_dicts(variables, inputs))
    return

def execute_instruction(instruction):
    if instruction == 'NOP' or instruction == 'nop':
        return
    instruction_split = instruction.split(' ')
    for operation in instruction_split:
        execute_operation(operations[operation])
    return

def evaluate_condition(condition):
    if condition == 'True' or condition=='true' or condition == 1:
        return True
    if condition == 'False' or condition=='false' or condition == 0:
        return False
    condition_explicit = condition
    for element in conditions:
        condition_explicit = condition_explicit.replace(element, conditions[element])
    #print('----' + condition_explicit)
    return eval(condition_explicit, {'__builtins__': None}, merge_dicts(variables, inputs))

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result



#######################################
###       Start of simulation       ###

print('\n---Start simulation---')

# -------- Initiate Simulation --------
def init_simulation():
    # Initiate variables
    global cycle, state
    cycle = 0
    state = initial_state
    # Print initial status
    print(f"At the beginning of the simulation the status is:\nVariables:")
    for var in variables:
        print(f"  {var}: {variables[var]}")
    print(f"Initial state: {state}")

# -------- Print Begin and End State of Each Cycle --------
def print_init_cycle():
    print("--------------------------------------------------")
    print(f"Cycle: {cycle}")
    print(f"Current state: {state}")
    print("Inputs:")
    for inp in inputs:
        print(f"  {inp}: {inputs[inp]}")

def print_end_cycle():
    print(f"Next state: {state}")
    print(f"At the end of cycle {cycle} execution, the status is:")
    print("Variables:")
    for var in variables:
        print(f"  {var}: {variables[var]}")

# -------- Perform Cycle --------
def perform_cycle():
    # Initiate variables for cycle
    global cycle, state
    sel_condition = sel_instruction = None
    # Set inputs
    try:
        for input in fsmd_stim['fsmdstimulus']['setinput']:
            if int(input['cycle']) == cycle:
                execute_setinput(input['expression'])
    except:
        # No stimulus
        pass

    print_init_cycle()

    # Loop through transitions checking conditions
    for transition in fsmd[state]:
        if evaluate_condition(transition['condition']):
            # Save details of selected transition
            sel_condition = transition['condition']
            sel_instruction = transition['instruction']
            state = transition['nextstate']
            break

    try:
        # Apply details defined in transition
        print(f"The condition ({sel_condition}) is true.")
        print(f"Executing instruction: {sel_instruction}")
        execute_instruction(sel_instruction)
    except:
        # Failed to perform instruction (transition not found or faulty instruction)
        print("!----!----!----!----!----!----!----!----!----!----")
        print("Incorrect instruction.")
        state = end_state

    print_end_cycle()
    cycle += 1

# -------- Run Simulation --------
def main():
    init_simulation()
    while (state != end_state) & (cycle < iterations):
        perform_cycle()
    # Reached final state. Perform finishing cycle
    perform_cycle()
    # End
    print("--------------------------------------------------")
    print("End-state reached.")
    print("End of simulation. Goodbye!")

main()

###        End of simulation        ###
#######################################