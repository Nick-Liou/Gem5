# First Assignment: Introduction to the gem5 Simulator

## Task 1: Basic gem5 parameters specified in starter_se.py

Parameters that can be set from the command line:

- CPU type (atomic, minor, HPI): atomic
- Number of CPU cores: 1
- CPU frequency: 1GHz	
- Memory type: DDR3_1600_8x8
- Number of memory channels: 2
- Number of memory ranks per channel: None
- Memory size: 2GB
- Memory mode: timing

Other parameters:

- Cache line size: 64 bytes
- Voltage domain: 3.3V
- CPU voltage: 1.2V
- Clock domain 	(syscall emulation): 1GHz
- Memory bus
- Cache hierarchy (L1, L2 etc.)

Many other parameters (such as cache sizes, latencies, associativity) are specified in different python files (eg. devices.py)

## Task 2: Simulation output files
 We ran the simulation using the following command:
 ```
 ./build/ARM/gem5.opt -d hello_result configs/example/arm/starter_se.py --cpu="minor" "tests/test-progs/hello/bin/arm/linux/hello"
 ```

In config.ini (or config.json, they are equivalent) one can find details about the configuration of the simulated system.  
The simulation results are located in stats.txt.

### a. Locate variables from question 1 in the output files

config.ini
```
cache_line_size=64

mem_ranges=0:2147483647

[system.cpu_cluster.cpus]
type=MinorCPU

[system.clk_domain]
type=SrcClockDomain
clock=1000

numThreads=1
p_state_clk_gate_max=1000000000000

[system.cpu_cluster.clk_domain]
type=SrcClockDomain
clock=1000

[system.cpu_cluster.voltage_domain]
type=VoltageDomain
eventq_index=0
voltage=1.2

[system.voltage_domain]
type=VoltageDomain
eventq_index=0
voltage=3.3

type=MinorCPU
```

stats.txt
```
system.voltage_domain.voltage                3.300000
system.cpu_cluster.voltage_domain.voltage     1.200000

simFreq                                  1000000000000 (10^12 Tick/Sec = 1THz)
system.clk_domain.clock                          1000 ticks	(simulation period syscall emulation)
system.cpu_cluster.clk_domain.clock            1000 ticks	(CPU cycle period)

```



### b. Describe the meaning of the following stats: sim_seconds, sim_insts, host_inst_rate

- sim_seconds: Seconds simulated from the simulated CPU perspective.
  ```
  sim_seconds        0.000035        # Number of seconds simulated
  ```


- sim_insts: Number of instructions run on the simulated CPU:
  ```
  sim_insts          5027            # Number of instructions simulated
  ```


- host_inst_rate: Real time number of instructions per second simulated:
  ```
  host_inst_rate     151942          # Simulator instruction rate (inst/s)
  ```


### c. What is the total number of “committed” commands? Why is it different from the statistic presented in gem5’s results?

```
sim_insts                                    	5027                   	# Number of instructions simulated
sim_ops                                      	5831                   	# Number of ops (including micro ops) simulated

system.cpu_cluster.cpus.committedInsts       	5027                   	# Number of instructions committed
system.cpu_cluster.cpus.committedOps         	5831                   	# Number of ops (including micro ops) committed


system.cpu_cluster.cpus.discardedOps          1300                    # Number of ops (including micro ops) which were discarded before commit

```
- Instructions vs ops  
  Some instructions are too complicated to execute in a single operation. At the start of the CPU pipeline (at the fetching or decoding stage), complex instructions can be broken down into multiple simpler ones, which are called "micro ops" . This is more common in x86 and CISC architectures.

- Issued vs committed:  
  The simulated CPU features branch prediction, which is a common technique to avoid stalling the CPU when waiting for a branch result. The CPU will guess the result of the branch, and start executing instructions, but will not "commit" them until its prediction is confirmed. If the CPU predicted incorrectly, the instructions executed can be "aborted" (by never being committed).
  

### d. How many times was the L2 cache accessed? How could you calculate the accesses if they were not directly provided in the simulation results?
Below are the stats relevant to L2 access:
```
system.cpu_cluster.l2.tags.data_accesses     	7804                   	# Number of data accesses
system.cpu_cluster.l2.demand_accesses::total      	474                   	# number of demand (read+write) accesses
```

In theory, we can calculate L2 accesses by adding up all L1 cache misses:
```
system.cpu_cluster.cpus.dcache.overall_misses::total      	177                   	# number of overall misses
system.cpu_cluster.cpus.icache.overall_misses::total      	327                   	# number of overall misses
```

As an interesting sidenote, we observe that the number of L1 icache misses is equal to L2 instruction misses:
```
system.cpu_cluster.l2.overall_misses::.cpu_cluster.cpus.inst      	327                   	# number of overall misses
system.cpu_cluster.l2.overall_misses::.cpu_cluster.cpus.data      	147                   	# number of overall misses
system.cpu_cluster.l2.overall_misses::total      	474                   	# number of overall misses
```

## Task 3: Different CPU models in gem5

SimpleCPU  
Suited for cases where detailed execution is not necessary. They don’t model a pipelined execution. AtomicSimpleCPU uses “atomic” memory accesses, which only estimates latencies and cache access times. TimingSimpleCPU uses “timing” memory accesses, which is a more realistic simulation of cache behavior. 

