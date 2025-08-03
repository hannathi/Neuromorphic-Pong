#brian2_test.py
from brian2 import *

prefs.codegen.target = "numpy"

start_scope()

tau = 10*ms
v_rest = -70*mV
v_threshold = -50*mV
v_reset = -70*mV

eqs = '''
dv/dt = (v_rest - v)/tau : volt
'''

neurons = NeuronGroup(1, eqs, threshold='v>v_threshold', reset='v=v_reset', method='exact')
neurons.v = v_rest

neurons.v[0] = -40*mV

mon = StateMonitor(neurons, 'v', record=True)

run(50*ms)

print("Neuron voltages during simulation:")
print(mon.v[0])
