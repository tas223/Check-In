from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys


def retrieveFlightInfo():
    questions = [
        "first name",
        "last name",
        "confirmation code",
    ]
    answers = []
    for question in questions:
        print(f"What is your {question}?")
        answer = input().strip()
        notCorrect = True
        while notCorrect:
            print(
                f"You entered the {question} {answer}. Is that correct? (y/n)")
            ans = input().strip().lower()
            if ans == 'y':
                notCorrect = False
            else:
                print(f"What is your {question}?")
                answer = input().strip()
        answers.append(answer)
    return answers


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
    print("Your check in has been scheduled.")
    return totalSeconds


def launchCheckIn(confirmationCode, firstName, lastName):
    try:
        PATH = "/Users/aishanisrikumar/chromeDriver/chromedriver"
        service = Service(PATH)
        options = webdriver.ChromeOptions()
        chromeDriver = webdriver.Chrome(service=service, options=options)
        chromeDriver.get(
            "https://www.southwest.com/air/check-in/?clk=HC_Prepare_1284_CTA1")
        code = chromeDriver.find_element(By.ID, "confirmationNumber")
        code.send_keys(confirmationCode)
        passengerFirstName = chromeDriver.find_element(
            By.ID, "passengerFirstName")
        passengerFirstName.send_keys(firstName)
        passengerLastName = chromeDriver.find_element(
            By.ID, "passengerLastName")
        passengerLastName.send_keys(lastName)
        submit = chromeDriver.find_element(By.ID, "form-mixin--submit-button")
        submit.send_keys(Keys.RETURN)
        chromeDriver.quit()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    print("This service is only offered for Southwest Airlines. Do you wish to proceed? (y/n)")
    ans = input().strip().lower()
    if ans == 'n':
        print("Sorry. We can't check you in for your flight.")
        sys.exit(0)
    firstName, lastName, confirmationCode = retrieveFlightInfo()
    sleepTime = schedule()
    if sleepTime < 0:
        sys.exit(0)
    if sleepTime > 0:
        time.sleep(sleepTime)
    launchCheckIn(confirmationCode, firstName, lastName)
