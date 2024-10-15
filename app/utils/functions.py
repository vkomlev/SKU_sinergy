from app.services.base_service import BaseService
import datetime, re

def apply_transformation(value, transformation, **kwargs):
    if transformation == 'db_get_key_from_fields':
        service = kwargs.get('service')
        if service:
            return service.get_key_from_fields(value=value, **kwargs)
    elif transformation == 'parse_date_string':
        return parse_date_string(value)
    # Можно добавить дополнительные преобразования
    return value

def parse_date_string(value):
    """Parse date range strings and other formats to return the appropriate date."""
    if isinstance(value, str):
        try:
            # Match patterns like "17 — 18 сентября"
            match = re.match(r'\d+\s*[–—\-]\s*\d+\s*(\D+)', value)
            if match:
                day = match.group(0).split()[-1]
                month = match.group(1).strip()
                date_str = f"{day} {month} {datetime.datetime.now().year}"
                return datetime.datetime.strptime(date_str, '%d %B %Y').date()

            # Match single date with extra text, e.g. "18.09.2024\nДубль. Товар у акопа"
            match = re.match(r'\d{2}\.\d{2}\.\d{4}', value)
            if match:
                return datetime.datetime.strptime(match.group(0), '%d.%m.%Y').date()
        except ValueError:
            pass
    elif isinstance(value, datetime.date):
        return value
    # For other non-date texts, return None
    return None