# version of data flow
import argparse
import ast
import json
from graphviz import Digraph

from extra_info import generate_recipe as gen_recipe
import re
from collections import Counter
from pprint import pprint

_color_ = '#FFFFCC'  # default color for output node
_inNodeColor_ = '#FAFAF0'  # default color for input node
_process_color_ = '#CCFFCC'
# _level3_color_ = '#ffc04d'  # if the transformation is column-level
# _level0_color = '#D0D0D0'  # if the transformation is single-edit/ star row
_edge_color_ = '#000000'  # default edge color: black
_gen_val_color_ = '#f7ce8d'  # generic + value changed
_type_con_color_ = '#d4eafa'  # type convert color
_type_label_color_ = '#14697e'  # type convert label color
_custome_v_color = '#fbb8b8'  # customized value color
_gen_label_color_ = '#b06e04'  # generic + value label color
_remove_color_ = '#D0D0D0'  # color for removing cells

'''
if style: must label & edge color
if label: must edge color

'''

class ORMAGraph:
    def __init__(self):
        # SQL
        self.history_id = 0
        self.step_index = 0
        self.out_node_names = []
        self.in_node_names = []
        self.process = []
        self.raw_operator = None
        self.edge = []  # from in_node_names -to-> process from process -to-> out_not_name
        self.level = None  # according to effect of operations, classify into three levels
        self.derived_columns = []
        self.d_edge = []  # save edges for derived columns


def extract_facet(operation, columns):
    '''
    Extract columns in facet for extending read_scope
    '''
    if 'engineConfig' in [*operation]:
        engineConfig = operation['engineConfig']
        facets = engineConfig['facets']
        read_cols = []
        # if facets not empty => soft derivation exists
        if not facets:
            read_cols = []
        else:
            for facet in facets:
                if facet['name'] in columns:
                    read_cols.append(facet['name'])
    else:
        read_cols = []
    return read_cols if read_cols else []


def merge_basename(operator, cur_cols):
    """
    return: read columns, separator
    """
    # Add-column:
    # two kinds of expressions:
    # 1. the column name has space: "grel:cells[\"Sponsor 2\"].value + cells[\"Sponsor 7\"].value"  : [A-Z]\w+ \d
    # 2. the column name does not have space: "grel:cells.name.value + cells.event.value" :   \.\w+\.
    # Join-column: 
    # "join ([coalesce(cells[...].value,''),coalesce(...),...)],'separator')"
    # 3. normal one: "grel:value"
    exp = operator['expression']
    # read-scope: operator['baseColumnName'] if basename is not in the expression 

    base_name = operator['baseColumnName']

    # Case 1: Handling `grel:if` expressions
    if 'grel:if' in exp:
        # Extract column names from `cells[...]`
        column_matches = re.findall(r"cells\[\"(.*?)\"\]\.value|cells\.(\w+)\.value", exp)
        
        # Flatten and filter out empty matches
        read_cols = list(set(col for match in column_matches for col in match if col in cur_cols))
        if base_name not in read_cols:
            read_cols.append(base_name)

        return read_cols, None

    # Case 2: Handling `join([coalesce(...)], 'separator')` expressions
    elif 'join (' in exp:
        match = re.search(r"join\s*\(\s*\[(.*?)\]\s*,\s*(.*?)\s*\)", exp)
        if match:
            columns_part = match.group(1)  # Extract coalesce() expressions
            separator_part = match.group(2)  # Extract separator

            # Extract column names from coalesce expressions
            column_matches = re.findall(r"cells\['(.*?)'\]", columns_part)
            read_cols = list(set(column_matches))
            if base_name not in read_cols:
                read_cols.append(base_name)

            # Convert separator to Python string (removing quotes)
            try:
                separator = ast.literal_eval(separator_part)
            except:
                separator = separator_part  # Fallback if parsing fails

            return read_cols, separator

    # Case 3: Handling concatenated column expressions (e.g., grel:cells.year.value + '-' + cells.month.value)
    elif "grel:" in exp:
        # Extract column names from both `cells.column.value` and `cells["column"].value`
        column_matches = re.findall(r"cells\.(\w+)\.value|cells\[\"(.*?)\"\]\.value", exp)

        # Flatten results and remove empty values
        read_cols = list(set(col for match in column_matches for col in match if col))

        # Extract possible separators (anything inside quotes)
        separator_matches = re.findall(r"['\"](.*?)['\"]", exp)
        separator = list(set(separator_matches)) if separator_matches else None 

        # Ensure base_name is included
        if base_name and base_name not in read_cols:
            read_cols.append(base_name)

        return read_cols, separator

    # Default case: No matches found, return empty list
    return [base_name], None


