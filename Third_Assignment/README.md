# Third Assignment: Energy-Delay-Area Product Optimization (gem5 + McPAT)

## Step 1: Introduction to McPAT

### 1. Dynamic Power - Leakage Power

In general, leakage power is the power demand of an idle system, while dynamic power is the power demand that fluctuates depending on the load.

In a CPU, dynamic power is caused by logic gates changing state. Leakage power is caused by transistor leakage current and happens even when no change of state is necessary.

Dynamic power depends on the characteristics of the program executed, because certain CPU modules/instructions may consume more power than others. Leakage power is constant.

Since we are talking about power, the execution time of a program doesn't directly affect these two metrics (assuming that the program's resource demands stay constant)

### 2. Assessing energy usage

In this example, we are asked to choose between a 5 Watt and a 50 Watt CPU, in order to maximize working time on a battery of limited capacity.

While the 5 Watt CPU may seem (at first glance) more appropriate, we cannot be 100% sure of that choice. That's beacause it's not specified if these power figures refer to peak, TDP or average power consumption.

One could imagine a scenario where the "5 Watt" CPU always consumes 5 Watts, while the "50 Watt" CPU has a peak consumption of 50 Watts, but over the course of a workload only consumes 3 Watts on average.

(Fun fact: The Intel i5 CPU powering the laptop where this text is written, can go from 2 Watts when idle, to 25 Watts of power consumption, just by running McPAT :D )

The stats given by McPAT can give us a better answer, as we can compare both peak power and "runtime" power (which accounts for the CPU utilization profile). McPAT also supports power management (CPU frequency/voltage reacting to temperature/power) and power saving ("disabling" idle circuit blocks) features used by modern CPUs.

### 3. Xeon vs ARM A9

In this section, we are assessing whether a Xeon can be more efficient than an ARM A9, under the assumption that the Xeon can finish the same workload 50 times faster.

Under that assumption, the Xeon would have to consume more than 50x the power compared to the ARM A9 in order be less efficient. 

Here are statistics from McPAT for the two CPUs:

| Statistic       | Xeon      | ARM A9   |
|:----------------|:---------:|:--------:|
| Peak Power      | 134.938 W | 1.7419 W |
| Total Leakage   | 36.831 W  | 0.1087 W |
| Peak Dynamic    | 98.106 W  | 1.6332 W |
| Runtime Dynamic | 72.919 W  | 2.9605 W |

According to these statistics, the Xeon could in theory be more efficient, as the Runtime Dynamic power consumption is only 24.6x higher than the ARM. However, we also observe that the Total Leakage is more than 300x higher.

Thus, if the workload consumes only a small proportion of the Peak Dynamic power, the Xeon can end up having more than 50x average power demand.

Let's express this with an equation, assuming average power consumption is given as follows:

$$
P_{avg} = P_L + kP_{D}
$$

Where $P_L$ is the leakage power, $P_D$ is the peak dynamic power, and $k\in[0,1]$ expresses the amount of dynamic load relative to peak.

We observe that, if $k$ is small enough, $P_{avg}$ will mostly depend on $P_L$



## Step 2: gem5 + McPAT: Optimizing the Energy-Delay Product (EDP)

### 1. Energy consumption

### 2. 

### 3. 