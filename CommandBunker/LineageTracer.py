import json

__author__ = 'stephen'


def main():
    target_id = 15104
    generation = 74

    experiment_archive = "Archive/xor/20150704 22:22:46/generation"
    lineage = []

    while generation > 1:
        historical_record = open("%s-%s.json" % (experiment_archive, generation), "r")
        genes = json.load(historical_record)
        historical_record.close()

        target = filter(lambda g: g["id"] == target_id, genes)[0]
        lineage.append(target)

        target_id = target["parent"]
        generation = target["generation"]

    print json.dumps(sorted(lineage, key=lambda o: o["generation"]))


if __name__ == "__main__":
    main()