# column-dependency view
def translate_operator_json_to_graph(json_data, schemas):
    # json_data, schema_info = gen_recipe(project_id)
    # schemas = get_schema_list(schema_info)
    orma_data = []
    nodes_num_about_column = Counter()

    def get_column_current_node(column_name):
        if column_name not in nodes_num_about_column:
            node_name = f'{column_name}.v0'
            nodes_num_about_column[column_name] += 1
            return node_name
        else:
            node_id = nodes_num_about_column[column_name]

            return f"{column_name}.v{node_id - 1}"

    def create_new_node_of_column(column_name):
        nodes_num_about_column[column_name] += 1
        return get_column_current_node(column_name)

    for i, operator in enumerate(json_data, start=1):
        graph = ORMAGraph()  # graph includes nodes and edges
        graph.raw_operator = operator
        graph.step_index = i
        graph.history_id = operator['id']
        cur_schema = schemas[i]
        prev_schema = schemas[i - 1]
        # Type convert: toNumber/toDate
        # customize : cell-level/mass-edit
        # single-col: rename/remove
        # generic and multi-col/single-col: addition/split/transform
        if 'op' in [*operator]:
            if operator['op'] == 'core/column-addition':  # merge operation
                graph.process = [f'({i}) column-addition']
                read_cols, seperator = merge_basename(operator, cur_schema)
                for col in read_cols:
                    graph.in_node_names += [
                        {'col_name': col, 'label': f'{get_column_current_node(col)}'}  # column name: label[unique]
                    ]

                newcolumnName = operator['newColumnName']
                graph.out_node_names += [
                    {'col_name': newcolumnName, 'label': f'{create_new_node_of_column(newcolumnName)}',
                     'color': _color_}
                ]

            elif operator['op'] == 'core/column-split':  # split operation
                column_name = operator['columnName']
                graph.process = [f'({i}) column-split']
                remove_original_col = operator['removeOriginalColumn']
                graph.in_node_names += [
                    {'col_name': column_name, 'label': f'{get_column_current_node(column_name)}'}
                ]
                new_cols = list(set(cur_schema) - set(prev_schema))
                for col in new_cols:
                    graph.out_node_names += [
                        {'col_name': col, 'label': f'{create_new_node_of_column(col)}', 'color': _color_}
                    ]
                if remove_original_col:
                    remove_col = f'remove-{column_name}'
                    graph.out_node_names += [
                        {'col_name': remove_col, 'label': f'{create_new_node_of_column(remove_col)}',
                         'color': _remove_color_}
                    ]
                else:
                    pass

            elif operator['op'] == 'core/column-rename':  # split operation
                old = operator['oldColumnName']
                new = operator['newColumnName']
                graph.process = [f'({i}) column-rename']
                graph.in_node_names += [
                    {'col_name': old, 'label': f'{get_column_current_node(old)}'}
                ]
                graph.out_node_names += [
                    {'col_name': new, 'label': f'{create_new_node_of_column(new)}', 'color': _color_}
                ]

            elif operator['op'] == 'core/column-removal':
                graph.process = [f'({i}) removal']
                col = operator['columnName']
                lb_col = get_column_current_node(col)
                graph.in_node_names += [
                    {'col_name': col, 'label': f'{lb_col}'}
                ]
                # TODO which color?
                # port is needed to represent null
                new_col = f'remove-{col}'
                lb_new = create_new_node_of_column(new_col)
                graph.out_node_names += [
                    {'col_name': f'remove-{col}', 'label': f'{lb_new}', 'color': _remove_color_}
                ]

            elif operator['op'] == 'core/column-addition-by-fetching-urls':
                graph.process = [f'({i}) column addition-by-fetching-urls']
                base = operator['baseColumnName']
                new = operator['newColumnName']
                lb_base = get_column_current_node(base)
                lb_new = create_new_node_of_column(new)
                graph.in_node_names += [
                    {'col_name': base, 'label': f'{lb_base}'}
                ]
                graph.out_node_names += [
                    {'col_name': new, 'label': f'{lb_new}', 'color': _color_}
                ]

            elif operator['op'] == 'core/multivalued-cell-join':
                graph.process = [f'({i}) multivalued-cell-join']
                col = operator['columnName']
                lb_col = get_column_current_node(col)
                graph.in_node_names += [
                    {'col_name': col, 'label': f'{lb_col}'}
                ]
                graph.out_node_names += [
                    {'col_name': col, 'label': f'{create_new_node_of_column(col)}', 'color': _color_}
                ]

            elif operator['op'] == 'core/transpose-columns-into-rows':
                graph.process = [f'({i}) transpose-columns-into-rows']
                start = operator['startColumnName']
                combine = operator['combinedColumnName']
                graph.in_node_names += [
                    {'col_name': start, 'label': f'{get_column_current_node(start)}'}
                ]
                graph.out_node_names += [
                    {'col_name': combine, 'label': f'{create_new_node_of_column(combine)}', 'color': _color_}
                ]

            elif operator['op'] == 'core/row-removal':
                graph.process = [f'({i}) row-removal']
                cur_node = operator['engineConfig']['facets'][0]['name']
                new_node = operator['engineConfig']['facets'][0]['name']
                graph.in_node_names += [
                    {'col_name': cur_node, 'label': f'{get_column_current_node(cur_node)}'}
                ]
                graph.out_node_names += [
                    {'col_name': new_node, 'label': f'{create_new_node_of_column(new_node)}', 'color': _color_}
                ]

            elif operator['op'] == 'core/column-move':
                index = operator['index']
                graph.process = [f'({i}) Move_to #{index}']
                column_name = operator['columnName']
                graph.in_node_names += [
                    {'col_name': column_name, 'label': f'{get_column_current_node(column_name)}'}
                ]
                graph.out_node_names += [
                    {'col_name': column_name, 'label': f'{create_new_node_of_column(column_name)}', 'color': _color_}
                ]
            elif operator['op'] == 'core/mass-edit':
                graph.process = [f'({i}) mass-edit']
                column_name = operator['columnName']
                read_cols = extract_facet(operator, cur_schema) # add read scope of columns
                if column_name not in read_cols:
                    read_cols.append(column_name)
                
                for col in read_cols:
                    graph.in_node_names += [
                        {'col_name': col, 'label': f'{get_column_current_node(col)}'}
                    ]
                graph.out_node_names += [
                    {'col_name': column_name, 'label': f'{create_new_node_of_column(column_name)}',
                     'color': _color_}
                ]
            elif operator['op'] == 'core/recon':
                graph.process = [f'({i}) reconciliation']
                column_name = operator['columnName']
                graph.in_node_names += [
                    {'col_name': column_name, 'label': f'{get_column_current_node(column_name)}'}
                ]
                graph.out_node_names += [
                    {'col_name': column_name, 'label': f'{create_new_node_of_column(column_name)}',
                     'color':_color_}
                ]
            else:  # normal unary operation
                try:
                    # add read columns from facets information
                    expression = operator['expression']
                    exp = expression.split(':')[-1]
                    graph.process = [f'({i}) {exp}']
                    column_name = operator['columnName']
                    read_cols = extract_facet(operator, cur_schema)
                    if column_name not in read_cols:
                        read_cols.append(column_name)
                    for col in read_cols:
                        graph.in_node_names += [
                            {'col_name': col, 'label': f'{get_column_current_node(col)}'}
                        ]
                    graph.out_node_names += [
                        {'col_name': column_name, 'label': f'{create_new_node_of_column(column_name)}',
                            'color': _color_}
                    ]
                except KeyError:
                    continue
        else:
            description = operator['description'].split(' ')
            if 'column' in description:
                # single edit
                column_name = description[-1]
                desc = operator['description']
                row_number = desc.split(",")[0].split(" ")[-1]
                process = f'single_cell_edit row #{row_number}'
                graph.process = [f'({i}) {process}']
                graph.in_node_names += [
                    {'col_name': column_name, 'label': f'{get_column_current_node(column_name)}'}
                ]
                graph.out_node_names += [
                    {'col_name': column_name, 'label': f'{create_new_node_of_column(column_name)}',
                     'color': _color_}
                ]
            else:
                pass
        graph.edge += [{'from': graph.in_node_names, 'to': graph.process},
                       {'from': graph.process, 'to': graph.out_node_names}]

        orma_data.append(graph)
    return orma_data


