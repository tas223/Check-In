from datetime import datetime
import sys
import subprocess


def askQuestion(question):
    """Prompts user with question and validates their answer.

    Args:
        question (str): question to ask user.

    Returns:
        str: answer confirmed by user.
    """
    print(question)
    answer = input().strip()
    notCorrect = True
    while notCorrect:
        print(
            f"You entered {answer}. Is that correct? (y/n)")
        ans = input().strip().lower()
        if ans == 'y':
            notCorrect = False
        else:
            print(question)
            answer = input().strip()
    return answer


def retrieveUserInfo():
    """Collects user information by passing questions in to askQuestion().

    Returns:
        list: a list of answers needed to check the user in.
    """
    questions = [
        "What is your first name?",
        "What is your last name?",
        "What is your confirmation code?"
    ]
    answers = []
    for question in questions:
        answers.append(askQuestion(question))
    return answers


def calculateFlightInfo():
    """Calculates time until check in and uses return value to signal whether to launch the subprocess script.

    Returns:
        str: returns the flight time if the user can still be checked or -1 if not.
    """

    flight = askQuestion(
        "Enter the date and time of your flight as MM-DD-YYYY HH:MM (24 hour format)")
    flightTime = datetime.strptime(flight, '%m-%d-%Y %H:%M')
    currentTime = datetime.now()
    delay = flightTime - currentTime
    timer = str(delay).split(',')

    if timer[0][0] == '-':
        print("Flight date has already passed. You can not be checked in for your flight.")
        return "-1"

    if len(timer) < 2:
        print("Optimal check in time has passed. You are being checked in now.")
        return flight

    print("Your check in is scheduled.")
    return flight


if __name__ == "__main__":
    """
        Confirms that user has a flight with Southwest, prompts user for flight information, and schedules check in.

        Usage: python checkIn.py
    """
    print("This service is only offered for Southwest Airlines. Do you wish to proceed? (y/n)")
    ans = input().strip().lower()
    if ans == "n":
        print("Sorry. We can't check you in for your flight.")
        sys.exit(0)

    firstName, lastName, confirmationCode = retrieveUserInfo()
    flightInfo = calculateFlightInfo()
    if flightInfo == "-1":
        sys.exit(0)

    try:
        subprocessCommand = ["python", "scheduler.py",
                             confirmationCode, firstName, lastName, flightInfo]
        scheduler = subprocess.Popen(
            subprocessCommand, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, start_new_session=True)
        sys.exit(0)
    except Exception as e:
        print("There was an error scheduling your flight. See error message below.")
        print(e)
