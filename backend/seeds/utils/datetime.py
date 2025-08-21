from datetime import datetime
from zoneinfo import ZoneInfo

def dateTimeOccurredToISO(dt_str: str) -> str:
    dt = datetime.strptime(dt_str, '%m/%d/%Y %I:%M %p')
    return dateToCentralISO(dt)

def dateReportedToISO(dt_str: str) -> str:
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return dateToCentralISO(dt)

def dateToCentralISO(dt_date: datetime) -> str:
    dt_central = dt_date.replace(tzinfo=ZoneInfo('America/Chicago'))
    iso_string = dt_central.isoformat()
    return iso_string
