# security-posture-report

## Why I built this

Managing IT infrastructure and security operations across 800+ users spanning 7 separate businesses means routinely cross-referencing identity, endpoint, and patch data across multiple systems — Active Directory/Entra ID, endpoint management, and patch management — to get a clear picture of overall risk. This tool automates that correlation, producing a single consolidated report instead of checking several consoles separately.

## What it does

Reads three CSV exports — an Active Directory/Entra user export, an endpoint compliance export, and a patch status export — and runs eight checks across them:

- Stale but enabled accounts
- Accounts with non-expiring passwords
- Privileged accounts without MFA
- Noncompliant devices
- Devices without disk encryption
- Devices with stale check-ins
- Devices with overdue critical patches
- Devices with stale patch scans

Findings are weighted by severity and combined into an overall risk score, then broken down by business department so it's clear which part of the organization carries the most risk. The report prints to the console and can optionally be saved to a file.

## Example output

============================================================
SECURITY POSTURE REPORT
Total findings: 67
Overall risk score: 455
High: 40  Medium: 8  Low: 19
--- Findings by Department ---
Finance: 17
Glazerite Sales: 16
HR: 15
Emplas: 9
Manufacturing: 6
Warehouse: 3
IT: 1
--- Privileged accounts without MFA (3) ---

user000 (Finance) — last logon 2026-06-27
user013 (Manufacturing) — last logon 2026-07-10
user026 (Manufacturing) — last logon 2026-06-02

## How to run it

python main.py


Optional flags:
- `--data-dir <folder>` — point to a different folder of CSV exports (defaults to `sample_data`)
- `--output <file>` — save the report to a file in addition to printing it

Data in `sample_data/` is entirely synthetic — no real organizational data is used anywhere in this repository.

## Design decisions

Findings are weighted by severity — privileged accounts without MFA and unencrypted devices are weighted highest, since they represent the most direct compromise risk, down to lower-weighted hygiene issues like stale check-ins. Weighted counts roll up into an overall score plus a high/medium/low breakdown.

Device and patch findings don't carry department information directly, so the tool builds lookup tables at runtime to trace a device back to its owner, and an owner back to their department — the same basic principle used to correlate separate log sources together.

The tool exits with a non-zero status code when high-severity findings are present, so it can be plugged into automated workflows or scheduled tasks rather than only run manually.

## Roadmap

- Chart/visual summary of findings
- Automated test suite
- CI pipeline
- Historical tracking to flag new findings vs. recurring ones