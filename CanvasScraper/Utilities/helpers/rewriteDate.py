# This program is created by Al9912.

from datetime import datetime

def rewriteDate(date_str, message):
    if date_str:
            try:
                # Parse the ISO 8601 string
                dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

                # Reformat to your preferred style (for example: 'Oct 12, 2025, 3:57 PM')
                formatted = dt.strftime("%B %d, %Y, %I:%M %p")

                return formatted
            except ValueError:
                 return formatted
    else:
        return message