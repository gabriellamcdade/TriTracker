import csv

with open("data/activities.csv", "r") as file:
    activities = csv.DictReader(file)

    for activity in activities:
        print(activity)