#-----------------------------------------------------------------------------
# Title       : Report Plotting Script
# File        : plot_metrics.py
# Date        : 2025-06-04
# Author      : Erick Andrés Obregón Fonseca
# Email       : erickof@ieee.org
# Organization: ECASLAB
# Description : Reads report_summary.csv and generates comparison plots of
#               area, delay, and total power per adder and bit width.
# License     : MIT License (see LICENSE file for details)
#-----------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os

from typing import List

def plot_metric(df: pd.DataFrame, metric: str, output_dir: str = ".") -> None:
    """
    Plots a given metric across all adders grouped by bit width.

    Args:
        df (pd.DataFrame): DataFrame containing all design results.
        metric (str): The metric to plot (e.g. 'area (um^2)', 'delay (ns)').
        output_dir (str): Directory where plots will be saved.
    """
    plt.figure(figsize=(8, 5))

    for adder in df['adder'].unique():
        subset: pd.Series = df[df['adder'] == adder]
        plt.plot(subset['bits'], subset[metric], marker='o', label=adder)

    plt.title(f'{metric} vs Bit Width')
    plt.xlabel('Bit Width')
    plt.ylabel(metric)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Create filename-safe version of metric
    filename: str = f'{metric.replace(" ", "_").replace("(", "").replace(")", "")}.png'
    filepath: str = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    print(f'Saved plot: {filepath}')
    plt.close()

def main():
    input_csv: str = 'report_summary.csv'
    output_dir: str = 'plots'

    os.makedirs(output_dir, exist_ok=True)

    df: pd.DataFrame = pd.read_csv(input_csv)

    metrics_to_plot: List[str] = [
        'area (um^2)', 'delay (ns)', 'internal power (uW)',
        'switching power (uW)', 'leakage power (uW)', 'total power (uW)'
    ]

    for metric in metrics_to_plot:
        if metric in df.columns:
            plot_metric(df, metric, output_dir)

if __name__ == '__main__':
    main()
