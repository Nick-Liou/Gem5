import pandas as pd
from pathlib import Path
import re
import subprocess

# We already have a .csv file with a lot of relevant data.
# For each entry in that .csv, we will find the config.json and
# stats.txt file from that run, and run mcpat using it.
# Then, we will update that entry with the new data that
# mcpat produces.


def run_mcpat(mcpat_path: str, gem5_result_path: str):
    return_dict = {}


    script_args = ["python2.7",
                mcpat_path + "/Scripts/GEM5ToMcPAT.py",
                gem5_result_path + "/stats.txt",
                gem5_result_path + "/config.json",
                mcpat_path + "/mcpat/ProcessorDescriptionFiles/inorder_arm.xml"]
                
    # run gem5 to mcpat script
    subprocess.run(script_args, env={"PYTHONPATH": "."})

    mcpat_args = [  mcpat_path + "/mcpat/mcpat",
                    "-infile", "mcpat-out.xml",
                    "-print_level", "5" ]

    # run mcpat
    output = subprocess.run(mcpat_args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    lines = output.splitlines()
    print(lines[60])

    # Match the whole "Core:" block
    match = re.search("^Core:\s*((\n.*){6})", output, flags=re.MULTILINE)
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
    match = re.search("^L2\s*((\n.*){6})", output, flags=re.MULTILINE)
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

    print(return_dict)

    return return_dict





csv_file = "../Second_Assignment/spec_results/all.csv"
runs_path = "../Second_Assignment/spec_results"
mcpat_path = "/home/arch/Desktop/mcpat"


data = pd.read_csv(csv_file)

power_data = [] #list of dicts

for index, row in data.iterrows():
    folder_name = "/".join([runs_path,row["Benchmark"], row["Config"]])
    if Path(folder_name).exists():
        result_dict = run_mcpat(mcpat_path, folder_name)
        result_dict["Benchmark"] = row["Benchmark"]
        result_dict["Config"] = row["Config"]
        power_data.append(result_dict)
        pd.DataFrame(power_data).to_csv("out.csv")
    else:
        print("Directory '" + folder_name + "' not found, skipping...")



