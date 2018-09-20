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
spacing = 20
block_size = 20
num_possible_values = 8

local_component = 1
global_component = 1
ideal = (global_component, local_component)
# -------------------------------------------------

possible_values = range(0,5)
pygame.init()
s = pygame.display.set_mode((spacing*grid_size,spacing*grid_size+80))
p_clock = pygame.time.Clock()

# Create the connected grid.
for x in range(grid_size):
    for y in range(grid_size):
            nodes[str((x,y))] = (n.node(x,y,random.randint(0,num_possible_values)))
for x in range(grid_size):
    for y in range(grid_size):
                for (a,b) in [(0,1),(1,0),(0,-1),(-1,0)]:
                    nodes[str((x,y))].neighbors.append( nodes[str(((x+a)%grid_size,(y+b)%grid_size))])

def func(the_list): return entropy(the_list)

def mean(the_list):
    return sum(the_list)/len(the_list)
def variance(the_list):
    m = mean(the_list)
    return sum([(x-m)**2 for x in the_list])
def entropy(the_list):
    dict = {}
    for item in the_list:
        if str(item) in dict: dict[str(item)] += 1
        else: dict[str(item)] = 1
    ps = [x/len(the_list) for x in dict.values()]
    ps = [x*math.log(x,2) for x in ps]
    return -sum(ps)

def draw_nodes():

    for v in nodes.values():
        for n in v.neighbors:
            pygame.draw.line(s, (90,90,90), (v.x*spacing+int(block_size/2), v.y*spacing+int(block_size/2)), \
                                    (n.x*spacing+int(block_size/2), n.y*spacing+int(block_size/2)), 1)
    for v in nodes.values():
        c = v.value * (255/len(possible_values))
        color = (c,c,c)
        pygame.draw.rect(s, color, (v.x*spacing, v.y*spacing, block_size, block_size), 0)


def set_nodes():
    new_values = {}
    for this_node in nodes.values():

        global_values = [n.value for n in list(filter(lambda x:x!=this_node, nodes.values()))]
        local_values = [n.value for n in this_node.neighbors]

        global_returns = [func(global_values+[pv]) for pv in possible_values]
        local_returns = [func(local_values+[pv]) for pv in possible_values]

        # Define a distance function.
        dist = lambda x,y: sum((x[i]-y[i])**2 for i in range(len(x)))

        possible_points = list(zip(global_returns, local_returns))
        #dists = [dist((0,0), (p[0]*ideal[0], p[1]*ideal[1])) for p in possible_points]
        dists = [p[0]*ideal[0]+p[1]*ideal[1] for p in possible_points]
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
        if global_component < 1:
            global_component += 0.1
        else:
            global_component = 1
    elif im.down(pygame.K_DOWN):
        if global_component > -1:
            global_component -= 0.1
        else: global_component = -1

    if im.down(pygame.K_RIGHT):
        if local_component < 1:
            local_component += 0.1
        else:
            local_component = 1
    elif im.down(pygame.K_LEFT):
        if local_component > -1:
            local_component -= 0.1
        else: local_component = -1

    if im.pressed(pygame.K_q):
        num_possible_values += 1
        for n in nodes.values():
            n.value = random.randint(0,num_possible_values)
    if im.pressed(pygame.K_a) and num_possible_values > 1:
        num_possible_values -= 1
        for n in nodes.values():
            n.value = random.randint(0,num_possible_values)
    possible_values = range(num_possible_values)

    if im.pressed(pygame.K_SPACE):
        for n in nodes.values():
            n.value = random.randint(0,num_possible_values)

    ideal = (global_component, local_component)
    pygame.draw.rect(s,(20,20,20),(0,0,spacing*grid_size*2,spacing*grid_size+80))

    draw_nodes()
    set_nodes()

    win_font = pygame.font.SysFont("Deja Vu", 40)
    s.blit(win_font.render("("+str(round(ideal[0],2))+", "+str(round(ideal[1],2))+")", 1, (255, 255, 255)), (10, spacing*grid_size+30))
    win_font = pygame.font.SysFont("Deja Vu", 15)
    s.blit(win_font.render("(GLOBAL, LOCAL)", 1, (200,200,200)), (10, spacing*grid_size+60))
    win_font = pygame.font.SysFont("Deja Vu", 20)
    s.blit(win_font.render(str(round(func([n.value for n in nodes.values()]),1)), 1, (200,200,200)), (130, spacing*grid_size+30))
    avg_func = sum([func([v.value for v in n.neighbors]) for n in nodes.values()]) / len(nodes.values())
    s.blit(win_font.render(str(round(avg_func,1)), 1, (200,200,200)), (130, spacing*grid_size+50))


    pygame.display.flip()
    p_clock.tick(30)