Minor CPU  
Detailed in-order execution model with 4-stage pipeline (Fetch1, Fetch2, Decode, Execute). The first 2 stages fetch and decompose instructions into micro-ops if needed. Supports branch prediction, meaning that instructions can be issued but not committed. Has a Load/Store Queue for storing multiple outstanding memory transactions.

The gem5 simulator also provides a modern out-of-order CPU model (O3CPU), with high-accuracy timings and tracing/visualization capabilities.


### a. Executing a C program in gem5 using different CPU models (TimingSimpleCPU and MinorCPU)

Below are results regarding the simulation time for the two CPU models:


TimingSimpleCPU 
```
final_tick                              	651861000                   	# Number of ticks from beginning of simulation (restored from checkpoints and never reset)
host_inst_rate                            	1516274                   	# Simulator instruction rate (inst/s)
host_mem_usage                             	674144                   	# Number of bytes of host memory used
host_op_rate                              	2012128                   	# Simulator op (including micro ops) rate (op/s)
host_seconds                                 	0.28                   	# Real time elapsed on the host
host_tick_rate                         	2355957939                   	# Simulator tick rate (ticks/s)
sim_freq                             	1000000000000                   	# Frequency of simulated ticks
sim_insts                                  	419272                   	# Number of instructions simulated
sim_ops                                    	556687                   	# Number of ops (including micro ops) simulated
sim_seconds                              	0.000652                   	# Number of seconds simulated
sim_ticks                               	651861000                   	# Number of ticks simulated

```


MinorCPU
```
final_tick                              	309449000                   	# Number of ticks from beginning of simulation (restored from checkpoints and never reset)
host_inst_rate                             	405647                   	# Simulator instruction rate (inst/s)
host_mem_usage                             	678752                   	# Number of bytes of host memory used
host_op_rate                               	538688                   	# Simulator op (including micro ops) rate (op/s)
host_seconds                                 	1.03                   	# Real time elapsed on the host
host_tick_rate                          	299218668                   	# Simulator tick rate (ticks/s)
sim_freq                             	1000000000000                   	# Frequency of simulated ticks
sim_insts                                  	419481                   	# Number of instructions simulated
sim_ops                                    	557100                   	# Number of ops (including micro ops) simulated
sim_seconds                              	0.000309                   	# Number of seconds simulated
sim_ticks                               	309449000                   	# Number of ticks simulated
```

### b. Differences and similarities in the two models’ results.

- **The differences:**  
  MinorCPU is a more detailed and realistic CPU model, simulating a pipeline and branch prediction. SimpleCPU doesn’t simulate those, so it’s not as realistic, but as a result it’s much simpler and faster to simulate.  

  Compared to MinorCPU, the simulation using SimpleCPU model was a lot faster (host_seconds), as the host system was able to simulate more instructions per second (host_inst_rate).

  On the other hand, we can see that MinorCPU had to simulate less than half the CPU cycles until the program's completion (system.cpu.numCycles). We also observe the following:  
  ```
  SimpleCPU: CPI = system.cpu.numCycles  /  sim_insts = 1303722 / 419272 = 3.10948  
  MinorCPU: CPI = system.cpu.cpi = 1.475390 
  ```

   MinorCPU has a way better (smaller) CPI compared to SimpleCPU. That’s because MinorCpu has a 4-stage pipeline, which means that, as long as the pipeline remains relatively full (and we don’t have many stalls, hazards and branch mispredictions), we can get a CPI close to 1.  

   Finally, MinorCPU seems to have more memory accesses, but with a significantly higher bandwidth.  

- **The similarities:**  
  We ran the same program, so the amount of instructions and ops is practically the same.

### c. Change CPU parameters (eg. memory frequency/technology) and explain the results for the two different CPU models.

We compared two different RAM technologies, DDR3_1600_8x8 and DDR4_2400_8x8, for MinorCPU and TimingSimpleCPU.

We know that the advantages of DDR4 are:  
- Lower voltage → lower power demand
- Higher supported clock frequency → higher (peak) bandwidth
- More banks (16 versus 8 in DDR3)
- Different data prefetching scheme (“8N with bank groups”)

Thus, we paid attention to fields regarding memory bandwidth, memory latency, and memory power consumption. For example:
```
system.mem_ctrls.avgRdBW (Average DRAM read bandwidth in MiByte/s)
system.mem_ctrls.peakBW (Theoretical peak bandwidth in MiByte/s)
system.mem_ctrls.avgMemAccLat (Average memory access latency per DRAM burst)
system.mem_ctrls.rank0.averagePower (Core power per rank (mW))
```

For DDR4 we observed:  
- Decreased average power (system.mem_ctrls.rank0.averagePower)
- Increased maximum theoretical bandwidth (system.mem_ctrls.peakBW)
- More memory banks

However, most of the expected benefits of DDR4 + higher memory frequency were not observed in the results. We assume that is because our test program was not memory intensive.  
It also becomes obvious that a larger sample/variety of simulation results would be needed to fairly compare different technologies and architecture choices.

