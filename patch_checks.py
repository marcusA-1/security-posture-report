from datetime import datetime


def check_overdue_patches(patch_rows: list[dict], critical_threshold: int =5) -> list[dict]:
    overdue =[]
    for patch in patch_rows:
        if patch["MissingCriticalPatches"]>= critical_threshold:
            overdue.append(patch)
    return overdue


def check_stale_patch_scans(patch_rows: list[dict], stale_days_threshold: int = 14) -> list[dict]:
    stale_scans = []
    for patch in patch_rows:
        last_scan = datetime.strptime(patch["LastPatchScan"], "%Y-%m-%d")
        days_sincescan = (datetime.now() - last_scan).days
        if days_sincescan > stale_days_threshold:
            stale_scans.append(patch) 
    return stale_scans 
