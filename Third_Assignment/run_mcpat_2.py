from pathlib import Path
import subprocess


def run_mcpat(mcpat_path: str, gem5_result_path: str, config_name: str, benchmark_name: str):

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

    path = Path("/".join([".", "results_mcpat", benchmark_name]))
    path.mkdir(exist_ok=True, parents=True)

    with open(path.as_posix() + "/" + config_name + ".txt", "w+") as f:
        f.writelines(output)





csv_file = "../Second_Assignment/spec_results/all.csv"
runs_path = "../Second_Assignment/spec_results"
mcpat_path = "/home/arch/Desktop/mcpat"


benchmarks = ["speclibm",
"specmcf",
"spechmmer",
"specsjeng",
"specbzip"]


for folder in Path(runs_path).iterdir():

    if not (folder.is_dir() and folder.stem in benchmarks):
        continue

    benchmark_name = folder.stem
    
    for config in folder.iterdir():
        config_name = config.stem
        print(config_name)

        run_mcpat(mcpat_path, str(config), config_name, benchmark_name)











# data = pd.read_csv(csv_file)

# power_data = [] #list of dicts

# for index, row in data.iterrows():
#     folder_name = "/".join([runs_path,row["Benchmark"], row["Config"]])
#     if Path(folder_name).exists():
#         result_dict = run_mcpat(mcpat_path, folder_name)
#         result_dict["Benchmark"] = row["Benchmark"]
#         result_dict["Config"] = row["Config"]
#         power_data.append(result_dict)
#         pd.DataFrame(power_data).to_csv("out.csv")
#     else:
#         print("Directory '" + folder_name + "' not found, skipping...")



