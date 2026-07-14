def calculate_risk_score(findings_by_category: dict) -> dict:
    weights = {
        "privileged_without_mfa": 10,
        "unencrypted_devices": 10,
        "non_expiring_passwords": 5,
        "overdue_patches": 8,
        "noncompliant_devices": 10,
        "stale_accounts": 8,
        "stale_checkins": 3,
        "stale_patch_scans": 3,
    }
    overall_score = 0
    high_severity_count = 0
    medium_severity_count = 0
    low_severity_count = 0

    for category, findings in findings_by_category.items():
        weight = weights.get(category, 1)
        overall_score += len(findings) * weight
        if weight >= 8:
            high_severity_count += len(findings)
        elif weight >= 5:
            medium_severity_count += len(findings)
        else:
            low_severity_count += len(findings)

    return {
        "overall_score": overall_score,
        "high_severity_count": high_severity_count,
        "medium_severity_count": medium_severity_count,
        "low_severity_count": low_severity_count,
    }
        

