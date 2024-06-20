from datetime import datetime


def scheduler():
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
        print("Prime check in time has already passed, but we will check you in now")
        return 0

    days = int(timer[0].split(" ")[0]) - 1
    timerBreakdown = datetime.strptime(timer[-1].strip(), "%H:%M:%S.%f")
    totalSeconds = (days * 86400) + (timerBreakdown.hour * 3600) + \
        (timerBreakdown.minute * 60) + timerBreakdown.second
    return totalSeconds


if __name__ == "__main__":
    sleepTime = scheduler()
    print(sleepTime)
