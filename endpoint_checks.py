from datetime import datetime


def check_noncompliant_devices(devices: list[dict]) -> list[dict]:
    noncompliant = []
    for device in devices:
        if device["ComplianceState"] == "Noncompliant":
            noncompliant.append(device)
    return noncompliant
    


def check_unencrypted_devices(devices: list[dict]) -> list[dict]:
    unencrypted = []
    for device in devices:
        if device["BitLockerEnabled"] == "FALSE":
            unencrypted.append(device) 
    return unencrypted


def check_stale_checkins(devices: list[dict], stale_days_threshold: int = 30) -> list[dict]:
   stale_devices = []
   for device in devices: 
        last_checkin = datetime.strptime(device["LastCheckIn"], "%Y-%m-%d")
        days_since_checkin = (datetime.now() - last_checkin).days
        if days_since_checkin > stale_days_threshold:
            stale_devices.append(device)
   return stale_devices
        

