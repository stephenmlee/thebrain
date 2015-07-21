import copy
import json
import os
import datetime
import numpy as np
from CommandBunker.ControlPanel import AGE_DROPOFF_THRESHOLD
from Cranium import NeuralNetwork
from Cranium.NeuralNetwork import UnstableNetworkError
from EvolutionChamber.Population import Population

__author__ = 'stephen'


def decode(genome_file):
    f = open(genome_file, 'r')
    g = json.load(f)
    f.close()
    return g


def generate():
    n = 0
    while True:
        n += 1
        yield "." if n % 2 == 0 else "+"


def archive_population(population, generation):
    file = "%s/generation-%s.json" % (archive, generation)
    f = open(file, "w")
    f.write(json.dumps([organism for organism in population.organisms], indent=2))
    f.close()


def std_normalize(timeseries):
    timeseries = copy.copy(timeseries)
    timeseries -= np.mean(timeseries, axis=0)
    timeseries /= np.std(timeseries, axis=0)
    return timeseries


def min_max_normalize(timeseries):
    result = []
    for value in timeseries:
        result.append((value - min(timeseries)) / (max(timeseries) - min(timeseries)))
    return result


if __name__ == "__main__":
    run = 1
    target_fitness = 10000

    while run < 100:

        print "==================== RUN %s ====================" % run

        starting_genome = decode('Experiments/CryogenicStorage/prophet_genome.json')
        population = Population(starting_genome)

        best_fitness = 0
        generation = 1
        last_improvement = 0

        archive = "Experiments/Archive/prophet/%s" % datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
        os.makedirs(archive)
        archive_population(population, generation)

        timeline_path = "%s/timeline.txt" % archive
        timeline = open(timeline_path, "w")

        ftse100_data = decode('Experiments/Vault/ftse100-2013-14.json')
        ftse100 = []
        volume = []
        for quote in ftse100_data["query"]["results"]["quote"]:
            ftse100.append(float(quote["Close"]))
            volume.append(float(quote["Volume"]))

        ftse100.reverse()
        volume.reverse()

        ftse100_pct = []

        for index, value in enumerate(ftse100):
            if index == 0:
                ftse100_pct.append(0)
            else:
                ftse100_pct.append((ftse100[index] - ftse100[index - 1]) / ftse100[index - 1])

        ftse100_n = min_max_normalize(ftse100)
        volume_n = min_max_normalize(volume)

        ftse100_t1 = [ftse100_n[0]]
        ftse100_t1.extend(ftse100_n[:len(ftse100_n) - 1])

        ftse100_t2 = [ftse100_n[0], ftse100_n[0]]
        ftse100_t2.extend(ftse100_n[:len(ftse100_n) - 2])

        ftse100_t3 = [ftse100_n[0], ftse100_n[0], ftse100_n[0]]
        ftse100_t3.extend(ftse100_n[:len(ftse100_n) - 3])

        volume_t1 = [volume_n[0]]
        volume_t1.extend(volume_n[:len(ftse100_n) - 1])

        try:

            money = 1000
            shares = 0

            for index, quote in enumerate(ftse100):
                today = quote
                tomorrow = ftse100[min(index + 1, len(ftse100) - 1)]

                if tomorrow > today:
                    if money > 0:
                        shares = money / ftse100[index]
                        money = 0
                else:
                    if shares > 0:
                        money = shares * ftse100[index]
                        shares = 0

            print "Buy and hold: %s" % ((1000 / ftse100[0]) * ftse100[len(ftse100) - 1])

            print "Best possible result: %s" % money if money > 0 else shares * ftse100[len(ftse100) - 1]

            while True:

                for genome in population.organisms:
                    genome["champ"] = None
                    brain = NeuralNetwork.expressed_from(genome)

                    money = 1000
                    shares = 0

                    try:
                        for index, quote in enumerate(ftse100):
                            brain.stimulate([("S1", ftse100_t1[index]),
                                             ("S2", ftse100_t2[index]),
                                             ("S3", ftse100_t3[index]),
                                             ("S4", volume_t1[index])
                                             ])
                            brain.electrify()
                            prediction = brain.outputs()["O1"].activation()

                            if prediction > 0.75:
                                if money > 0:
                                    # shares = money / ftse100[max(0, index - 2)]  # cheat!
                                    shares = money * 0.995 / ftse100[index]
                                    money = 0
                            elif prediction < 0.25:
                                if shares > 0:
                                    # money = shares * ftse100[max(0, index - 2)]  # cheat!
                                    money = shares * 0.995 * ftse100[index]
                                    shares = 0

                        ending_balance = money if money > 0 else shares * ftse100[len(ftse100) - 1]
                        genome["fitness"] = ending_balance

                    except UnstableNetworkError:
                        genome["fitness"] = 0
                        genome["stability"] = "UNSTABLE"

                champ_species = population.max_fitness_species()
                champ = champ_species.max_fitness_organism()
                champ["champ"] = "Champion"

                if champ["fitness"] > best_fitness:
                    best_fitness = champ["fitness"]
                    last_improvement = 0
                else:
                    last_improvement += 1
                    if last_improvement > AGE_DROPOFF_THRESHOLD * 2:
                        print json.dumps(population.max_fitness_species().max_fitness_organism())
                        raise Exception("STAGNANT POPULATION")

                zoo = []
                for species in population.species:
                    zoo.extend(species.id for x in range(0, len(species.member_organisms)))

                last_species_id = 0

                population_map = ""
                generator = generate()
                species_character = generator.next()
                for sample in range(0, 100):
                    sampled_species_id = zoo[int(sample * (len(zoo) / 100))]
                    if sampled_species_id != last_species_id:
                        last_species_id = sampled_species_id
                        species_character = generator.next()
                    population_map += species_character
                snapshot = population_map + " : Generation %s -- Population: %s, Species: %s, Max Fitness: %s (%s)," % (
                    generation, len(population.organisms), len(population.species), champ["fitness"], champ["id"])

                print snapshot
                timeline.write(snapshot)
                timeline.write('\n')
                archive_population(population, generation)

                if best_fitness > target_fitness:
                    print json.dumps(population.max_fitness_species().max_fitness_organism())
                else:
                    population.EPOCH(generation)
                    generation += 1

        except Exception:
            run += 1
