import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_total_power(df: pd.DataFrame):
    df["total_power"] = df["core_runtime_dynamic"] + df["L2_runtime_dynamic"]
    df.sort_values(by=["total_power"], inplace=True)

    sns.catplot(data=df, x="total_power",
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="Config", 
        kind="bar"
        # y="sim_seconds",
        # kind="bar", hue="Config"
    )
    plt.show(block=True)

  
    
def plot_L1d(df: pd.DataFrame):
    df["Config"] = df["Config"].str.replace("default", "L1d_64kB")
    df = df[df["Config"].str.match("L1d_\d+kB")]
    print(df[["Config", "system.cpu.cpi"]])
    df.sort_values(by=["Config"], inplace=True)
    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="processor_peak_power", 
        # y="sim_seconds",
    kind="bar", hue="Config")
    plt.show(block=True)

def plot_L1i(df: pd.DataFrame):
    df["Config"] = df["Config"].str.replace("default", "L1i_32kB")
    df = df[df["Config"].str.match("L1i_\d+kB")]
    print(df[["Config", "system.cpu.cpi"]])
    df.sort_values(by=["Config"], inplace=True)
    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="processor_peak_power", 
        # y="sim_seconds",
    kind="bar", hue="Config")
    plt.show(block=True)

def plot_L2(df: pd.DataFrame):
    df["Config"] = df["Config"].str.replace("default", "L2_2MB")
    df = df[df["Config"].str.match("L2_\d+MB")]
    print(df[["Config", "system.cpu.cpi"]])
    df.sort_values(by=["Config"], inplace=True)
    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="processor_peak_power", 
        # y="sim_seconds",
    kind="bar", hue="Config")
    plt.show(block=True)

def plot_assoc(df: pd.DataFrame):
    df["Config"] = df["Config"].str.replace("default", "L2_assoc_8")
    print(df[["Config", "system.cpu.cpi"]])
    df.sort_values(by=["Config"], inplace=True)
    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="processor_peak_power", 
        # y="sim_seconds",
    kind="bar", hue="Config")
    plt.show(block=True)

def plot_cacheline(df: pd.DataFrame):
    df["Config"] = df["Config"].str.replace("default", "Cacheline_64")
    df = df[df["Config"].str.match("Cacheline_\d+")]

    print(df[["Config", "system.cpu.cpi"]])

    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="processor_peak_power", 
    kind="bar", hue="Config")
    plt.show(block=True)


perf_csv_path = "../Second_Assignment/spec_results/all.csv"
power_csv_path = "out.csv"


perf_data = pd.read_csv(perf_csv_path)
power_data = pd.read_csv(power_csv_path)


data = pd.merge(perf_data, power_data, how="inner", on=["Config", "Benchmark"])

if data.isnull().values.any():
    print("Warning: Nan values in dataframe")

plot_total_power(data)
plot_assoc(data)

# plot_cacheline(data)
# plot_L1i(data)
# plot_L1d(data)
plot_L2(data)

# df = df[df["Config"].str.match("default")]
