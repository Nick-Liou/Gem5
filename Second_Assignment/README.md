# Second Assignment: Design Space Exploration using Gem5

## Step 1

### 1. Default memory configuration on MinorCPU

From config.ini:  
```
[system.cpu.dcache]
assoc=2
size=65536

[system.cpu.dcache.tags]
block_size=64

[system.cpu.icache]
assoc=2
size=32768

[system.cpu.icache.tags]
block_size=64

[system.l2]
assoc=8
size=2097152
```

### 2. Plots of fundemental measurements
![sim_seconds](spec_results/plots/sim_seconds.png)
![cpi](spec_results/plots/cpi.png)
![d-cache_miss_rate](spec_results/plots/d-cache_miss_rate.png)
![i-cache_miss_rate](spec_results/plots/i-cache_miss_rate.png)


From the above graphs, it is apparent that high d-cache miss rate is stongly correlated to high CPI rate.

### 3. Changing the CPU clock
```
sim_freq                                 1000000000000                       # Frequency of simulated ticks

system.clk_domain.clock                          1000                       # Clock period in ticks

system.cpu_clk_domain.clock                       500                       # Clock period in ticks

```

When we change the frequency of the simulated CPU, system.cpu_clk_domain.clock changes proportionally, while system.clk_domain.clock remains constant.

Also, we notice the following entries in config.ini:
```
[system.cpu.dcache]
clk_domain=system.cpu_clk_domain

[system.l2]
clk_domain=system.cpu_clk_domain

[system.membus]
clk_domain=system.clk_domain
```

We can conclude that different things in the system run on different clocks. CPU and CPU caches have the same clock, while a different clock is used for RAM).

