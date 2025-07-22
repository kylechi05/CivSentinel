from datetime import datetime
from zoneinfo import ZoneInfo

def dateToCentralISO(dt_date: datetime) -> str:
    dt_central = dt_date.replace(tzinfo=ZoneInfo('America/Chicago'))
    iso_string = dt_central.isoformat()
    return iso_string
