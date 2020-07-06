#!/usr/local/bin/python3

# put your routing program here!

from sys import argv

from pprint import pprint

from utils import *

segments_file = "road-segments.txt"
gps_file = "city-gps.txt"
graph = make_connectivity_graph(segments_file)
gps_graph = make_gps_graph(gps_file)
populate_coords_for_empty(graph, gps_graph)

city1 = argv[1]
city2 = argv[2]
method = argv[3].lower()

def make_segment_search_move(fringe, end_city=None, gps_graph=None):
    if end_city is None:
        fringe_item = fringe[0]
        next_city = fringe_item['next_cities'].pop(0)
        connected_cities = get_connected_cities(graph, next_city)
        fringe.append(
            create_fringe_object(
                fringe_item['path']+(next_city,),
                connected_cities,
                0
            )
        )
        if not fringe_item['next_cities']:
            fringe.pop(0)
        return next_city

    #this uses gps heuristic
    fringe_item = fringe[0]
    current_city = fringe_item['path'][-1]
    base_slope = get_slope(gps_graph,current_city, end_city)
    move_index = 0
    min_diff = 99999
    for index, city in enumerate(fringe_item['next_cities']):
        current_diff = base_slope - get_slope(gps_graph, city, end_city)
        if current_diff < min_diff:
            min_diff = current_diff
            move_index = index

    next_city = fringe_item['next_cities'].pop(index)

    connected_cities = get_connected_cities(graph, next_city)
    fringe.append(
        create_fringe_object(
            fringe_item['path']+(next_city,),
            connected_cities,
            0
        )
    )

    return next_city


def segment_seach(graph, start_city_name, end_city_name):

    connected_cities = get_connected_cities(graph, start_city_name)
    fringe = [
        create_fringe_object(
            (start_city_name,),
            connected_cities,
            0
        ),
    ]
    continue_traversal = True if connected_cities else False
    solution_found = False
    moves = 0

    while continue_traversal:
        while not fringe[0]['next_cities']:
            fringe.pop(0)
        if fringe and fringe[0]['next_cities']:
            next_city = make_segment_search_move(
                fringe, end_city_name, gps_graph
            )
            moves += 1
            if next_city == end_city_name:
                continue_traversal = False
                solution_found = True
        else:
            continue_traversal = False
    # print("moves: ", moves)

    if solution_found:
        return fringe[-1]

def get_city_distance_from_graph(
    fringe_item, current_city_index, next_city_index
):
    current_city_name = fringe_item['path'][current_city_index]
    next_city_name = fringe_item['next_cities'][next_city_index]
    dist = fringe_item['distance'] + graph[current_city_name][
        next_city_name
    ]['distance']
    return dist

def get_speed(fringe_item, current_city_index, next_city_index):
    current_city_name = fringe_item['path'][current_city_index]
    next_city_name = fringe_item['next_cities'][next_city_index]
    segment = graph[current_city_name][
        next_city_name
    ]
    dist = fringe_item['distance'] + (
        segment['distance'] / float(segment['speed_limit'])
    )
    return dist

def best_milage(fringe_item, current_city_index, next_city_index):
    current_city_name = fringe_item['path'][current_city_index]
    next_city_name = fringe_item['next_cities'][next_city_index]
    segment = graph[current_city_name][
        next_city_name
    ]
    mil = get_milage(float(segment['speed_limit']))
    dist = fringe_item['distance'] + mil
    return dist

def traverse(fringe, end_city_name, func_to_use, gps_graph):
    weight1 = 8
    weight2 = 2
    if not fringe:
        #no moves remaining, returning
        return None, False
    fringe_item = None

    pop_list = []
    for index, fringe_item in enumerate(fringe):
        if not fringe_item['next_cities']:
            pop_list.append(index)
        if fringe_item['next_cities']:
            best_move = create_next_move_obj(
                index,(
                    func_to_use(
                        fringe_item, -1, 0
                    ) * weight1 + get_slope(
                        gps_graph,
                        fringe_item['path'][-1],
                        fringe_item['next_cities'][0],
                    ) * weight2
                )
                , 0
            )

    for pop in pop_list:
        fringe.pop(pop)

    for fringe_item_index, fringe_item in enumerate(fringe):
        if end_city_name in fringe_item['next_cities']:
            end_city_index = fringe_item['next_cities'].index(end_city_name)

            best_move = create_next_move_obj(
                fringe_item_index,
                (func_to_use(
                        fringe_item, -1, end_city_index
                    ) * weight1 + get_slope(
                        gps_graph,
                        fringe_item['path'][-1],
                        fringe_item['next_cities'][end_city_index],
                    ) * weight2
                ),
                end_city_index
            )

            #return reached true if final city reached
            return best_move, True

        for city_index, city in enumerate(fringe_item['next_cities']):
            next_move = create_next_move_obj(
                fringe_item_index,
                (func_to_use(
                    fringe_item, -1, city_index
                    ) * weight1 + get_slope(
                        gps_graph,
                        fringe_item['path'][-1],
                        fringe_item['next_cities'][city_index],
                    ) * weight2
                ),
                city_index
            )
            if (next_move['distance'] < best_move['distance']
                # and fringe_item['next_moves']
            ):
                best_move = next_move
    #return reached False as  final city not reached
    return best_move, False

def make_move_on_distance(fringe, next_move):
    fringe_item_index = next_move['fringe_item_index']
    distance = next_move['distance']
    next_move_index = next_move['next_move_index']

    fringe_item = fringe[fringe_item_index]
    next_city = fringe_item['next_cities'][next_move_index]
    connected_cities = get_connected_cities(graph, next_city)
    next_fringe_item = create_fringe_object(
        fringe_item['path']+(next_city,), connected_cities, distance
    )
    fringe.append(next_fringe_item)
    fringe_item['next_cities'].pop(next_move_index)
    if not fringe_item['next_cities']:
        fringe.pop(fringe_item_index)
    return next_fringe_item



def road_trip(graph, start_city_name, end_city_name, heuristic, gps_graph):
    if (end_city_name not in graph.keys()
        or start_city_name not in graph.keys()):
        return
    connected_cities = get_connected_cities(graph, start_city_name)
    fringe = [
        create_fringe_object(
            (start_city_name,),
            connected_cities,
            0
        ),
    ]
    continue_traversal = True if connected_cities else False
    solution_found = False
    moves = 0

    while continue_traversal:

        if heuristic == 1:
            #distance
            fn_to_use = get_city_distance_from_graph
        elif heuristic == 2:
            #speed
            fn_to_use = get_speed
        elif heuristic == 3:
            #speed
            fn_to_use = best_milage


        next_move, reached = traverse(
            fringe, end_city_name, fn_to_use, gps_graph
        )
        if not next_move:
            continue_traversal = False
            return
        #TODO remove fringe items when when no next move
        #DO above in make move case
        solution = make_move_on_distance(fringe, next_move)
        if reached:
            continue_traversal = False
            solution_found = True
        moves+=1

    #     if moves%500==0:
    #         print("moves: ", moves)
    # print("moves: ", moves)
    if solution_found:
        return solution

if method == 'segments':
    get_formatted_output_from_frige_item(
        graph, segment_seach(graph, city1, city2)
    )
elif method == 'distance':
    get_formatted_output_from_frige_item(
        graph, road_trip(graph, city1, city2, 1, gps_graph)
    )
elif method == 'time':
    get_formatted_output_from_frige_item(
        graph, road_trip(graph, city1, city2, 2, gps_graph)
    )
elif method == 'mpg':
    get_formatted_output_from_frige_item(
        graph, road_trip(graph, city1, city2, 3, gps_graph)
    )
