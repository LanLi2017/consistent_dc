from graphviz import Digraph

from extra_info import generate_recipe as gen_recipe
# from extra_info import generate_recipe as gen_recipe
# import all library needed for this class
import re
from collections import Counter
from pprint import pprint

from orma import ORMAGraph

# TASK 3: Create a table_view of data cleaing workflow
def table_view(project_id, combined=False):
    json_data, schema_info = gen_recipe(project_id)
    table_view_data = []
    for i, operator in enumerate(json_data, start=1):
        graph = ORMAGraph()  # graph includes nodes and edges
        graph.raw_operator = operator
        graph.step_index = i
        graph.history_id = operator['id']
        prev_table = f'table{i - 1}'
        cur_table = f'table{i}'

        if 'op' in [*operator]:
            if operator['op'] == 'core/column-addition':  # merge operation
                colname = f'col-name "{operator["baseColumnName"]}"'
                newColumnName = f'newColumnName "{operator["newColumnName"]}"'
                grelexp = f'expression "{operator["expression"].split(":")[-1]}"'

                insertpos = f'InsertPosition "{operator["columnInsertIndex"]}"'  # physical position
                graph.process = [f'({i}) column-addition']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname,
                        newColumnName,
                        grelexp,
                        insertpos
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]

            elif operator['op'] == 'core/column-split':  # split operation
                colname = f'col-name  "{operator["columnName"]}"'
                separator = f'separator "{operator["separator"]}"'
                remove = f'removeOriginalColumn "{operator["removeOriginalColumn"]}"'
                graph.process = [f'({i}) column-split']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname,
                        separator,
                        remove
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]

            elif operator['op'] == 'core/column-rename':  # split operation
                oldColumnName = f'oldColumnName "{operator["oldColumnName"]}"'
                newColumnName = f'newColumnName "{operator["newColumnName"]}"'
                graph.process = [f'({i}) column-rename']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        oldColumnName,
                        newColumnName
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]

            elif operator['op'] == 'core/column-removal':
                colname = f'col-name "{operator["columnName"]}"'
                graph.process = [f'({i}) column-removal']

                if not combined:
                    graph.in_node_names += [
                        prev_table,
                    ]
                    # TODO
                    # port is needed to represent null
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname,
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]

            elif operator['op'] == 'core/column-addition-by-fetching-urls':
                colname = f'col-name "{operator["baseColumName"]}"'
                newColumnName = f'newColumnName "{operator["newColumName"]}"'
                urlExpression = f'urlExpression "{operator["urlExpression"].split(":")[-1]}"'
                graph.process = [f'({i}) column addition-by-fetching-urls']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname,
                        newColumnName,
                        urlExpression
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]

            elif operator['op'] == 'core/multivalued-cell-join':
                colname = f'col-name "{operator["columName"]}"'
                keyColumnName = f'keyColumnName "{operator["keyColumnName"]}"'
                separator = f'separator "{operator["separator"]}"'

                graph.process = [f'({i}) multivalued-cell-join']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname,
                        keyColumnName,
                        separator
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]

            elif operator['op'] == 'core/transpose-columns-into-rows':
                colname = f'col-name "{operator["startColumnName"]}"'
                columnCount = f'columnCount "{operator["columnCount"]}"'
                combinedColumnName = f'combinedColumnName "{operator["combinedColumnName"]}"'
                separator = f'separator "{operator["separator"]}"'

                graph.process = [f'({i}) transpose-columns-into-rows']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname,
                        columnCount,
                        combinedColumnName,
                        separator
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]

            elif operator['op'] == 'core/row-removal':
                colname = f'col-name "{operator["engineConfig"]["facets"][0]["columnName"]}"'
                expression = f'expression "{operator["engineConfig"]["facets"][0]["expression"].split(":")[-1]}"'

                graph.process = [f'({i}) row-removal']

                if not combined:
                    graph.in_node_names += [
                        prev_table,
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname,
                        expression
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]

            elif operator['op'] == 'core/column-move':
                colname = f'col-name "{operator["columnName"]}"'
                index = operator["index"]

                graph.process = [f'({i}) Move_to #{index}']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname,
                        index
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]

            elif operator['op'] == 'core/mass-edit':
                colname = f'col-name "{operator["columnName"]}"'
                graph.process = [f'({i}) mass-edit']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
            elif operator['op'] == 'core/multivalued-cell-split':
                colname = f'col-name "{operator["columnName"]}"'
                keyColumnName = f'keyColumnName {operator["keyColumnName"]}'
                mode = f"mode {operator['separator']}"
                separator = f'separator "{operator["separator"]}"'
                regex = f'"regex {operator["regex"]}"'
                graph.process = [f'({i}) multivalued-cell-split']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname,
                        keyColumnName,
                        mode,
                        separator,
                        regex
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
            elif operator['op'] == 'core/recon':
                colname = operator['columnName']
                graph.process = [f'({i}) reconciliation']
                recon_id = operator['config']['type']['id']
                columns = []
                mode = operator['config']['mode']
                if operator['config']['columnDetails']:
                    columns = operator['config']['columnDetails'][0]['column']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        colname,
                        recon_id,
                        columns,
                        mode
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]

            else:  # normal unary operation
                try:
                    expression = operator['expression']
                    exp_preprocess = expression.split(".")[0]
                    column_name = operator['columnName']
                    if exp_preprocess == 'value':
                        graph.process = [f'({i}) .{expression.split(".")[-1]}']
                    else:
                        # value change
                        graph.process = [f'({i}) {expression.split(":")[-1]}']
                    colname = f'col-name "{column_name}"'
                    if not combined:
                        graph.in_node_names += [
                            prev_table
                        ]
                        graph.out_node_names += [
                            cur_table
                        ]
                    else:
                        graph.in_node_names += [
                            prev_table,
                            colname
                        ]
                        graph.out_node_names += [
                            cur_table
                        ]

                except KeyError:
                    graph.process = [f'({i}) {operator["op"].split("/")[-1]}']
                    graph.in_node_names += [
                        prev_table,
                        # colname,
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
            # graph.edge += [{'from': graph.in_node_names, 'to': graph.process},
            #                {'from': graph.process, 'to': graph.out_node_names}]
            # table_view_data.append(graph)

        else:
            description = operator['description'].split(' ')
            if 'column' in description:
                # single edit
                column_name = f'col-name "{description[-1]}"'
                desc = operator['description']
                row_number = desc.split(",")[0].split(" ")[-1]
                process = f'single_cell_edit row #{row_number}'
                graph.process = [f'({i}) {process}']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        column_name,
                        row_number
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
            else:
                # Star/flag row 1
                desc = operator['description']
                row_number = desc.split(" ")[-1]
                process = f'{"_".join(desc.split(" ")[:2])} #{row_number}'
                graph.process = [f'({i}) {process}']
                if not combined:
                    graph.in_node_names += [
                        prev_table
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
                else:
                    graph.in_node_names += [
                        prev_table,
                        row_number
                    ]
                    graph.out_node_names += [
                        cur_table
                    ]
        graph.edge += [{'from': graph.in_node_names, 'to': graph.process},
                       {'from': graph.process, 'to': graph.out_node_names}]
        table_view_data.append(graph)

    return table_view_data


def get_node_from_table_view(orma_data):
    mixed_nodes = []
    data_nodes = []  # nodes include data node
    params_nodes = []
    for graph in orma_data:
        mixed_nodes += graph.in_node_names
        mixed_nodes += graph.out_node_names

    pattern = re.compile(r'(table)\d+')
    for nodes in mixed_nodes:
        if pattern.match(nodes):
            data_nodes.append(nodes)
        else:
            params_nodes.append(nodes)
    return data_nodes, params_nodes


def generate_table_dot(project_id=2124203262743, output='output/table_view.gv', combined=False):
    # data node: #FFFFCC
    # process: #CCFFCC
    table_view_data = table_view(project_id, combined)
    feature_data = {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': _color_, 'peripheries': '1',
                    'fontname': 'Helvetica'}
    tableview_dot = Digraph('ORMA-Table-View', filename=output)
    tableview_dot.graph_attr['ranksep'] = '0.2'
    data_nodes, params_nodes = get_node_from_table_view(table_view_data)
    edges = get_edge_from_ormadata(table_view_data)
    tableview_dot.attr('node', shape=feature_data['shape'], style=feature_data['style'],
                       fillcolor=feature_data['fillcolor'])
    for node_item in data_nodes:
        # data node: in_node & out_node
        tableview_dot.node(node_item)

    # parameter nodes
    tableview_dot.attr('node', shape=feature_data['shape'], style=feature_data['style'],
                       fillcolor=_inNodeColor_)
    for params in params_nodes:
        tableview_dot.node(params)

    tableview_dot.attr('node', shape=feature_data['shape'], style='filled', fillcolor=_process_color_,
                       peripheries='1', fontname='Helvetica')
    for graph in table_view_data:
        # process node
        process_node = graph.process[0]
        tableview_dot.node(process_node)  # update process node

    for edge in edges:
        from_node = edge['from']
        to_node = edge['to']
        if len(from_node) == 1 and len(to_node) == 1:
            tableview_dot.edge(from_node[0], to_node[0])

        if len(from_node) == 1 and len(to_node) > 1:
            for to_item in to_node:
                tableview_dot.edge(from_node[0], to_item)

        if len(from_node) > 1 and len(to_node) == 1:
            for from_item in from_node:
                tableview_dot.edge(from_item, to_node[0])

    tableview_dot.view()
    return tableview_dot
