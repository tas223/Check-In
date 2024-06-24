from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def retrieveFlightInfo():
    print("This service is only offered for Southwest Airlines. Do you wish to proceed? (y/n)")
    ans = input().strip().lower()
    if ans == 'n':
        print("Sorry. We can't check you in for your flight.")
        return -1
    print("What is your first name?")
    firstName = input().strip().lower().capitalize()
    notCorrect = True
    while notCorrect:
        print("You entered the first name " +
              firstName + ". Is that correct? (y/n)")
        ans = input().strip().lower()
        if ans == 'y':
            notCorrect = False
        else:
            print("What is your first name?")
            firstName = input().strip().lower().capitalize()
    print("What is your last name?")
    lastName = input().strip().lower().capitalize()
    notCorrect = True
    while notCorrect:
        print("You entered the last name " +
              lastName + ". Is that correct? (y/n)")
        ans = input().strip().lower()
        if ans == 'y':
            notCorrect = False
        else:
            print("What is your last name?")
            lastName = input().strip().lower().capitalize()
    print("What is your confirmation code or ticket number?")
    code = input().strip().upper()
    notCorrect = True
    while notCorrect:
        print("You entered the confirmation code/ticket number " +
              code + ". Is that correct? (y/n)")
        ans = input().strip().lower()
        if ans == 'y':
            notCorrect = False
        else:
            print("What is your confirmation code or ticket number?")
            code = input().strip().upper()


def schedule():
    print("Enter the date and time of your flight as MM-DD-YYYY HH:MM")
    flight = input().strip()
    flightTime = datetime.strptime(flight, '%m-%d-%Y %H:%M')
    currentTime = datetime.now()
    delay = flightTime - currentTime
    timer = str(delay).split(',')

    if timer[0][0] == '-':
        print("Flight date has already passed. You can not be checked in for your flight.")
        return -1

    if len(timer) < 2:
        print("Optimal check in time has passed. You are being checked in now.")
        return 0

    days = int(timer[0].split(" ")[0]) - 1
    timerBreakdown = datetime.strptime(timer[-1].strip(), "%H:%M:%S.%f")
    totalSeconds = (days * 86400) + (timerBreakdown.hour * 3600) + \
        (timerBreakdown.minute * 60) + timerBreakdown.second
    return totalSeconds


def launchCheckIn():
    # SOUTHWEST ONLY
    try:
        PATH = "/Users/aishanisrikumar/chromeDriver/chromedriver"
        service = Service(PATH)
        options = webdriver.ChromeOptions()
        chromeDriver = webdriver.Chrome(service=service, options=options)
        chromeDriver.get(
            "https://www.southwest.com/air/check-in/?clk=HC_Prepare_1284_CTA1")
        code = chromeDriver.find_element(By.ID, "confirmationNumber")
        code.send_keys("Confirmation Code")
        firstName = chromeDriver.find_element(By.ID, "passengerFirstName")
        firstName.send_keys("First Name")
        lastName = chromeDriver.find_element(By.ID, "passengerLastName")
        lastName.send_keys("Last Name")
        submit = chromeDriver.find_element(By.ID, "form-mixin--submit-button")
        submit.send_keys(Keys.RETURN)
        chromeDriver.quit()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    launchCheckIn()
    # sleepTime = schedule()
    # if sleepTime > 0:
    #     print("Your check in has been scheduled.")
    #     time.sleep(sleepTime)
