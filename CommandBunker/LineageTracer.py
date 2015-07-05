import json

__author__ = 'stephen'


def main():
    target_id = 7899
    generation = 39

    experiment_archive = "Archive/xor/20150705 09:47:47/generation"
    lineage = []

    while generation >= 1:
        historical_record = open("%s-%s.json" % (experiment_archive, generation), "r")
        genes = json.load(historical_record)
        historical_record.close()

        target = filter(lambda g: g["id"] == target_id, genes)[0]
        lineage.append(target)

        target_id = target.get("parent", "")
        generation = target.get("generation", 0)

    sorted_lineage = sorted(lineage, key=lambda o: o.get("generation", 0))

    for gene in sorted_lineage:
        print "%s|%s" % (int(gene.get("generation", 0)) + 1, gene["fitness"])

    print json.dumps(sorted_lineage)


if __name__ == "__main__":
    main()
