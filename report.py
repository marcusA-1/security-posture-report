"""
report.py
----------
Plumbing: formats findings + risk score into a readable console report.
Already working -- you shouldn't need to touch this to get the project
running, but improving it (e.g. adding an HTML export) is a good stretch
goal once the checks and scoring are done.
"""

CATEGORY_LABELS = {
    "stale_accounts": "Stale (but enabled) accounts",
    "non_expiring_passwords": "Accounts with non-expiring passwords",
    "privileged_without_mfa": "Privileged accounts without MFA",
    "noncompliant_devices": "Noncompliant devices",
    "unencrypted_devices": "Devices without disk encryption",
    "stale_checkins": "Devices with stale check-ins",
    "overdue_patches": "Devices with overdue critical patches",
    "stale_patch_scans": "Devices with stale patch scans",
}

def format_user_finding(user):
    return f"{user['Username']} ({user['Department']}) — last logon {user['LastLogon']}"

def format_device_finding(device):
    return f"{device['DeviceName']} (owner: {device['Owner']}) — last check-in {device['LastCheckIn']}"

def format_patch_finding(patch):
    return f"{patch['DeviceName']} — {patch['MissingCriticalPatches']} missing critical patches (last scanned {patch['LastPatchScan']})"
CATEGORY_FORMATTERS = {
    "stale_accounts": format_user_finding,
    "non_expiring_passwords": format_user_finding,
    "privileged_without_mfa": format_user_finding,
    "noncompliant_devices": format_device_finding,
    "unencrypted_devices": format_device_finding,
    "stale_checkins": format_device_finding,
    "overdue_patches": format_patch_finding,
    "stale_patch_scans": format_patch_finding,
}
def build_report_text(findings_by_category, risk_summary, department_counts=None):
    lines = []
    lines.append("=" * 60)
    lines.append("SECURITY POSTURE REPORT")
    lines.append("=" * 60)

    total_findings = sum(len(v) for v in findings_by_category.values())
    lines.append(f"\nTotal findings: {total_findings}")

    if risk_summary:
        lines.append(f"Overall risk score: {risk_summary.get('overall_score')}")
        lines.append(
            f"  High: {risk_summary.get('high_severity_count', 0)}  "
            f"Medium: {risk_summary.get('medium_severity_count', 0)}  "
            f"Low: {risk_summary.get('low_severity_count', 0)}"
        )
    if department_counts:
        lines.append("\n--- Findings by Department ---")
        for department, count in sorted(department_counts.items(), key=lambda item: item[1], reverse=True):
            lines.append(f" {department}: {count}")

    for category, findings in findings_by_category.items():
        label = CATEGORY_LABELS.get(category, category)
        lines.append(f"\n--- {label} ({len(findings)}) ---")
        if not findings:
            lines.append("  None")
            continue
        formatter = CATEGORY_FORMATTERS.get(category, str)
        for finding in findings:
            lines.append(f"  - {formatter(finding)}")

    return "\n".join(lines)

def write_report_to_file(report_text, filepath):
    with open(filepath, "w") as f:
        f.write(report_text)