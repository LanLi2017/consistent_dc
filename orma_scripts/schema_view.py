
from graphviz import Digraph
from orma import merge_basename
from extra_info import generate_recipe as gen_recipe


_color_ = '#FFFFCC'  # default color for output node
_inNodeColor_ = '#FAFAF0'  # default color for input node
_edge_color_ = '#000000'  # default edge color: black
_gen_val_color_ = '#f7ce8d'  # generic + value changed
_type_con_color_ = '#d4eafa'  # type convert color
_type_label_color_ = '#14697e'  # type convert label color
_custome_v_color = '#fbb8b8'  # customized value color
_gen_label_color_ = '#b06e04'  # generic + value label color
_remove_color_ = '#D0D0D0'  # color for removing cells

# TASK 2; Create a summary view of data cleaning workflow
def schema_analysis(recipe, schema_info):
    edges = []
    # analyze schema change and define the edges
    for i, operator in enumerate(recipe, start=1):
        if 'op' in [*operator]:
            if operator['op'] == 'core/column-addition':  # merge operation
                basename = merge_basename(operator)
                edge_to = {f'schema{i}': operator['newColumnName'], 'color': _gen_val_color_}
                if isinstance(basename, list):
                    for idx, col_name in enumerate(basename):
                        if idx == len(basename) - 1:
                            edge_from = {f'schema{i - 1}': col_name, 'label': ' column-addition',
                                         'edge_color': _gen_label_color_}
                        else:
                            edge_from = {f'schema{i - 1}': col_name, 'label': ' ',
                                         'edge_color': _gen_label_color_}
                        edges.append([edge_from, edge_to])
                else:
                    edge_from = {f'schema{i - 1}': basename, 'label': ' column-addition',
                                 'edge_color': _gen_label_color_}
                    edges.append([edge_from, edge_to])

            elif operator['op'] == 'core/column-split':  # split operation
                cur_schema = schema_info[i]
                prev_schema = schema_info[i - 1]
                new_cols = list(set(cur_schema) - set(prev_schema))
                # label_name = operator['op'].split('-')[-1]

                for idx, cols in enumerate(new_cols):
                    # edge_label = f'_{cols.split(" ")[-1]}
                    if idx == 0:
                        edge_from = {f'schema{i - 1}': operator['columnName'], 'label': ' column-split',
                                     'edge_color': _gen_label_color_}
                    else:
                        edge_from = {f'schema{i - 1}': operator['columnName'], 'label': ' ',
                                     'edge_color': _gen_label_color_}
                    edge_to = {f'schema{i}': cols, 'color': _gen_val_color_}
                    edges.append([edge_from, edge_to])
                # original_col = operator['columnName']
                # flag_original = original_col in cur_schema
                # if flag_original:
                #     edge_from = {f'schema{i - 1}': operator['columnName'], 'label': ' ',
                #                  'edge_color': _gen_label_color_}
                #     edge_to = {f'schema{i}': original_col, 'color': _color_}
                #     # not remove the original column
                #     edges.append([edge_from, edge_to])
                # else:
                #     # remove the original column
                #     pass

            elif operator['op'] == 'core/column-rename':  # split operation
                edge_from = {f'schema{i - 1}': operator['oldColumnName'], 'label': ' column-rename',
                             'edge_color': _edge_color_}
                edge_to = {f'schema{i}': operator['newColumnName'], 'color': _color_}
                edges.append([edge_from, edge_to])

            elif operator['op'] == 'core/column-removal':
                edge_from = {f'schema{i - 1}': operator['columnName'], 'label': ' column-removal',
                             'style': 'dashed', 'edge_color': _gen_label_color_}
                prev_schema = schema_info[i - 1]
                old_idx = prev_schema.index(operator['columnName'])
                prev_idx = old_idx - 1
                edge_to = {f'schema{i}': f"{prev_schema[prev_idx]}",
                           'color': _remove_color_,
                           }
                # edge_to 'label': edge_label, 'style': 'dashed',
                #                              'edge_color': '#000000'}
                edges.append([edge_from, edge_to])

            elif operator['op'] == 'core/column-addition-by-fetching-urls':
                edge_from = {f'schema{i - 1}': operator['baseColumnName']}
                edge_to = {f'schema{i}': f"{operator['newColumnName']}", 'color': _gen_val_color_}
                edges.append([edge_from, edge_to])

            elif operator['op'] == 'core/multivalued-cell-join':
                edge_from = {f'schema{i - 1}': operator['columnName']}
                edge_to = {f'schema{i}': f"{operator['columnName']}", 'color': _gen_val_color_}
                edges.append([edge_from, edge_to])

            elif operator['op'] == 'core/transpose-columns-into-rows':
                new_cols = [operator['keyColumnName'], operator['valueColumnName']]
                for index, new_col in enumerate(new_cols):
                    if index == 0:
                        edge_from = {f'schema{i - 1}': operator['startColumnName'],
                                     'label': ' ', 'edge_color': _gen_label_color_}
                    else:
                        edge_from = {f'schema{i - 1}': operator['startColumnName'],
                                     'label': ' transpose-columns-into-rows', 'edge_color': _gen_label_color_}
                    edge_to = {f'schema{i}': f"{new_col}", 'color': _gen_val_color_}
                    edges.append([edge_from, edge_to])

            elif operator['op'] == 'core/row-removal':
                edge_from = {f'schema{i - 1}': operator['engineConfig']['facets'][0]['name']}
                edge_to = {f'schema{i - 1}': operator['engineConfig']['facets'][0]['name'], 'color': _color_}
                edges.append([edge_from, edge_to])

            elif operator['op'] == 'core/column-move':
                cur_schema = schema_info[i]  # after applying this transformation
                # column_to #5
                old_schema = schema_info[i - 1]  # before applying this transformation

                col_name = operator['columnName']
                old_idx = old_schema.index(col_name)
                new_idx = operator['index']
                edge_from = {f'schema{i - 1}': col_name, 'style': 'dashed',
                             'label': f' Move_to #{new_idx}',
                             'edge_color': _edge_color_}
                edge_to = {f'schema{i}': col_name, 'color': _color_}
                edges.append([edge_from, edge_to])  # for now consider it as change structure level

                old_col_name = old_schema[new_idx]
                # define invisible node: from and to
                iv_edge_from = {f'schema{i - 1}': old_col_name, 'style': 'invisible',
                                'label': '',
                                'dir': 'none',
                                'edge_color': _edge_color_}
                iv_edge_to = {f'schema{i}': old_col_name, 'color': _inNodeColor_}
                edges.append([iv_edge_from, iv_edge_to])

                # add start to start
                start_col_name = old_schema[0]
                start_edge_from = {f'schema{i - 1}': start_col_name, 'style': 'invisible',
                                   'label': '',
                                   'dir': 'none',
                                   'edge_color': _edge_color_}
                start_edge_to = {f'schema{i}': start_col_name, 'color': _inNodeColor_}
                edges.append([start_edge_from, start_edge_to])

                # add end to end
                end_col_name = old_schema[-1]
                end_edge_from = {f'schema{i - 1}': end_col_name, 'style': 'invisible',
                                 'label': '',
                                 'dir': 'none',
                                 'edge_color': _edge_color_}
                end_edge_to = {f'schema{i}': end_col_name, 'color': _inNodeColor_}
                edges.append([end_edge_from, end_edge_to])

            elif operator['op'] == 'core/mass-edit':
                edge_from = {f'schema{i - 1}': operator['columnName'], 'label': ' mass-edit', 'edge_color': '#BB0000'}
                edge_to = {f'schema{i}': operator['columnName'], 'color': _custome_v_color}
                edges.append([edge_from, edge_to])

            # TODO
            # reconciliation
            elif operator['op'] == 'core/recon':
                edge_from = {f'schema{i - 1}': operator['columnName'], 'label': ' reconciliation',
                             'edge_color': '#BB0000'}
                edge_to = {f'schema{i}': operator['columnName'], 'color': _custome_v_color}
                edges.append([edge_from, edge_to])
            else:  # normal unary operation
                try:
                    column_name = operator['columnName']
                    if 'expression' in operator:
                        expression = operator['expression']
                        exp_preprocess = expression.split(".")[0]
                        if exp_preprocess == 'value':
                            label = f' .{expression.split(".")[-1]}'
                            if expression == 'value.toDate()':
                                # schema change
                                edge_color = _type_label_color_
                                edge_to = {f'schema{i}': operator['columnName'], 'color': _type_con_color_}
                            elif expression == 'value.toNumber()':
                                # schema change
                                edge_color = _type_label_color_
                                edge_to = {f'schema{i}': operator['columnName'], 'color': _type_con_color_}
                            else:
                                edge_color = _gen_label_color_
                                edge_to = {f'schema{i}': operator['columnName'], 'color': _gen_val_color_}

                        else:
                            # value change
                            label = f' {expression}'
                            edge_color = _gen_label_color_
                            edge_to = {f'schema{i}': operator['columnName'], 'color': _gen_val_color_}
                        edge_from = {f'schema{i - 1}': operator['columnName'], 'label': label, 'edge_color': edge_color}
                        edges.append([edge_from, edge_to])
                    else:
                        label = operator['op'].split('/')
                        edge_from = {f'schema{i - 1}': column_name, 'label': f' {label}',
                                     'edge_color': _gen_label_color_}
                        edge_to = {f'schema{i}': column_name, 'color': _gen_val_color_}
                        edges.append([edge_from, edge_to])
                except KeyError:
                    continue
        else:
            prev_schema = schema_info[i - 1]
            cur_schema = schema_info[i]
            assert len(cur_schema) == len(prev_schema)
            description = operator['description'].split(' ')
            if 'column' in description:
                # single edit
                # take care of this transformation!
                column_name = description[-1]
                desc = operator['description']
                edge_label = f' single_cell_edit row #{desc.split(",")[0].split(" ")[-1]}'
                edge_from = {f'schema{i - 1}': column_name, 'label': edge_label, 'edge_color': '#BB0000'}
                edge_to = {f'schema{i}': column_name, 'color': _custome_v_color}
                edges.append([edge_from, edge_to])
            else:
                # Star/flag row 1
                desc = operator['description']
                edge_label = f' {"_".join(desc.split(" ")[:2])} #{desc.split(" ")[-1]}'
                edge_from = {f'schema{i - 1}': cur_schema[0], 'label': edge_label, 'style': 'dashed',
                             'edge_color': '#000000'}
                edge_to = {f'schema{i}': cur_schema[0], 'color': '#D0D0D0'}
                edges.append([edge_from, edge_to])

    return edges


