import json

def parse_edits(edits):
    res = []
    for edit in edits:
        e_from = edit['from']
        e_to = edit['to']
        res.append({
            'from': e_from,
            'to': e_to
        })
    return res

def extract(recipe):
    # Extract operation names, functions, description
    # Save the compressed information into a JSON format res
    output = []
    for operator in recipe:
        op_dict = {}
        if 'op' in operator:
            op_name = operator['op']
            op_dict['operation name'] = op_name
            desc = operator['description']
            op_dict['description'] = desc
            if op_name == 'core/text-transform':
                op_dict['arg'] = {'expression': operator['expression']}
            elif op_name == 'core/mass-edit':
                edits = operator['edits']
                op_dict['arg'] = {'edits': parse_edits(edits)}
            elif op_name == 'core/column-addition':
                op_dict['arg'] = {'expression': operator['expression']}
            elif op_name == 'core/column-removal':
                op_dict['arg'] = {'columnName': operator['columnName']}
            elif op_name == 'core/column-split':
                op_dict['arg'] = {'separator': operator['separator'],
                                  'removeOriginalColumn': operator["removeOriginalColumn"]}
            elif op_name == 'core/column-rename':
                op_dict['arg'] = {'old': operator['oldColumnName'],
                                  'new': operator['newColumnName']}
            else:
                continue
        output.append(op_dict)
    assert len(output) == len(recipe)
    return output

with open('titanic/preparations/recipes/titanic_prep2.json', 'r')as prep:
    r1 = json.load(prep)
    # r2 = json.load(prep)

# output2 = extract(r2)
output1 = extract(r1)
# print(output2)
# with open('titanic/preparations/recipes/prep2_comp.json', 'w') as prep2_comp:
#     json.dump(output2, prep2_comp, indent=4)
with open('titanic/preparations/recipes/prep1_comp.json', 'w') as prep1_comp:
    json.dump(output1, prep1_comp, indent=4)