from chromosome import Chromosome
import random


class Generation:

    def __init__(self):
        self.chromosomes = []
        self.c_dic = {}
        self.mutation_rate = 0

    # Add chromosomes created by previous generation, if applicable
    def import_chromosomes(self, chromosomes):
        self.chromosomes = chromosomes
        self.c_dic.clear()

    # Used to take mutation rate from previous generation
    def import_mutation(self, mutation_rate):
        self.mutation_rate = mutation_rate

    # Create and initialize cells, typically used by first generation
    def create_cells(self, amount, input_distance):
        for i in range(0, int(amount)):
            self.chromosomes.append(Chromosome())
            self.chromosomes[i].init_cells(input_distance)

    # Generate fitness amount for each chromosome
    def run_fitness(self, data):
        for i in range(0, len(self.chromosomes)):
            self.chromosomes[i].fitness_function(data)
            self.c_dic[self.chromosomes[i].get_fitness()] = self.chromosomes[i]

    def selection(self, algorithm, percent):
        selected_chromosomes = []
        sorted_chromosomes = []
        cut = int(float(percent) * float(len(self.chromosomes)))
        for i in sorted(self.c_dic):
            sorted_chromosomes.append(self.c_dic[i])
        # Select top <percent> portion of chromosomes
        if algorithm.lower() == 'elitest':
            low_bound = len(selected_chromosomes) - cut
            selected_chromosomes = sorted_chromosomes[low_bound:]
            return selected_chromosomes
        # Run tournaments to select top <percent> portion of chromosomes
        elif algorithm.lower() == 'tournament':
            while(len(selected_chromosomes) != cut):
                rand_one = random.uniform(0, len(sorted_chromosomes))
                rand_two = random.uniform(0, len(sorted_chromosomes))
                winner = max(rand_one, rand_two)
                selected_chromosomes.append(sorted_chromosomes[int(winner)])
                del sorted_chromosomes[int(winner)]
            return selected_chromosomes
        else:
            self.raise_error('selection')

    # Generate remaining amount of children required
    def crossover(self, algorithm, selected):
        amount = len(self.chromosomes) - len(selected)
        children = []
        # Run until required amount of children are generated
        while (len(children) != amount):
            # Select two parents at random
            r1 = random.uniform(0, len(selected))
            r2 = random.uniform(0, len(selected))
            cell_values = []
            # Create children based on selected algorithm
            if algorithm.lower() == 'uniform':
                # Randomly select from genes of parent
                for i in range(1, 3):
                    select = random.uniform(0, 2)
                    if int(select) == 0:
                        cell_values.append(selected[int(r1)].get_cells()[i])
                    else:
                        cell_values.append(selected[int(r2)].get_cells()[i])
            elif algorithm.lower() == 'kpoint':
                # Select genes based on specific parents
                for i in range(1, 3):
                    if (i == 1):
                        cell_values.append(selected[int(r1)].get_cells()[i])
                    else:
                        cell_values.append(selected[int(r2)].get_cells()[i])
            else:
                self.raise_error('crossover')
            children.append(Chromosome())
            children[-1].birth_cell(cell_values)
        return children

    # Offer the chance of variability by mutating genes to new values
    def mutation(self, mutation_init, mutation_delta, next_gen):
        self.mutation_rate = float(mutation_init)
        # Scroll through first four genes in each chromosome
        for i in range(0, len(next_gen)):
            for j in range(0, len(next_gen[i].get_cells()) - 1):
                mutate_check = random.uniform(1, int(self.mutation_rate*100))
                if (int(mutate_check) == 1):
                    next_gen[i].mutate_value(j)
        return next_gen
        # Determine if the mutation rate remains fixed, or is changed
        if str(mutation_delta.lower()) != 'false':
            self.mutation_rate -= (self.mutation_rate * mutation_delta)

    def get_mutation(self):
        return self.mutation_rate

    def raise_error(err):
        raise IOError('Problem with ' + err + ' algorithm- ' /
                      'please check config.txt file')

    # Displays minimum, maximum, and average fitness values
    def display_stats(self):
        fitness_amounts = []
        max_amount = 0
        max_chromosome = None
        for i in range(0, len(self.chromosomes)):
            if (max_amount < self.chromosomes[i].get_fitness()):
                max_amount = self.chromosomes[i].get_fitness()
                max_chromosome = self.chromosomes[i]
            fitness_amounts.append(self.chromosomes[i].get_fitness())
        fitness_amounts.sort()
        print('Best performing fitness = ' + str(fitness_amounts[-1]))
        print('Highest performing chromosome: ' +
              str(max_chromosome.get_cells()) + '\n')
