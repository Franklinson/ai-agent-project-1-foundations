"""Time tool for getting current time information."""

from datetime import datetime
from typing import Dict, Any


def get_time(timezone: str = 'UTC', format: str = 'iso') -> Dict[str, Any]:
    """
    Get current time information.
    
    Args:
        timezone: Timezone (currently only UTC supported)
        format: Output format ('iso', 'timestamp', 'readable')
    
    Returns:
        Dict with time information
    """
    try:
        now = datetime.utcnow()
        
        formats = {
            'iso': now.isoformat(),
            'timestamp': now.timestamp(),
            'readable': now.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if format not in formats:
            return {'success': False, 'error': f'Invalid format: {format}'}
        
        return {
            'success': True,
            'time': formats[format],
            'format': format,
            'timezone': timezone,
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'hour': now.hour,
            'minute': now.minute,
            'second': now.second
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}