def get_node_from_ormadata(orma_data):
    data_nodes = []  # nodes include data node
    for graph in orma_data:
        data_nodes += graph.in_node_names
        data_nodes += graph.out_node_names

    return data_nodes


def get_edge_from_ormadata(orma_data):
    edges = []
    # edge [color=red]; // so is this
    # main -> init [style=dotted];
    for graph in orma_data:
        edges += graph.edge
    return edges


def draw_edges(edges, orma_graph):
    # read and refine into edges in graph
    for i, edge in enumerate(edges):
        if not edge['from']:
            pass
        else:
            edge_from, edge_to = edge['from'], edge['to']
            # edge_from, edge_to, color_type = edge
            edge_from_update = ''
            edge_to_update = ''

            if isinstance(edge_from, dict):
                for key, value in edge_from.items():
                    if key == 'col_name':
                        pass
                    elif key == 'color':
                        pass
                    else:
                        edge_from_update = edge_from[key]
                assert isinstance(edge_to, str)
                edge_to_update = edge_to
                orma_graph.edge(edge_from_update, edge_to_update)
            elif isinstance(edge_to, dict):
                for key, value in edge_to.items():
                    if key == 'col_name':
                        pass
                    elif key == 'color':
                        pass
                    else:
                        edge_to_update = edge_to[key]
                assert isinstance(edge_from, str)
                edge_from_update = edge_from
                orma_graph.edge(edge_from_update, edge_to_update)
    return orma_graph


