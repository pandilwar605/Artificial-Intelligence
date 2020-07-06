from pprint import pprint

def make_connectivity_graph(segments_file):
    graph = {}
    with open(segments_file, "r") as f:
        for index, line in enumerate(f.readlines()):
            cleaned_data = line.strip().split()
            city1 = cleaned_data[0]
            city2 = cleaned_data[1]
            length = int(cleaned_data[2])
            speed = int(cleaned_data[3])
            highway = cleaned_data[4]
            #p = line.strip().split(" ")

            value = {
                'distance': length,
                'speed_limit': speed,
                'freeway name': highway
            }

            if city1 not in graph:
                graph[city1] = {city2: value}
            else:
                graph[city1][city2] = value

            if city2 not in graph:
                graph[city2] = {city1: value}
            else:
                graph[city2][city1] = value

    return graph

def make_gps_graph(gps_file):
    gps_graph = {}
    with open(gps_file, 'r') as f:
        for line in f.readlines():
            town, lat, lon = line.split()
            gps_graph[town] = {'lat': float(lat), 'lon': float(lon)}
    return gps_graph

def populate_coords_for_empty(connectivity_graph, gps_graph):
    for town, connections in connectivity_graph.items():
        if town not in gps_graph.keys():
            gps_graph[town] = make_up_gps_co_ordinates(
                town,connections, gps_graph
            )

def make_up_gps_co_ordinates(town, connections, gps_graph):
    weight_sum = 0
    lat,lon = .0, .0
    for key, value in connections.items():
        distance=value['distance']
        weight_sum+=distance
        try:
            # print(gps_graph[key]['lat'], gps_graph[key]['lon'], distance)
            lat+=gps_graph[key]['lat']*distance
            lon+=gps_graph[key]['lon']*distance
        except KeyError as k:
            pass
    return {'lat':lat, 'lon':lon}


def get_connected_cities(graph, city):
    return sorted(graph[city].keys())


def create_fringe_object(path, next_cities, distance):
    refined_move_list = []
    for move in next_cities:
        if move not in path:
            refined_move_list.append(move)

    return {
        'path': path,
        'distance': distance,
        'next_cities': refined_move_list
    }

def create_next_move_obj(fringe_item_index, distance, next_move_index):
    return {
        'fringe_item_index': fringe_item_index,
        'distance': distance,
        'next_move_index': next_move_index
    }

def get_milage(vel):
    return 8*float(vel)/3*(1-(vel/float(150)))**4

def get_params(path, connectivity_graph):
    distance = 0
    hours = 0
    for index in range(len(path)-1):
        connection_item = connectivity_graph[path[index]][path[index+1]]
        distance+=connection_item['distance']
        hours+=(connection_item['distance']/float(
                connection_item['speed_limit']
            )
        )
    return distance, hours

def get_slope(graph, city1, city2):

    return (
        (float(graph[city2]['lon']) - float(graph[city1]['lon']))/
        ((float(graph[city2]['lat']) - float(graph[city1]['lat']))+(1e-10))
    )



def get_formatted_output_from_frige_item(connectivity_graph, fringe_item):
    if not fringe_item:
        pprint("Inf")
        return

    total_segments = len(fringe_item['path'])
    total_miles, total_hours = get_params(
        fringe_item['path'], connectivity_graph
    )
    total_gas_gallon = total_miles/get_milage(total_miles/total_hours)
    path_string = " ".join(fringe_item['path'])

    print("{segments} {miles} {hours}"
        " {gas_gallon} {path_string}".format(
            segments=total_segments,
            miles=total_miles,
            hours=total_hours,
            gas_gallon=total_gas_gallon,
            path_string=path_string,
        )
    )


def tp():
    # example cases
    '"Y"_City,_Arkansas' 'Red_Chute,_Louisiana'
