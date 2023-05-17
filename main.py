import requests
from datetime import datetime, timedelta
import csv

def get_completed_challenges(username, page=0):
    url = f"https://www.codewars.com/api/v1/users/{username}/code-challenges/completed"
    params = {'page': page}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        return []

def count_challenges_in_timeframe(username, start_date, end_date):
    page = 0
    count = 0

    while True:
        challenges = get_completed_challenges(username, page)
        if not challenges:
            break

        for challenge in challenges:
            completed_at = datetime.fromisoformat(challenge['completedAt']).date()
            if start_date <= completed_at <= end_date:
                count += 1
            elif completed_at < start_date:  # Assumes challenges are sorted in descending order of completion
                return count
        
        page += 1

    return count

f = open("data.csv")
data = csv.reader(f)
next(data)
f = open('result.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(["name",'dainly', 'week',"month","count"])
for i in data:
    username = i[2]


    # Get today's date
    today = datetime.now().date()

    # Calculate the start and end dates for daily, weekly, and monthly timeframes
    daily_start = today - timedelta(days=1)
    weekly_start = today - timedelta(weeks=1)
    monthly_start = today.replace(day=1) - timedelta(days=1)

    # Count for the daily timeframe (yesterday to today)
    daily_count = count_challenges_in_timeframe(username, daily_start, today)

    # Count for the weekly timeframe (last week's start date to today)
    weekly_count = count_challenges_in_timeframe(username, weekly_start, today)

    # Count for the monthly timeframe (previous month's start date to today)
    monthly_count = count_challenges_in_timeframe(username, monthly_start, today)

    
    writer = csv.writer(f)
    writer.writerow([i[0], daily_count,weekly_count,monthly_count])
