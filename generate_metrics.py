""""
Title       : Report Extraction Script
File        : generate_metrics.py
Date        : 2025-06-04
Author      : Erick Andrés Obregón Fonseca
Email       : erickof@ieee.org
Organization: ECASLAB
Description : Extracts area, delay, and power metrics from separate .rpt files
              (area, timing, and power) for multiple adders and bit widths.
              Generates a summarized CSV file with all results.
License     : MIT License (see LICENSE file for details)
"""
import csv
import os
import re

from typing import Optional, Tuple, List, Dict

def extract_area(filepath: str) -> Optional[float]:
    """Extracts the total area from a given report file.

    Args:
        filepath (str): Path to the area report file.

    Returns:
        Optional[float]: The total area in square micrometers, or None if not
            found.
    """
    try:
        with open(filepath, 'r') as f:
            content: str = f.read()

        match: Optional[re.Match[str]] = re.search(r'Total area:\s+([0-9.]+)',
                                                   content)

        return float(match.group(1)) if match else None
    except Exception:
        return None

def extract_delay(filepath: str) -> Optional[float]:
    """Extracts the data arrival time from a given timing report file.

    Args:
        filepath (str): Path to the timing report file.

    Returns:
        Optional[float]: The data arrival time in nanoseconds, or None if not
            found.
    """
    try:
        with open(filepath, 'r') as f:
            content: str = f.read()

        match: Optional[re.Match[str]] = re.search(
                                            r'data arrival time\s+([0-9.]+)',
                                            content)

        return float(match.group(1)) if match else None
    except Exception:
        return None

def extract_power(filepath: str) -> Dict[str, Optional[float]]:
    """Extracts power metrics from a given power report file.

    Args:
        filepath (str): Path to the power report file.

    Returns:
        Dict[str, Optional[float]]: A dictionary containing internal,
            switching, leakage, and total power values in microwatts.
    """
    try:
        with open(filepath, 'r') as f:
            content: str = f.read()

        match: Optional[re.Match[str]] = re.search(
            r'Total\s+([-+]?[0-9.eE+-]+) uW\s+([-+]?[0-9.eE+-]+) ' +\
            r'uW\s+([-+]?[0-9.eE+-]+) uW\s+([-+]?[0-9.eE+-]+) uW',
            content)

        power_values: Tuple = tuple(map(float, match.groups())) \
            if match else (None, None, None, None)

        power: Dict[str, Optional[float]] = {
            'internal power (uW)': power_values[0],
            'switching power (uW)': power_values[1],
            'leakage power (uW)': power_values[2],
            'total power (uW)': power_values[3]
        }

        return power
    except Exception:
        power: Dict[str, Optional[float]] = {
            'internal power (uW)': None,
            'switching power (uW)': None,
            'leakage power (uW)': None,
            'total power (uW)': None
        }

        return power

def collect_results() -> List[Dict[str, Optional[float]]]:
    """Collects area, delay, and power metrics for all designs.
    This function reads the environment variables ADDERS and BIT_WIDTHS to
    determine which adders and bit widths to process. It then extracts the
    metrics from the corresponding report files and compiles them into a list
    of dictionaries.
    Each dictionary contains the adder type, bit width, area, delay, and power
    metrics.
    
    Returns:
        List[Dict[str, Optional[float]]]: A list of dictionaries, each
            containing the metrics for a specific design.
    """
    adders: List[str] = os.environ.get('ADDERS', '').split()
    bit_widths: List[str] = os.environ.get('BIT_WIDTHS', '').split()
    results: List[Dict[str, Optional[float]]] = []

    for adder in adders:
        for bits in bit_widths:
            design: str = f'{adder}{bits}'

            area_file: str = f'reports/{design}_area.rpt'
            power_file: str = f'reports/{design}_power.rpt'
            timing_file: str = f'reports/{design}_timing.rpt'

            area: Optional[float] = extract_area(area_file)
            delay: Optional[float] = extract_delay(timing_file)
            power: Dict[str, Optional[float]] = extract_power(power_file)

            results.append({
                'adder': adder,
                'bits': int(bits),
                'area (um^2)': area,
                'delay (ns)': delay,
                **power
            })

    return results

def write_csv(
        results: List[Dict[str, Optional[float]]],
        output_file: str) -> None:
    """Writes the collected results to a CSV file.

    Args:
        results (List[Dict[str, Optional[float]]]): A list of dictionaries
            containing the metrics for each design.
        output_file (str): Path to the output CSV file where results will be
            saved.
    """
    field_names = [
        'adder', 'bits', 'area (um^2)', 'delay (ns)', 'internal power (uW)',
        'switching power (uW)', 'leakage power (uW)', 'total power (uW)'
    ]

    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(results)

if __name__ == '__main__':
    results: List[Dict[str, Optional[float]]] = collect_results()
    report_file: str = 'report_summary.csv'
    write_csv(results, report_file)
    print(f'Report written to {report_file}')
