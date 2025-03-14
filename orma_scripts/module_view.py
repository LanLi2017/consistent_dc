# decomposition
# serial - parallel
import json
from orma import generate_dot, get_schema_list, translate_operator_json_to_graph
from extra_info import generate_recipe as gen_recipe

def dfs(graph, u):
    visited_nodes = [u]
    try:
        for v in graph[u]:
            visited_nodes += dfs(graph, v)
    except KeyError:
        pass
    return visited_nodes


def write_linked_dep(edges):
    # this will return dictionary: {node: [dependent nodes]}
    # we only care the nodes with different name but linked together
    neighbors_of = {}
    nodes = set()
    for edge in edges:
        u = edge['from']
        len_u = len(u)
        v = edge['to']
        len_v = len(v)
        if len_u == 1 and len_v == 1:
            u = u[0]['col_name']
            v = v[0]['col_name']
            nodes.add(u)
            nodes.add(v)
            # if u != v:
            # Add edge u->v and u->v
            neighbors_of.setdefault(u, []).append(v)
            neighbors_of.setdefault(v, []).append(u)

        elif len_v > 1:
            u = u[0]['col_name']
            nodes.add(u)
            for output in v:
                nodes.add(output['col_name'])
                # if output['col_name'] != u:
                neighbors_of.setdefault(u, []).append(output['col_name'])
                neighbors_of.setdefault(output['col_name'], []).append(u)
        elif len_u > 1:
            v = v[0]['col_name']
            nodes.add(v)
            for input_node in u:
                nodes.add(input_node['col_name'])
                # if input_node['col_name'] != v:
                neighbors_of.setdefault(input_node['col_name'], []).append(v)
                neighbors_of.setdefault(v, []).append(input_node['col_name'])
    return neighbors_of, nodes


def find_component(neighbors_of, u, component=None):
    if component is None:
        component = {u}
    for v in neighbors_of[u]:
        if v in component:
            continue
        component.add(v)
        find_component(neighbors_of, v, component)
    return component


def cluster_main(project_id):
    json_data, schema_info = gen_recipe(project_id)
    schemas = get_schema_list(schema_info)
    orma_data = translate_operator_json_to_graph(json_data, schemas)
    new_edges = []
    for graph in orma_data:
        new_edges += [{'from': graph.in_node_names, 'to': graph.out_node_names}]

    neighbors_of, nodes = write_linked_dep(new_edges)
    components = []
    visited_nodes = set()
    for u in nodes:
        if u in visited_nodes:
            continue
        component = find_component(neighbors_of, u)
        components.append(component)
        visited_nodes |= component
    del visited_nodes

    return components


def split_recipe(project_id=2124203262743, output_gv='../usecase2/modular_views/module_view'):
    # how to define subworkflow:
    # same input or same output
    components = cluster_main(project_id)

    json_data, schema_info = gen_recipe(project_id)
    schemas = get_schema_list(schema_info)
    orma_data = translate_operator_json_to_graph(json_data, schemas)

    clusters = []
    for component in components:
        cluster = []
        for i, graph in enumerate(orma_data):
            in_nodes = []
            for in_node in graph.in_node_names:
                in_nodes.append(in_node['col_name'])
            in_nodes_set = set(in_nodes)
            common_flag = in_nodes_set.intersection(set(component))
            if common_flag:
                cluster.append(i)
            else:
                pass
        clusters.append(cluster)

    operators = [graph.raw_operator for graph in orma_data]
    counter = 0
    for cluster_list in clusters:
        json_res = []
        cluster_schemas = []
        if not cluster_list:
            pass
        else:
            for index in cluster_list:
                json_res.append(operators[index])
                cluster_schemas.append(schemas[index])
        if json_res:
            with open(f'{output_gv}_{counter}.json', 'w')as f:
                json.dump(json_res, f, indent=4)
            # output_gv = f'{output_gv}_{counter}'
            orma_g = generate_dot(json_res, cluster_schemas, f'{output_gv}_{counter}')
            orma_g.view()
            counter += 1
        else:
            pass