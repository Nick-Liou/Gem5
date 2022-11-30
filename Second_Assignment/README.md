# Second Assignment: Design Space Exploration using Gem5

## Step 1

### Default memory configuration on MinorCPU

From config.ini:  
```
response_latency=20
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