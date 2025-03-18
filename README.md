# iDrac_Info

# iDRAC Monitoring via Redfish API

This Python script monitors Dell iDRAC servers using the Redfish API. It collects and displays information about CPU temperatures, fan speeds, fan health, CPU health, and RAM health. The data is displayed in a formatted table and updated every 60 seconds.

## Features:
- Automatic connection to multiple iDRACs.
- Collection of thermal data (CPU temperatures and fan speeds).
- Health checks for components (fans, CPU, and RAM).
- Data displayed in an organized table.

## Requirements:
- Python 3.x
- `python-redfish` library
- `prettytable` library

- ### Configuration

Before running the script, add the iDRACs you want to monitor by updating the `idrac_list` in the script:

```python
idrac_list = [
    {"ip": "192.168.1.100", "user": "root", "password": "calvin"},
    {"ip": "192.168.1.101", "user": "root", "password": "calvin"},
]

## Usage

Run the script from the command line or directly with Python:

```sh
python script.py

## Output

![Example Output](output.png)
