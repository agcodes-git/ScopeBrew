# Define a function f() over a set of numbers.
# Define a function which minimizes f() over a small set. Is f() minimized over the larger set?

# Is minimizing f() over a small set ever ambiguous?
# If it is, then the results on the big set will be complicated.

# Minimize variance locally.
# Maximize variance globally.

import pygame
import sys
import node as n
import math
import random

pygame.init()
s = pygame.display.set_mode((500,500))
p_clock = pygame.time.Clock()

nodes = {}
grid_size = 25

# Create the connected grid.
for x in range(grid_size):
    for y in range(grid_size):
            nodes[str((x,y))] = (n.node(x,y,random.randint(0,1)))


for x in range(grid_size):
    for y in range(grid_size):
                for (a,b) in [(0,1),(1,0),(0,-1),(-1,0)]:
                    nodes[str((x,y))].neighbors.append( nodes[str(((x+a)%grid_size,(y+b)%grid_size))])

def mean(the_list):
    return sum(the_list)/len(the_list)

def variance(the_list):
    m = mean(the_list)
    return sum([(x-m)**2 for x in the_list])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    pygame.draw.rect(s,(20,20,20),(0,0,500,500))

    spacing = 15
    block_size = 15

    # Draw the nodes and their connections.
    for v in nodes.values():
        for n in v.neighbors:
            pygame.draw.line(s, (90,90,90), (v.x*spacing+int(block_size/2), v.y*spacing+int(block_size/2)), \
                                    (n.x*spacing+int(block_size/2), n.y*spacing+int(block_size/2)), 1)
    for v in nodes.values():
        color = (v.value*50, v.value*50, v.value*50)
        pygame.draw.rect(s, color, (v.x*spacing, v.y*spacing, block_size, block_size), 0)

    new_values = {}
    for this_node in nodes.values():
        possible_values = [0,1,2]
        global_values = [n.value for n in list(filter(lambda x:x==this_node, nodes.values()))]
        local_values = [n.value for n in this_node.neighbors]

        global_returns = [variance(global_values+[pv]) for pv in possible_values]
        local_returns = [variance(local_values+[pv]) for pv in possible_values]

        ideal = (0.4, 1)

        # Normalize the ideal vector.
        ideal_len = math.sqrt(sum(x**2 for x in ideal))
        ideal = [x/ideal_len for x in ideal]

        # Define a distance function.
        dist = lambda x,y: sum((x[i]-y[i])**2 for i in range(len(x)))

        # Normalize the acquired vectors.
        possible_points = list(zip(global_returns, local_returns))
        possible_points = [(0,0) if (a==0 and b==0) else (a/math.sqrt(a**2+b**2), b/math.sqrt(a**2+b**2)) for (a,b) in possible_points]

        # Get the list of distances.
        dists = [dist(ideal, p) for p in possible_points]

        # This index also the index for the possible value that minimizes the distance between the
        # actual point (global, local) and the ideal.
        min_dist_index = dists.index(min(dists))

        if random.random() > 0: new_values[str((this_node.x, this_node.y))] = possible_values[min_dist_index]
        else: new_values[str((this_node.x, this_node.y))] = this_node.value

    # Now swap over the minimzing values.
    for key in new_values:
        nodes[key].value = new_values[key]

    pygame.display.flip()
    p_clock.tick(60)
