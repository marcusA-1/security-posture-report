# security-posture-report — Build Spec

## What it does
Reads three CSV exports (Active Directory/Entra users, endpoint compliance, patch status), runs a set of security checks against each, scores the overall risk, and prints a consolidated report. The idea: instead of checking three different consoles, one report shows everything that needs attention.

## Why (for the manager pitch)
You already manually cross-reference this information during incident response and audits. This turns it into a five-second command instead of three logins and manual comparison. It's also a natural stepping stone toward the SIEM correlation logic used in real detection engineering — which is directly relevant to the Security+ /Azure certs you're asking to have funded.

## Data sources (see `sample_data/` for exact format — synthetic data, not real)

**`ad_export.csv`** — Username, Department, Enabled, LastLogon (YYYY-MM-DD), PasswordNeverExpires, IsPrivileged, MFAEnabled (all TRUE/FALSE except dates)

**`endpoint_compliance.csv`** — DeviceName, Owner, ComplianceState (Compliant/Noncompliant), OSVersion, BitLockerEnabled, LastCheckIn (YYYY-MM-DD)

**`patch_status.csv`** — DeviceName, MissingCriticalPatches (integer), LastPatchScan (YYYY-MM-DD)

## Modules and what YOU need to implement

### `ad_checks.py`
- `check_stale_accounts(users, inactive_days_threshold=90)` — return a list of enabled users whose LastLogon is older than the threshold. Stale-but-enabled accounts are a classic attack surface (nobody notices if they're compromised).
- `check_non_expiring_passwords(users)` — return enabled users with PasswordNeverExpires == TRUE.
- `check_privileged_without_mfa(users)` — return users where IsPrivileged == TRUE and MFAEnabled == FALSE. This one should probably be treated as higher severity than the others — your call on how to reflect that.

### `endpoint_checks.py`
- `check_noncompliant_devices(devices)` — return devices where ComplianceState == "Noncompliant".
- `check_unencrypted_devices(devices)` — return devices where BitLockerEnabled == FALSE.
- `check_stale_checkins(devices, stale_days_threshold=30)` — return devices whose LastCheckIn is older than the threshold (a device that hasn't checked in might be lost, stolen, or offline for a suspicious reason).

### `patch_checks.py`
- `check_overdue_patches(patch_rows, critical_threshold=5)` — return devices with MissingCriticalPatches >= threshold.
- `check_stale_patch_scans(patch_rows, stale_days_threshold=14)` — return devices whose LastPatchScan is older than the threshold (if a device hasn't scanned recently, you don't actually know its patch state).

### `scoring.py`
- `calculate_risk_score(findings_by_category)` — takes a dict of {category_name: [list of findings]} and returns an overall numeric score plus a severity breakdown (e.g. high/medium/low counts). **This is the part that needs real thought**: not all findings are equally bad. A privileged account without MFA is worse than one stale device check-in. Decide your own weighting and be ready to explain why in an interview — there's no single right answer here, just defensible reasoning.

## Already built for you (plumbing, not the judgment calls)
- `data_loader.py` — CSV loading helpers
- `main.py` — wires everything together: loads data, calls your check functions, passes results to scoring, prints the report
- `report.py` — basic console report formatter (feel free to improve this once the checks work — an HTML export would be a good stretch goal)

## How to work through this
1. Get `ad_checks.py` working first, run `python main.py` after each function and check the output makes sense against `sample_data/ad_export.csv` (open it in Excel/VS Code and manually verify your script is catching the right rows).
2. Repeat for `endpoint_checks.py` and `patch_checks.py`.
3. Do `scoring.py` last, once you can see what findings actually look like.
4. Write your own README once it works, explaining what it does and why — that's what goes on GitHub and what you'd walk your manager through.

Ping me once you've had a go at `check_stale_accounts` (the first function) and I'll review what you've written before you move to the next one.
