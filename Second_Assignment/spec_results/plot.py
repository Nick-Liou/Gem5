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

def plot_L1i(df: pd.DataFrame):
    df["Config"] = df["Config"].str.replace("default", "L1i_16kB")
    df = df[df["Config"].str.match("L1i_\d+kB")]
    print(df[["Config", "system.cpu.cpi"]])
    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="system.cpu.cpi", 
    kind="bar", hue="Config")
    plt.show(block=True)

def plot_L2(df: pd.DataFrame):
    df["Config"] = df["Config"].str.replace("default", "L2_2MB")
    df = df[df["Config"].str.match("L2_\d+MB")]
    print(df[["Config", "system.cpu.cpi"]])
    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="system.cpu.cpi", 
    kind="bar", hue="Config")
    plt.show(block=True)

def plot_cacheline(df: pd.DataFrame):
    df["Config"] = df["Config"].str.replace("default", "Cacheline_64")
    df = df[df["Config"].str.match("Cacheline_\d+")]
    df["Config"] = pd.to_numeric(df["Config"].str.removeprefix("Cacheline_"))
    print(df[["Config", "system.cpu.cpi"]])
    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        y="system.cpu.cpi", 
    kind="bar", hue="Config")
    plt.show(block=True)

def plot_all(df: pd.DataFrame):

    default_cpi = df[df["Config"] == "default"][["Benchmark","system.cpu.cpi"]]
    default_cpi.rename(columns={"system.cpu.cpi": "default_cpi"}, inplace=True)
    # print(seq_data)

    print(default_cpi)
    df = df.merge(default_cpi, on="Benchmark")
    print(df)
    df["speedup"] = df["system.cpu.cpi"]/df["default_cpi"]
    print(df[["Config", "system.cpu.cpi"]])
    sns.catplot(data=df, x="Benchmark", 
#       y="system.cpu.dcache.overall_miss_rate::total", 
        # y="system.cpu.cpi",
        y="speedup", 
    kind="bar", hue="Config")
    plt.show(block=True)

df = pd.read_csv("results.txt", delim_whitespace=True)
df[["Benchmark", "Config"]] = df["Benchmarks"].str.split("/", expand=True)
df.drop("Benchmarks", axis=1, inplace=True)
df = df[df["Config"].str.match("(L\d.?_assoc_\d+)|default")]
plot_all(df)
#plot_cacheline(df)
#plot_all(df)
#plot_L1i(df)
#plot_L1d(df)
#plot_L2(df)