def get_schema_list(schema_info):
    schemas = []
    for schema in schema_info:
        schemas.append(schema['schema'])
    return schemas


def get_edge_ports(key, value, schemas):
    schema_no = int(key.split('schema')[-1])
    cur_schema = schemas[schema_no]
    from_idx = cur_schema.index(value)
    update_name = f'{key}:f{from_idx}'
    return update_name


def get_edges(edges, schemas, schema_graph):
    # read and refine into edges in graph
    for i, edge in enumerate(edges):
        edge_from, edge_to = edge
        # edge_from, edge_to, color_type = edge
        edge_from_update = ''
        edge_to_update = ''
        if 'dir' in [*edge_from]:
            for key, value in edge_from.items():
                if key == 'label':
                    pass
                elif key == 'style':
                    pass
                elif key == 'edge_color':
                    pass
                elif key == 'dir':
                    pass
                else:
                    edge_from_update = get_edge_ports(key, value, schemas)
            for key1, value1 in edge_to.items():
                if key1 == 'color':
                    pass
                else:
                    edge_to_update = get_edge_ports(key1, value1, schemas)
            schema_graph.edge(edge_from_update, edge_to_update, label=edge_from['label'], style=edge_from['style'],
                              dir=edge_from['dir'],
                              color=edge_from['edge_color'], fontcolor=edge_from['edge_color'])
        else:
            if 'style' in [*edge_from]:
                # specific transformation
                # label stands for edge's label
                for key, value in edge_from.items():
                    if key == 'label':
                        pass
                    elif key == 'style':
                        pass
                    elif key == 'edge_color':
                        pass
                    else:
                        edge_from_update = get_edge_ports(key, value, schemas)
                for key1, value1 in edge_to.items():
                    if key1 == 'color':
                        pass
                    else:
                        edge_to_update = get_edge_ports(key1, value1, schemas)
                schema_graph.edge(edge_from_update, edge_to_update, label=edge_from['label'], style=edge_from['style'],
                                  color=edge_from['edge_color'], fontcolor=edge_from['edge_color'])
            else:
                if 'label' in [*edge_from]:
                    # has label --> must have edge_color
                    for key, value in edge_from.items():
                        if key == 'label':
                            pass
                        elif key == 'edge_color':
                            pass
                        else:
                            edge_from_update = get_edge_ports(key, value, schemas)
                    for key1, value1 in edge_to.items():
                        if key1 == 'color':
                            pass
                        else:
                            edge_to_update = get_edge_ports(key1, value1, schemas)
                    schema_graph.edge(edge_from_update, edge_to_update, label=edge_from['label'],
                                      color=edge_from['edge_color'], fontcolor=edge_from['edge_color'])
                else:
                    for key, value in edge_from.items():
                        edge_from_update = get_edge_ports(key, value, schemas)
                    for key1, value1 in edge_to.items():
                        if key1 == 'color':
                            pass
                        else:
                            edge_to_update = get_edge_ports(key1, value1, schemas)
                    schema_graph.edge(edge_from_update, edge_to_update)
        # edges_list.append((edge_from_update, edge_to_update))
    return schema_graph


