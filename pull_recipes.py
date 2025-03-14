from call_or import get_operations, list_projects
from refine import *
import re 

def find_projects(pattern=r'menu_p.*'):
    """match project names and find the project ids"""
    names = []
    ids = []
    projects = list_projects()
    for proj_id, v in projects.items():
        dataset_name = v['name']
        project_id = int(proj_id)
        if re.match(pattern, dataset_name):
             print(dataset_name)
             ids.append(project_id)
             names.append(dataset_name)
    return ids, names


def pull_recipes(project_id, project_name):
    data = get_operations(project_id)
    filepath = f"recipes/{project_name}.json"
    if not os.path.exists(filepath):
        with open(filepath, "w") as workflow:
            json.dump(data, workflow, indent=4)  # `indent=4` adds pretty formatting
    else:
        print(f"{filepath} Has Been Existed!")

def main():     
    patterns = [r'dish_sample_.*', r'ppp_sample_.*', r'chi_sample_.*',
                r'menu_p.*']
    
    project_ids = []
    project_names = []
    for pattern in patterns:
        ids, names = find_projects(pattern)
        project_ids += ids
        project_names += names
    assert len(project_ids) == len(project_names)
    print(len(project_ids))
    os.makedirs("recipes", exist_ok=True)
    for idx, project_id in enumerate(project_ids):
        proj_name = project_names[idx]
        pull_recipes(project_id, proj_name)


if __name__ == '__main__':
    main()

# def pull_recipes(pattern=r'dish_sample_.*'):
#     """ Auto pull recipes if the project name follows the pattern"""
#     with open(filepath, "w") as workflow:
#         json.dump(data, workflow, indent=4)  # `indent=4` adds pretty formatting