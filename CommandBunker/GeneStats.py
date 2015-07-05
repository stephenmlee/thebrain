import json

__author__ = 'stephen'


def main():
    max_generation = 39
    species = 1

    experiment_archive = "Archive/xor/20150705 09:47:47/generation"

    print "Generation|species|population|max fitness|average fitness|average adjusted fitness"

    for generation in range(1, max_generation + 1):
        historical_record = open("%s-%s.json" % (experiment_archive, generation), "r")
        genes = json.load(historical_record)
        species_members = filter(lambda g: g.get("species", 0) == species, genes)

        historical_record.close()

        print "%s|%s|%s|%s|%s|%s" % (generation, species,
                                  len(species_members),
                                  max(species_members, key=lambda m: m.get("fitness", 0))["fitness"] if len(species_members) > 0 else "",
                                  sum([m.get("fitness",0) for m in species_members])/ len(species_members) if len(species_members) > 0 else "",
                                  sum([m.get("adjusted_fitness",0) for m in species_members])/ len(species_members) if len(species_members) > 0 else "")



if __name__ == "__main__":
    main()
