# Third Assignment: Energy-Delay-Area Product Optimization (gem5 + McPAT)

## Step 1: Introduction to McPAT

### 1. Dynamic Power - Leakage Power

In general, leakage power is the power demand of an idle system, while dynamic power is the power demand that fluctuates depending on the load.

In a CPU, dynamic power is caused by logic gates changing state, while leakage power is caused by transistor leakage current and happens even when no change of state is necessary.

Dynamic power depends on the characteristics of the program executed. Certain CPU modules/instructions may consume more power than others. Leakage current is constant.

Since we are talking about power, the execution time of a program doesn't directly affect these two metrics (assuming that the program's resource demands stay constant)

### 2. Assessing energy usage

In this example, we are asked to choose between a 5 Watt and a 50 Watt CPU, in order to maximize working time on a battery of limited capacity.

While the 5 Watt CPU may seem, at first glance, more appropriate, we cannot be 100% sure of that choice, beacause it's not specified if these power figures refer to peak, TDP or average power consumption.

One could imagine a scenario where the "5 Watt" CPU always consumes 5 Watts, while the "50 Watt" CPU has a peak consumption of 50 Watts, but over the course of a workload only consumes 3 Watts.

(Fun fact: The Intel i5 CPU powering the laptop where this text is written, can go from 2 Watts when idle, to 25 Watts of power consumption, just by running McPAT :D )

The stats given by McPAT can give us a better answer, as we can compare both peak power and "runtime" power (which accounts for the CPU utilization profile). McPAT also supports power management (CPU frequency/voltage reacting to temperature/power) and power saving ("disabling" idle circuit blocks) features used by modern CPUs.


### 3. 

## Step 2: gem5 + McPAT: Optimizing the Energy-Delay Product (EDP)

### 1. Energy consumption

### 2. 

### 3. 