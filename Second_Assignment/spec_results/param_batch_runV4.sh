#!/bin/bash

# insert name-argument pairs:
ARG_ARRAY=(

# "cl_256/L1d_128kB" 	"--l1d_size 128kB --cacheline_size 256" 
# "cl_256/L1d_32kB"  	"--l1d_size 32kB --cacheline_size 256"

# "cl_256/L1i_64kB"     	"--l1i_size 64kB --cacheline_size 256" 
# "cl_256/L1i_16kB" 	"--l1i_size 16kB --cacheline_size 256"

"cl_256/L2_4MB"     	"--l2_size 4MB --cacheline_size 256" 
"cl_256/L2_1MB" 	"--l2_size 1MB --cacheline_size 256"

"cl_256/L1d_assoc_4"	"--l1d_assoc 4 --cacheline_size 256" 
"cl_256/L1d_assoc_1"	"--l1d_assoc 1 --cacheline_size 256"

"cl_256/L1i_assoc_4"	"--l1i_assoc 4 --cacheline_size 256" 
"cl_256/L1i_assoc_1"	"--l1i_assoc 1 --cacheline_size 256" 

"cl_256/L2_assoc_4"	"--l2_assoc 4 --cacheline_size 256" 
"cl_256/L2_assoc_16"	"--l2_assoc 16 --cacheline_size 256"



)

arraylength=${#ARG_ARRAY[@]}
echo $((arraylength/2))

for (( i=0; i<$arraylength; i+=2 ));
do
  config_name=${ARG_ARRAY[$i]}
  config_params=${ARG_ARRAY[$((i+1))]}

  echo "____ Running config '$config_name' with params: $config_params _____"


	./build/ARM/gem5.opt -d spec_results/specbzip/$config_name configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/401.bzip2/src/specbzip -o "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000 $config_params &

	./build/ARM/gem5.opt -d spec_results/specmcf/$config_name configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000 $config_params &

	./build/ARM/gem5.opt -d spec_results/spechmmer/$config_name configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000 $config_params &


	./build/ARM/gem5.opt -d spec_results/specsjeng/$config_name configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000 $config_params &

	./build/ARM/gem5.opt -d spec_results/speclibm/$config_name configs/example/se.py --cpu-type=MinorCPU --caches --l2cache -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000 $config_params &

	wait #remove this to run every config in parallel :P

done


