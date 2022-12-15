import pandas as pd
from pathlib import Path
import re

def parse_txts(txt_file: str):
    
    return_dict = {}

    with open(txt_file, "r") as f:
        text = f.read()

    # Match the whole "Processor: " block
    match = re.search("^Processor:\s*((\n.*){8})", text, flags=re.MULTILINE)
    block = match.group(1)

    # extract fields that we want
    match = re.search("Peak Power = (\d+\.?\d*) W", block)
    if match:
        return_dict["processor_peak_power"] = match.group(1)


    # Match the whole "Core:" block
    match = re.search("^Core:\s*((\n.*){6})", text, flags=re.MULTILINE)
    block = match.group(1)

        # extract fields that we want
    match = re.search("Area = (\d+\.?\d*) mm\^2", block)
    if match:
        return_dict["core_area"] = match.group(1)

    match = re.search("Subthreshold Leakage = (\d+\.?\d*) W", block)
    if match:
        return_dict["core_subthreshold_leakage"] = match.group(1)

    match = re.search("Gate Leakage = (\d+\.?\d*) W", block)
    if match:
        return_dict["core_gate_leakage"] = match.group(1)

    match = re.search("Runtime Dynamic = (\d+\.?\d*) W", block)
    if match:
        return_dict["core_runtime_dynamic"] = match.group(1)


    # Match the whole "L3" block
    match = re.search("^L2\s*((\n.*){6})", text, flags=re.MULTILINE)
    block = match.group(1)

    match = re.search("Area = (\d+\.?\d*) mm\^2",block)
    if match:
        return_dict["L2_area"] = match.group(1)

    match = re.search("Subthreshold Leakage = (\d+\.?\d*) W", block)
    if match:
        return_dict["L2_subthreshold_leakage"] = match.group(1)

    match = re.search("Gate Leakage = (\d+\.?\d*) W", block)
    if match:
        return_dict["L2_gate_leakage"] = match.group(1)

    match = re.search("Runtime Dynamic = (\d+\.?\d*) W", block)
    if match:
        return_dict["L2_runtime_dynamic"] = match.group(1)

    return return_dict




results_path = "./results_mcpat"

benchmarks = ["speclibm",
"specmcf",
"spechmmer",
"specsjeng",
"specbzip"]



power_data = []

for folder in Path(results_path).iterdir():

    if not (folder.is_dir() and folder.stem in benchmarks):
        continue

    benchmark_name = folder.stem
    print("\nBenchmark: " + benchmark_name)
    
    for txt_file in folder.iterdir():
        config_name = txt_file.stem
        print("\tParsing file: " + str(txt_file))
        
        result_dict = parse_txts(str(txt_file))
        result_dict["Benchmark"] = benchmark_name
        result_dict["Config"] = config_name
        power_data.append(result_dict)


pd.DataFrame(power_data).to_csv("out.csv")
