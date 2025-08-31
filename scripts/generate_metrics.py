"""
Title       : Report Generation Script
File        : collect_reports.py
Date        : 2025-06-04
Author      : Erick Andres Obregon Fonseca
Email       : erickof@ieee.org/erickof@estudiantec.cr
Description : Extract area, delay, and power metrics from EDA tool reports
              and consolidate them into a CSV summary.
License     : MIT.

This script automates the collection of key metrics (area, timing, power) from
synthesis and STA reports. It supports multiple adders and bit-widths,
controlled via environment variables, and produces a CSV summary file.

Environment Variables
---------------------
ADDERS : str
    Space-separated list of adder names (e.g., "rca cla ksa").
BIT_WIDTHS : str
    Space-separated list of bit-widths (e.g., "4 8 16 32").

Output
------
- report_summary.csv : Consolidated CSV report with metrics for all (adder,
  bit-width) combinations.
"""
import csv
import os
import re

from typing import Optional, Tuple, List, Dict


def extract_area(filepath: str) -> Optional[float]:
    """
    Extract the total area from an area report file.

    Parameters
    ----------
    filepath : str
        Path to the area report file.

    Returns
    -------
    Optional[float]
        The total area in square micrometers, or None if not found.
    """
    try:
        with open(filepath, "r") as f:
            content: str = f.read()

        match: Optional[re.Match[str]] = re.search(
            r"Total area:\s+([0-9.]+)", content
        )
        return float(match.group(1)) if match else None
    except Exception:
        return None


def extract_delay(filepath: str) -> Optional[float]:
    """
    Extract the data arrival time from a timing report file.

    Parameters
    ----------
    filepath : str
        Path to the timing report file.

    Returns
    -------
    Optional[float]
        The data arrival time in nanoseconds, or None if not found.
    """
    try:
        with open(filepath, "r") as f:
            content: str = f.read()

        match: Optional[re.Match[str]] = re.search(
            r"data arrival time\s+([0-9.]+)", content
        )
        return float(match.group(1)) if match else None
    except Exception:
        return None


def extract_power(filepath: str) -> Dict[str, Optional[float]]:
    """
    Extract power metrics from a power report file.

    Parameters
    ----------
    filepath : str
        Path to the power report file.

    Returns
    -------
    Dict[str, Optional[float]]
        Dictionary with internal, switching, leakage, and total power
        values in microwatts.
    """
    try:
        with open(filepath, "r") as f:
            content: str = f.read()

        match: Optional[re.Match[str]] = re.search(
            r"Total\s+([-+]?[0-9.eE+-]+) uW\s+([-+]?[0-9.eE+-]+) "
            r"uW\s+([-+]?[0-9.eE+-]+) uW\s+([-+]?[0-9.eE+-]+) uW",
            content,
        )

        power_values: Tuple = tuple(map(float, match.groups())) if match else (
            None, None, None, None
        )

        return {
            "internal power (uW)": power_values[0],
            "switching power (uW)": power_values[1],
            "leakage power (uW)": power_values[2],
            "total power (uW)": power_values[3],
        }
    except Exception:
        return {
            "internal power (uW)": None,
            "switching power (uW)": None,
            "leakage power (uW)": None,
            "total power (uW)": None,
        }


def collect_results() -> List[Dict[str, Optional[float]]]:
    """
    Collect area, delay, and power metrics for all adder designs.

    The adders and bit-widths to process are read from the environment
    variables ``ADDERS`` and ``BIT_WIDTHS``. For each combination,
    corresponding report files are parsed and results consolidated.

    Returns
    -------
    List[Dict[str, Optional[float]]]
        List of dictionaries with the following keys:
        - 'adder'
        - 'bits'
        - 'area (um^2)'
        - 'delay (ns)'
        - 'internal power (uW)'
        - 'switching power (uW)'
        - 'leakage power (uW)'
        - 'total power (uW)'
    """
    adders: List[str] = os.environ.get("ADDERS", "").split()
    bit_widths: List[str] = os.environ.get("BIT_WIDTHS", "").split()
    results: List[Dict[str, Optional[float]]] = []

    for adder in adders:
        for bits in bit_widths:
            design: str = f"{adder}{bits}"

            area_file: str = f"reports/{design}_area.rpt"
            power_file: str = f"reports/{design}_power.rpt"
            timing_file: str = f"reports/{design}_timing.rpt"

            area: Optional[float] = extract_area(area_file)
            delay: Optional[float] = extract_delay(timing_file)
            power: Dict[str, Optional[float]] = extract_power(power_file)

            results.append(
                {
                    "adder": adder,
                    "bits": int(bits),
                    "area (um^2)": area,
                    "delay (ns)": delay,
                    **power,
                }
            )

    return results


def write_csv(results: List[Dict[str, Optional[float]]], output_file: str) -> None:
    """
    Write collected metrics to a CSV file.

    Parameters
    ----------
    results : List[Dict[str, Optional[float]]]
        Metrics for each design, as returned by :func:`collect_results`.
    output_file : str
        Path to the CSV file to generate.
    """
    field_names = [
        "adder",
        "bits",
        "area (um^2)",
        "delay (ns)",
        "internal power (uW)",
        "switching power (uW)",
        "leakage power (uW)",
        "total power (uW)",
    ]

    with open(output_file, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    results: List[Dict[str, Optional[float]]] = collect_results()
    report_file: str = "report_summary.csv"
    write_csv(results, report_file)
    print(f"[INFO] Report written to {report_file}")