def refine_dot_name(node_name):
    return f'"{node_name}"'


def process_feature_orma(orma_data, orma_dot):
    feature = {'shape': 'box', 'color': _process_color_, 'style': 'filled', 'peripheries': '1',
               'fontname': 'Helvetica'}  # label/size/font/...
    for graph in orma_data:
        if not graph.process:
            pass
        else:
            process_node = graph.process[0]
            orma_dot.attr('node', shape=feature['shape'], style=feature['style'], fillcolor=feature['color'],
                          peripheries=feature['peripheries'], fontname=feature['fontname'])
            orma_dot.node(process_node)
    return orma_dot


def generate_dot(json_data, schemas, output):
    # default feature setting for data node
    # json_data, schema_info = gen_recipe(project_id)
    # schemas = get_schema_list(schema_info)
    orma_data = translate_operator_json_to_graph(json_data, schemas)
    feature_data = {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': '#FFFFCC', 'peripheries': 1,
                    'fontname': "Helvetica-BoldOblique"}
    orma_dot = Digraph('ORMA', filename=output)

    data_nodes = get_node_from_ormadata(orma_data)
    edges = get_edge_from_ormadata(orma_data)
    orma_dot.attr('node', shape=feature_data['shape'], style=feature_data['style'], fillcolor=feature_data['fillcolor'])

    # how to represent different node in the same graph
    # label is same, but node name is not
    for node_item in data_nodes:
        node_name = node_item['col_name']
        node_label = node_item['label']
        orma_dot.node(node_label, label=node_name)  # same label but different node name
    orma_dot = process_feature_orma(orma_data, orma_dot)

    res_edges = []
    for edge in edges:
        from_node = edge['from']
        to_node = edge['to']
        if len(from_node) == 1 and len(to_node) == 1:
            res_edges.append({
                'from': from_node[0],
                'to': to_node[0],
            })

        if len(from_node) == 1 and len(to_node) > 1:
            for to_item in to_node:
                res_edges.append({
                    'from': from_node[0],
                    'to': to_item,
                })

        if len(from_node) > 1 and len(to_node) == 1:
            for from_item in from_node:
                res_edges.append({
                    'from': from_item,
                    'to': to_node[0],
                })

    # color the data nodes
    # if it appear in 'to'; don't change
    for node_item in data_nodes:
        node_label = node_item['col_name']
        node_name = node_item['label']
        occurred_v = []
        port_v = ''
        node_color = {}
        for idx, edge in enumerate(res_edges):
            # edge_from, edge_to, color_type = edge
            edge_from, edge_to = edge['from'], edge['to']
            if isinstance(edge_from, str):
                pass
            elif isinstance(edge_from, dict):
                if edge_from['label'] == node_name:
                    port_v = edge_from['label']  # what's/re the from column(s)
                    if port_v in occurred_v:
                        pass
                    else:
                        node_color.update({port_v: _color_})
                        # orma_dot.node(node_name, label=node_label, fillcolor=node_color[f'{port_v}'])

            if isinstance(edge_to, str):
                pass
            elif isinstance(edge_to, dict):
                if edge_to['label'] == node_name:
                    port_v = edge_to['label']  # what's/re the to column(s)
                    node_color.update({port_v: edge_to['color']})
                    occurred_v.append(port_v)
        if not port_v:
            pass
        else:
            orma_dot.node(node_name, label=node_label, fillcolor=node_color[port_v])

    draw_edges(res_edges, orma_dot)
    # orma_dot.view()
    return orma_dot

def get_schema_list(schema_info):
    schemas = []
    for schema in schema_info:
        schemas.append(schema['schema'])
    return schemas


def parallel_view_main(project_id, output_gv):
    '''Run parallel view'''
    json_data, schema_info = gen_recipe(project_id)
    schemas = get_schema_list(schema_info)
    orma_g = generate_dot(json_data, schemas, output_gv)
    orma_g.view()


def main():
    parser = argparse.ArgumentParser(description='OpenRefine Model Analysis')
    parser.add_argument(
        "--project_id",
        type=int,
        default=2011536917259,
        help='Input Project ID'
    )
    parser.add_argument(
        "--output",
        type=str,
        default='output/orma_exp.gv',
        help='path of the output gv file'
    )
    args = parser.parse_args()
    parallel_view_main(args.project_id, args.output)


if __name__ == '__main__':
    # 1794307527883
    # or_project_files/ppp_user3 load, try facet information for read_scope
    # python orma.py --project_id 2190796843367 --output output/ppp_user3.gv
    main()
