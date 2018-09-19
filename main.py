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
import input_manager as im
import copy

nodes = {}

# ----------- Settings ----------------------------
grid_size = 10
spacing = 30
block_size = 30
possible_values = [0,1,2]

g_l_angle = 45
ideal = (math.sin(math.radians(g_l_angle)), math.cos(math.radians(g_l_angle)))
# -------------------------------------------------

pygame.init()
s = pygame.display.set_mode((spacing*grid_size,spacing*grid_size))
p_clock = pygame.time.Clock()

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

def draw_nodes():
    for v in nodes.values():
        for n in v.neighbors:
            pygame.draw.line(s, (90,90,90), (v.x*spacing+int(block_size/2), v.y*spacing+int(block_size/2)), \
                                    (n.x*spacing+int(block_size/2), n.y*spacing+int(block_size/2)), 1)
    for v in nodes.values():
        color = (v.value*50, v.value*50, v.value*50)
        pygame.draw.rect(s, color, (v.x*spacing, v.y*spacing, block_size, block_size), 0)
def set_nodes():
    new_values = {}
    for this_node in nodes.values():
        global_values = [n.value for n in list(filter(lambda x:x==this_node, nodes.values()))]
        local_values = [n.value for n in this_node.neighbors]

        global_returns = [variance(global_values+[pv]) for pv in possible_values]
        local_returns = [variance(local_values+[pv]) for pv in possible_values]

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

        new_values[str((this_node.x, this_node.y))] = possible_values[min_dist_index]

    # Now swap over the minimizing values.
    for key in new_values:
        nodes[key].value = new_values[key]

while True:

    # Track the keyboard changes.
    im.last_keys_down = copy.deepcopy( im.keys_down )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            im.keys_down[str(event.key)] = True
        elif event.type == pygame.KEYUP:
            im.keys_down[str(event.key)] = False

    if im.down(pygame.K_UP):
        g_l_angle = (g_l_angle+1) % 360
    elif im.down(pygame.K_DOWN):
        g_l_angle = (g_l_angle-1) % 360

    # Normalize the ideal vector.
    ideal = (math.sin(math.radians(g_l_angle)), math.cos(math.radians(g_l_angle)))
    ideal_len = math.sqrt(sum(x ** 2 for x in ideal))
    ideal = [x / ideal_len for x in ideal]

    pygame.draw.rect(s,(20,20,20),(0,0,500,500))

    draw_nodes()
    set_nodes()

    win_font = pygame.font.SysFont("Deja Vu", 40)
    s.blit(win_font.render(str(round(math.sin(math.radians(g_l_angle)),2))+", "+str(round(math.cos(math.radians(g_l_angle)),2)), 1, (255, 255, 255)), (0, 0))

    print(g_l_angle)

    pygame.display.flip()
    p_clock.tick(30)
