import argparse
import os

import data_loader
import ad_checks
import endpoint_checks
import patch_checks
import scoring
import report
import department_breakdown 
import sys


def main():
    parser = argparse.ArgumentParser(description="Generate a consolidated security posture report.")
    parser.add_argument(
        "--data-dir", default="sample_data",
        help="Folder containing ad_export.csv, endpoint_compliance.csv, patch_status.csv"
    )
    parser.add_argument(
        "--output", default=None,
        help="Optional file path to save the report to, e.g. report.txt"
    )
    args = parser.parse_args()

    try:
        users = data_loader.load_ad_export(os.path.join(args.data_dir, "ad_export.csv"))
        devices = data_loader.load_endpoint_compliance(os.path.join(args.data_dir, "endpoint_compliance.csv"))
        user_department, device_owner = department_breakdown.build_lookup_tables(users, devices)
        patch_rows = data_loader.load_patch_status(os.path.join(args.data_dir, "patch_status.csv"))
    except FileNotFoundError as e:
        print(f"Error: couldn't find a required data file - {e}")
        print(f"Check that '{args.data_dir}' contains ad_export.csv, endpoint_compliance.csv, and patch_status.csv")
        return

    findings_by_category = {
        "stale_accounts": ad_checks.check_stale_accounts(users),
        "non_expiring_passwords": ad_checks.check_non_expiring_passwords(users),
        "privileged_without_mfa": ad_checks.check_privileged_without_mfa(users),
        "noncompliant_devices": endpoint_checks.check_noncompliant_devices(devices),
        "unencrypted_devices": endpoint_checks.check_unencrypted_devices(devices),
        "stale_checkins": endpoint_checks.check_stale_checkins(devices),
        "overdue_patches": patch_checks.check_overdue_patches(patch_rows),
        "stale_patch_scans": patch_checks.check_stale_patch_scans(patch_rows),
    }

    department_counts = department_breakdown.count_by_department(findings_by_category, user_department, device_owner)
    risk_summary = scoring.calculate_risk_score(findings_by_category)

    report_text = report.build_report_text(findings_by_category, risk_summary, department_counts)
    print(report_text)

    if args.output:
        report.write_report_to_file(report_text, args.output)
        print(f"\nReport saved to {args.output}") 
    
    if risk_summary.get("high_severity_count", 0) > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()