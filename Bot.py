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

def run_immediately_for_test():
    simpleRoll(Vars.get_config("myServer"))

# Schedule jobs for each configuration
print("\n")
print("Bot.py launch, waiting for schedule job ...")
print("\n")

if len(sys.argv) > 1 and sys.argv[1] == "--run-now":
    print("Running jobs immediately...")
    run_immediately_for_test()
else:
    schedule_job("gomenasai")
    schedule_job("yameteKudasai")
    schedule_job("myServer")

    print("\n")

    while True:
        schedule.run_pending()
        time.sleep(1)
