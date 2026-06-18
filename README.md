# Care Transition Efficiency & Placement Outcome Analytics

## Overview

This project analyzes the efficiency of the Unaccompanied Children (UAC) care transition pipeline from CBP custody to HHS care and sponsor placement.

The dashboard provides insights into transfer efficiency, discharge effectiveness, pipeline throughput, backlog accumulation, and outcome stability using interactive visualizations.

## Features

* Transfer Efficiency Analysis
* Discharge Effectiveness Monitoring
* Pipeline Throughput Tracking
* Backlog Detection
* Outcome Stability Analysis
* Interactive Streamlit Dashboard
* KPI Monitoring and Alerts

## Technologies Used

* Python
* Pandas
* NumPy
* Plotly
* Streamlit

## Dataset

The dataset contains daily records of:

* Children apprehended and placed in CBP custody
* Children in CBP custody
* Children transferred out of CBP custody
* Children in HHS Care
* Children discharged from HHS Care

## Key Performance Indicators

### Transfer Efficiency Ratio

Transfers ÷ CBP Custody

### Discharge Effectiveness Index

Discharges ÷ HHS Care

### Pipeline Throughput

Discharges ÷ Apprehensions

### Backlog Accumulation Rate

HHS Care − Discharges

## Dashboard Preview

Add screenshots of your dashboard here.

## Installation

```bash
pip install -r requirements.txt
streamlit run uac_dashboard.py
```

## Project Outcomes

* Identified care transition bottlenecks
* Measured placement effectiveness
* Evaluated system throughput
* Provided actionable operational insights

## Author

Arpita