def color_ports(schema, color_idx: list, color_type: dict):
    # html like label
    '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD PORT="f0">one</TD>
    <TD>two</TD>
  </TR>
</TABLE>>'''
    res = '<<table align="left" border="0" cellspacing="0">'
    res += '<tr>'
    for i, column in enumerate(schema):
        if i in color_idx:
            color = color_type[column]
            res += f'<td port="f{i}" border="1" bgcolor="{color}" >{column}</td>'
        else:
            res += f'<td port="f{i}" border="1">{column}</td>'
    res += '</tr>'
    res += '</table>>'
    return res


def draw_schema_evolution(recipe, schemas, output):
    # use Data structure from graphviz
    feature_data = {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': '#FAFAF0',
                    'fontname': "Symbol", 'fontsize': "12"}  # should be string!!!
    schema_graph = Digraph('Schema_Evolution', filename=output)
    schema_graph.graph_attr['ranksep'] = '0.5'
    schema_graph.attr('node', shape=feature_data['shape'], style=feature_data['style'],
                      fillcolor=feature_data['fillcolor'],
                      fontname=feature_data['fontname'], fontsize=feature_data['fontsize'])
    schema_graph.attr('edge', fontname="Helvetica-BoldOblique", fontsize="12")

    # schema_graph.attr('node', fontsize="16", shape="ellipse")

    # [[{'schema0': 'date'}, {'schema1': 'date 2'}],...]
    # [from, to]
    edges = schema_analysis(recipe, schemas)

    for i, schema in enumerate(schemas):
        node_name = f'schema{i}'
        occurred_v = []
        port_values = []
        port_idx = []
        node_color = {}
        for idx, edge in enumerate(edges):
            # edge_from, edge_to, color_type = edge
            edge_from, edge_to = edge
            if node_name in [*edge_from]:
                port_v = edge_from[node_name]  # what's/re the from column(s)
                port_id = schema.index(port_v)  # what's/re the port index(es)
                if port_v in occurred_v:
                    pass
                else:
                    port_values.append(port_v)
                    port_idx.append(port_id)
                    if 'style' in [*edge_from]:
                        if edge_from['style'] == 'invisible':
                            node_color.update({port_v: _inNodeColor_})
                        else:
                            node_color.update({port_v: _color_})
                    else:
                        node_color.update({port_v: _color_})

            if node_name in [*edge_to]:
                port_v = edge_to[node_name]  # what's/re the to column(s)
                port_id = schema.index(port_v)  # what's/re the port index(es)
                port_idx.append(port_id)
                port_values.append(port_v)
                node_color.update({port_v: edge_to['color']})
                occurred_v.append(port_v)

        label = color_ports(schema, port_idx, color_type=node_color)
        schema_graph.node(node_name, label=f'''{label}''')

    schema_graph = get_edges(edges, schemas, schema_graph)
    # schema_graph.edges(edges_list)

    return schema_graph


def model_schema_evolution(project_id, output_gv):
    # project_id = 2124203262743  # 2486157629041
    recipe, schema_info = gen_recipe(project_id)
    schemas = get_schema_list(schema_info)
    # output_gv = 'output/schema_evo.gv'
    schema_graph = draw_schema_evolution(recipe, schemas, output_gv)
    schema_graph.view()