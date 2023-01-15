import csv
import sys


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    sequences = {}

    with open(sys.argv[2]) as txt_file:
        dna = txt_file.read()

    with open(sys.argv[1]) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            line = row
            line.pop(0)
            for item in line:
                sequences[item] = 0
            break

    for key in sequences:
        rep = repeat_count(dna, key)
        sequences[key] = rep

    with open(sys.argv[1]) as csv_file:
        reader = csv.DictReader(csv_file)
        for person in reader:
            match_count = 0
            for key in sequences:
                if int(person[key]) == sequences[key]:
                    match_count += 1
            if match_count == len(sequences):
                print(person["name"])
                sys.exit(0)
                
        print('No match')
    
            
def repeat_count(dna, STR):
    start = 0
    end = len(STR)
    repeats = 0
    for i in range(len(dna)):
        if dna[start:end] == STR:
            tmp = 0
            while dna[start:end] == STR:
                tmp += 1
                start += len(STR)
                end += len(STR)
                if tmp > repeats:
                    repeats = tmp
        else:
            start += 1
            end += 1
    return repeats       


main()