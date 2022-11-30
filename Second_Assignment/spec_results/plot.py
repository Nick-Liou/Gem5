import pandas as pd
import seaborn as sns
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

    
    
def plot_L1d(df: pd.DataFrame):
    df["Config"] = df["Config"].str.replace("default", "L1d_64kB")
    df = df[df["Config"].str.match("L1d_\d+kB")]
    print(df[["Config", "system.cpu.cpi"]])
    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="system.cpu.cpi", 
    kind="bar", hue="Config")
    plt.show(block=True)

def plot_L2d(df: pd.DataFrame):
    df["Config"] = df["Config"].str.replace("default", "L2_2MB")
    df = df[df["Config"].str.match("L2_\d+MB")]
    print(df[["Config", "system.cpu.cpi"]])
    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="system.cpu.cpi", 
    kind="bar", hue="Config")
    plt.show(block=True)



df = pd.read_csv("results2.txt", delim_whitespace=True)
df[["Benchmark", "Config"]] = df["Benchmarks"].str.removeprefix("./").str.split("/", expand=True)
df.drop("Benchmarks", axis=1, inplace=True)
plot_L2d(df)

