# For this assignment, green denotes start and end space/node.
# red represents obstacles generated at random
# yellow denotes the path taken to reach end from start
# grid is 40 by 40
from game2dboard import Board
import random
obstacle_list = []
population = []
p_size = 30
fitness = []
probability = 0.15


# ----------------------------------------Genetic Algorithm Functions---------------------------------------
def chromosome(start, end, size):         # generates a possible path. Not necessarily optimal. Real valued.
    c = [start]
    while start != end:
        previous = start
        rnd = random.choice([[start[0] - 1, start[1] - 1], [start[0] + 1, start[1] + 1], [start[0] - 1, start[1] + 1], [start[0] + 1, start[1] - 1], [start[0] - 1, start[1]],[start[0], start[1] - 1],[start[0] + 1, start[1]],[start[0], start[1] +1]])
        start = rnd
        if start in obstacle_list or start[0] < 0 or start[0] > size or start[1] < 0 or start[1] > size:
            start = previous
        elif start != previous:
            c.append(start)               # each point in path is a gene.
    return c


def create_population(start, end, size):
    for j in range(p_size):
        population.append(chromosome(start, end, size))


def evaluate_fitness(pop):
    for j in range(len(pop)):
        fitness.append(1/len(pop[j]))


def selection(fit):                             # select the fittest 2 for crossover
    fitness_copy = fit[:]
    max1 = max(fitness_copy)
    fitness_copy.remove(max1)
    max2 = max(fitness_copy)
    index = []
    for j in range(len(fit)):
        if fit[j] == max1 or fit[j] == max2:
            index.append(j)
    return index


def best(fit):
    b = max(fit)
    index = 0
    for j in range(len(fit)):
        if fit[j] == b:
            index = j
            break
    return index

def crossover(index, pop):                     # crossover point must be same element for both routes
    c1 = pop[index[0]]
    c2 = pop[index[1]]
    new_c1 = []
    new_c2 = []
    limit = 0
    possible_cuts = []
    if len(c1) > len(c2):
        limit = len(c2)
    else:
        limit = len(c1)
    for j in range(limit):
        if c1[j][0] == c2[j][0] and c1[j][1] == c2[j][1]:
            possible_cuts.append(j)
    cut = random.choice(possible_cuts)
    for j in range(cut):
        new_c1.append(c2[j])
        new_c2.append(c1[j])
    for j in range(cut, len(c1)):
        new_c1.append(c1[j])
    for j in range(cut, len(c2)):
        new_c2.append(c2[j])
    return new_c1, new_c2


def mutation(route, end, size):           # random resetting. reset the genes from a random point in the chromosome
    r = random.randint(1, len(route)-2)
    e = len(route) - 1
    while e != r:
        route.pop(e)
        e -= 1
    c = route
    start = route[len(route)-1]
    while start != end:
        previous = start
        rnd = random.choice([[start[0] - 1, start[1] - 1], [start[0] + 1, start[1] + 1], [start[0] - 1, start[1] + 1],
                             [start[0] + 1, start[1] - 1], [start[0] - 1, start[1]], [start[0], start[1] - 1],
                             [start[0] + 1, start[1]], [start[0], start[1] + 1]])
        start = rnd
        if start in obstacle_list or start[0] < 0 or start[0] > size or start[1] < 0 or start[1] > size:
            start = previous
        elif start != previous:
            c.append(start)
    return c


# ----------------------------------------------------------------------------------------------------------

# ----------------------------Main---------------------------------------------------------

start_row = int(input("Enter starting row: "))
start_column = int(input("Enter starting column: "))
start1 = [start_row, start_column]

end_row = int(input("Enter ending row: "))
end_column = int(input("Enter ending column: "))
end1 = [end_row, end_column]

# --------------------Adding Configurations to the Grid ----------------
Display = Board(40, 40)
Display.cell_size = 15
Display.cell_color = "white"
# ----------------------------------------------------------------------

# --Displaying Random Obstacles and storing obstacle coordinates in obstacle list-----------
obstacles = random.randint(200, 300)
for i in range(obstacles):
    row = random.randint(1, 39)
    col = random.randint(1, 39)
    if row != start_row and col != start_column and row != end_row and col != end_column:
        Display[row][col] = "obs.png"
        temp = [row, col]
        obstacle_list.append(temp)
# -------------------------------------------------------------------------------------------

# ----------------------------------- GA Process ---------------------------------------------
create_population(start1, end1, 40)           # start by creating a population of chromosomes
path = []
for z in range(20):                           # 50 generations
    print("Generation: " + str(z))
    evaluate_fitness(population)  # assign the fitness values
    print("Generation: " + str(z))
    ind = selection(fitness)  # select the fittest two chromosomes for crossing of genes
    print("Generation: " + str(z))
    n1, n2 = crossover(ind, population)
    boolean = 1
    rnd_int = 0
    while boolean:
        rnd_int = random.randint(0, len(population)-1)
        if rnd_int not in ind:
            break
    if z == 19:
        x = best(fitness)
        path.append(population[x])
        break
    y = population[rnd_int]
    population.clear()
    if random.random() < probability:                       # mutation on probability
        c3 = mutation(y, end1, 40)
        population.append(c3)
    population.append(n1)
    population.append(n2)
    for p in range(3, p_size):
        create_population(start1, end1, 40)
    fitness.clear()
    print("Generation: " + str(z))
print(path)
# --------------------------------------------------------------------------------------------
for counter in range(1, len(path[0])-1):
    Display[path[0][counter][0]][path[0][counter][1]] = "route.png"

Display[start_row][start_column] = "car.png"
Display[end_row][end_column] = "car.png"

Display.show()
#------------------------------------------Main Ends-----------------------------------------------------
