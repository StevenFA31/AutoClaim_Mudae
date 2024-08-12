import Vars
import time
import schedule
import sys
from Function import simpleRoll

# Function to schedule jobs based on configuration
def schedule_job(config_name):
    config = Vars.get_config(config_name)
    if config:
        timeString = ':' + config['repeatMinute']
        print(f"Scheduling {config_name} job at {timeString}")
        schedule.every().hour.at(timeString).do(simpleRoll, config=config)
    else:
        print(f"Configuration {config_name} not found.")

# Schedule jobs for each configuration
print("\n")
print("Bot.py launch, waiting for schedule job ...")
print("\n")

schedule_job("myServer")

print("\n")

while True:
    schedule.run_pending()
    time.sleep(1)
