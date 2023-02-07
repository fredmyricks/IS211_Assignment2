import csv
import urllib.request
import argparse
import logging
from datetime import datetime

def downloadData(url):
    response = urllib.request.urlopen(url)
    return csv.reader(response.read().decode("utf-8").splitlines())

def processData(csvData):
    header = next(csvData)
    invalid_rows = []
    people = list(csvData)
    with open("invalid_rows.txt", "w") as output_file:
        for i, row in enumerate(people):
            try:
                birthdate = datetime.strptime(row[1], "%Y-%m-%d")
            except ValueError:
                invalid_rows.append(i + 2)
        output_file.write(str(invalid_rows))
    return people

def displayPerson(id, personData):
    for i, person in enumerate(personData):
        if person[2] == str(id):
            print("Name:", person[0])
            print("Birthdate:", person[1])
            return
    print("Person not found")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='The URL to download the data from')
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log', level=logging.ERROR,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    logger = logging.getLogger('assignment2')

    try:
        csvData = downloadData(args.url)
    except Exception as e:
        logger.error(str(e))
        print('An error occurred while downloading the data. Please check the errors.log for more details.')
        return

    personData = processData(csvData)

    while True:
        id = int(input('Enter an ID to lookup: '))
        if id <= 0:
            break
        displayPerson(id, personData)

if __name__ == '__main__':
    main()