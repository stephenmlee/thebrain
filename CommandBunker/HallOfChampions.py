import glob
import json
import os
import re

__author__ = 'stephen'


def main():
    experiment_archive = "Archive/prophet"

    dirs = os.listdir(experiment_archive)

    champions = []

    for dir in dirs:
        files = glob.glob(os.path.join(experiment_archive, dir, "*.json"))

        files = sorted(files, key=lambda x: int(re.match(".*generation-([0-9]*).json", x).group(1)))
        files.reverse()

        historical_record = open(files[0], "r")
        genes = json.load(historical_record)
        historical_record.close()

        for gene in genes:
            if gene["champ"] == "Champion":
                gene["archive"] = files[0]
                champions.append(gene)

    print json.dumps(champions)


if __name__ == "__main__":
    main()
