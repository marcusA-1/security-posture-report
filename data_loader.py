import csv


def load_csv(path):
    """Read a CSV file into a list of dicts (one dict per row)."""
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load_ad_export(path):
    return load_csv(path)


def load_endpoint_compliance(path):
    return load_csv(path)


def load_patch_status(path):
    rows = load_csv(path)
    for row in rows:
        try:
            row["MissingCriticalPatches"] = int(row["MissingCriticalPatches"])
        except (ValueError, KeyError):
            print(f"Warning: skipping invalid MissingCriticalPatches value for {row.get('DeviceName', 'unknown device')}, defaulting to 0")
            row["MissingCriticalPatches"] = 0
    return rows
        
