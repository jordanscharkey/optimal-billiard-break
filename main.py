from generations import Generation


# GLOBAL VARIABLES #
filename = 'default-testing-data.txt'        # '$FILENAME'
chromosome_amount = 30             # Amount of possible data configurations
generation_amount = 1000             # Amount of loops to conduct
selection_algorithm = 'elitest'      # 'tournament' or 'elitest'
crossover_algorithm = 'uniform'     # 'uniform' or 'kpoint'
generation_percentage = 0.25        # Top X% to take into consideration
mutation_rate = 0.05               # Probability of mutating
dynamics = False                    # False or float of percent to change
distance_range = 2.0                # Range of values to look for


# Reads through data file to return desired values
def parse_data(unparsed_data):
    parsed_data = unparsed_data
    for i in range(0, len(parsed_data)):
        if '\t' in parsed_data[i]:
            parsed_data[i] = parsed_data[i].split('\t')
        elif ' ' in parsed_data[i]:
            parsed_data[i] = parsed_data[i].split(' ')
        for j in range(0, len(parsed_data[i])):
            parsed_data[i][j] = parsed_data[i][j].replace('\n', '')
            parsed_data[i][j] = parsed_data[i][j].replace('\r', '')
            parsed_data[i][j] = float(parsed_data[i][j])
    return parsed_data


# Correctly read/parse config and data files
data_file = open(filename, 'r+')
data = parse_data(data_file.readlines())

# Initialize generation one
cur_gen = Generation()
cur_gen.create_cells(chromosome_amount, distance_range)

# Begin algorithm
for i in range(1, int(generation_amount) + 1):
    cur_gen.run_fitness(data)
    # Uncomment to check progress every 10th generation
    # if i % 10 == 0:
    #   print('\n### Generation ' + str(i) + ' Information ###')
    #   cur_gen.display_stats()
    sel = cur_gen.selection(selection_algorithm, generation_percentage)
    cross = cur_gen.crossover(crossover_algorithm, sel)
    fresh_chromosomes = sel + cross
    next_gen = cur_gen.mutation(mutation_rate, dynamics, fresh_chromosomes)
    mu = cur_gen.get_mutation()
    cur_gen = Generation()
    cur_gen.import_chromosomes(next_gen)
    cur_gen.import_mutation(mu)

# Display final set of information
print('\n\n### Final Generation Information ###')
cur_gen.run_fitness(data)
cur_gen.display_stats()
