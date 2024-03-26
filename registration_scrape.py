import pymsgbox
import sys
import os
import requests
import schedule
import time
from pytz import timezone
from datetime import datetime
import threading

def show_message_box(url):
    pymsgbox.alert(f'Registrations for {url} are open!', 'Registration Alert')

def check_registration(urls, var1, var2, var3):
    # Set date/time format
    format = "%m-%d-%Y %H:%M:%S"

    # Get local timezone
    lt = datetime.now(timezone('US/Eastern'))  # Eastern Time Zone

    print(f"checking... Time is:{lt.strftime(format)}\n")

    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                if var1 in response.text or var2 in response.text or var3 in response.text:
                    result = f"{url} - Closed"
                else:
                    result = f"{url} - Registrations are open!"
                    # Show message box asynchronously
                    threading.Thread(target=show_message_box, args=(url,)).start()
                print(f"{lt.strftime(format)} - {result}\n")
            else:
                result = f"{url} - Failed to retrieve website content. Status code: {response.status_code}"
                print(f"{lt.strftime(format)} - {result}\n")
        except Exception as e:
            result = f"{url} - An error occurred: {str(e)}"
            print(f"{lt.strftime(format)} - {result}\n")

        # Append the result to the log file with the localized time
        log_file = os.path.expanduser('scrape.log')  # Get full path to the home directory
        with open(log_file, 'a') as f:
            f.write(f"{lt.strftime(format)} - {result}\n")



# Ensure the scrape.log file exists
log_file = os.path.expanduser('scrape.log')  # Get full path to the home directory
try:
    open(log_file, 'a').close()  # Create the file if it doesn't exist
except Exception as e:
    print(f"An error occurred while creating the file {log_file}: {str(e)}")

# List of URLs to check
urls = ['https://drunkenslug.com/register', 'https://www.kleverig.eu/register.php', 'https://ninjacentral.co.za/register']

# Define the strings to look for in the response text
var1 = "Sorry! The Bar is closed"
var2 = "Sorry, registrations are closed"
var3 = "Registrations are currently invite only"

# Run the check_registration() function immediately
print("Starting Check Registration\n")
check_registration(urls, var1, var2, var3)

# Schedule the job to run every 5 minutes
schedule.every(8).hours.do(check_registration, urls, var1, var2, var3)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
