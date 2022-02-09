import random


# Seed random number generator
random.Random(12092021)


class Chromosome:

    # Initialize class
    def __init__(self):
        self.cells = []
        self.fitness = 0
        self.distance = 2.0

    # Randomly generate the distance and spin cells
    def init_cells(self, input_distance):
        spin = [-1, 0, 1]
        self.distance = input_distance
        dist = random.uniform(2.0, (25.00 - self.distance))
        self.cells.append(dist)
        self.cells.append(dist + self.distance)
        self.cells.append(spin[int(random.uniform(0, 3))])

    # Generate cell based on given values, typically from two parents
    def birth_cell(self, values):
        new_value = values[0] - self.distance
        self.cells.append(new_value)
        self.cells.append(values[0])
        self.cells.append(values[1])

    # Generates a new value, and checks for possible required swapping
    def mutate_value(self, gene):
        if gene == 0:
            dist = random.uniform(2.0, (25.00 - self.distance))
            self.cells[0] = dist
            self.cells[1] = dist + self.distance
        elif gene == 2:
            self.cells.append(int(random.uniform(0, 3) - 1))

    # Return cell list
    def get_cells(self):
        return self.cells

    # Handles fitness function
    def fitness_function(self, data):
        trigger = False
        num_triggered = 0
        for i in range(0, len(data)):
            # Check distance
            if (self.cells[0] < data[i][0]) and (data[i][0] < self.cells[1]):
                # Check spin
                if (self.cells[2] == int(data[i][1])):
                    trigger = True
                    num_triggered += 1
                    self.fitness += data[i][2]
        # Ignore data if no data fits (this shouldn't happen, but just in case)
        if not trigger:
            self.fitness = -5000
        # Represent fitness as mean rather than summation
        else:
            self.fitness /= num_triggered

    # Return fitness value
    def get_fitness(self):
        return self.fitness
