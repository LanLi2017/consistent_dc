import json
import google.generativeai as genai
from orma import *

genai.configure(api_key="AIzaSyCub3B-YVlt_Z_8zcBk1Fs3Cc28DsY9buU")
model = genai.GenerativeModel("gemini-2.0-flash")

def retrieve_recipe(project_id, fp="formal_recipe"):
    json_data, schema_info = gen_recipe(project_id)
    schemas = get_schema_list(schema_info)
    orma_g = translate_operator_json_to_graph(json_data, schemas)
    formal_recipe = graph_parser(orma_g, json_data)
    with open(f"recipes/{fp}.json", "w") as f:
        json.dump(formal_recipe, f, indent=4)
    return formal_recipe


def graph_parser(orma_g, recipe):
    # parse the recipe into a list of operations
    # each operation has op_name, read_scope, write_scope, and args(expression)
    # save the compressed information into a JSON format res
    formal_recipe = []
    for i, graph in enumerate(orma_g):
        ops_meta = {}
        ops_meta["op"] = recipe[i]["op"]
        ops_meta["read_scope"] = [x['col_name'] for x in graph.in_node_names]
        ops_meta["write_scope"] = [x['col_name'] for x in graph.out_node_names]
        # TODO: add more parameters for some operations without expression
        # if "expression" in recipe[i]:
        #     ops_meta["expression"] = recipe[i]["expression"]
        if ops_meta["op"]=='core/mass-edit':
            ops_meta["expression"] = recipe[i]["edits"]
        elif ops_meta["op"]=='core/column-split':
            ops_meta["separator"] = recipe[i]["separator"]
        elif "expression" in recipe[i]:
            ops_meta["expression"] = recipe[i]["expression"]
        else:
            continue
        formal_recipe.append(ops_meta)
    return formal_recipe


def clean_response(response, operation):
    # Clean the response from the LLM
    # Return JSON object
    if response.text:
        match = re.search(r'({.*})', response.text, re.DOTALL)

        if match:
            clean_json = match.group(1)  # Extract the valid JSON part
            try:
                enhanced_op = json.loads(clean_json)
                operation.update(enhanced_op)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                # Handle the error or return a default value
        else:
            print("No valid JSON found in the response.")
    else:
        print("Received empty response.")
        # Handle the empty response case    
    print(operation)
    return operation

def enhance_op_obj(operation):
    # Enhance the operation with the help of LLM
    # Return the enhanced operation with objective
    with open("prompts/learn_objectives.txt", "r") as f:
        learn_objectives = f.read()
    op_input = {k:v for k,v in operation.items()}
    print(op_input)
    gen_objectives = learn_objectives + f"""\n\n Based on the operation inputs provided as following, output 
    **category**, **objective** and **semantics** in 
.\n"""+f"""
Input: {op_input}
Output:
    """
    print(gen_objectives)
    response = model.generate_content(gen_objectives)
    operation = clean_response(response, operation)
    return operation


if __name__ == "__main__":
    # project_id = 2683654955729 # User1
    project_id = 2488155864905 # User2
    fp = "formal_recipe1"
    formal_recipe = retrieve_recipe(project_id, fp)
    enhanced_recipe = []
    for op in formal_recipe[:]:
        op_enhanced = enhance_op_obj(op)
        enhanced_recipe.append(op_enhanced)
    new_fp = "enhanced_recipe1"
    with open(f"recipes/{new_fp}.json", "w") as f:
        json.dump(enhanced_recipe, f, indent=4)


