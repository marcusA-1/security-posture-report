def build_lookup_tables(users: list[dict], devices: list[dict]) -> tuple[dict, dict]:
    """
    Buildstwo lookup dictionaries:
    - user_department: {username: department}
    - device_owner: {device_name: owner_username}
    """
    user_department = {}
    for user in users:
        user_department[user["Username"]] = user["Department"] 
        
    device_owner ={}
    for device in devices:
        device_owner[device["DeviceName"]] = device["Owner"] 
    return user_department, device_owner 

def get_department(finding: dict, user_department: dict, device_owner: dict) -> str:
    if "Department" in finding:
        return finding["Department"] 
    if "Owner" in finding:
        return user_department.get(finding["Owner"], "Unknown")
    if "DeviceName" in finding:
        owner = device_owner.get(finding["DeviceName"])
        return user_department.get(owner, "Unknown")
    return "Unknown" 

def count_by_department(findings_by_category: dict, user_department: dict, device_owner: dict) -> dict:
    counts = {}
    for category, findings in findings_by_category.items():
        for finding in findings:
            department = get_department(finding, user_department, device_owner)
            counts[department] = counts.get(department, 0) + 1
    return counts 
