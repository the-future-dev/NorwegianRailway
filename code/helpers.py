from datetime import datetime, timedelta
from rich.console import Console

console = Console(color_system="256")

class TimeFormatError(Exception()):
    pass

def dateToWeekday(date_string):
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_of_week = days[date_obj.weekday()]
    return day_of_week

def next_dayOfTheWeek(day):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    index = days.index(day)
    return days[(index + 1) % len(days)]

def inputWithFormat(prompt, format=None):
    while True:
        user_input = input(prompt)
        if format:
            try:
                dt = datetime.strptime(user_input, format)
                return dt.strftime(format)
            except ValueError:
                console.print(f'Invalid input. Please enter in the format: {format}', style='red')
        else:
            return user_input

def next_day(date_str: str) -> str:
    # Convert the input string to a datetime object
    date = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Add one day to the date
    next_date = date + timedelta(days=1)
    
    # Convert the resulting date back to a string in the desired format
    next_date_str = next_date.strftime('%Y-%m-%d')
    
    return next_date_str