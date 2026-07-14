from datetime import datetime


def check_stale_accounts(users: list[dict], inactive_days_threshold: int = 90) -> list[dict]:
    stale_users = []
    for user in users: 
        if user["Enabled"] != "TRUE": 
               continue 
        last_logon = datetime.strptime(user["LastLogon"], "%Y-%m-%d") 
        days_since_logon =(datetime.now() - last_logon).days
        if days_since_logon > inactive_days_threshold:
           stale_users.append(user)
    return stale_users


def check_non_expiring_passwords(users: list[dict]) -> list[dict]:
    non_expiring = []
    for user in users:
        if user["Enabled"] == "TRUE" and user["PasswordNeverExpires"] == "TRUE": 
            non_expiring.append(user)
    return non_expiring


def check_privileged_without_mfa(users: list[dict]) -> list[dict]:
    privileged_without_mfa = []
    for user in users:
        if user["MFAEnabled"] == "FALSE" and user["IsPrivileged"] == "TRUE": 
            privileged_without_mfa.append(user)
    return privileged_without_mfa  
