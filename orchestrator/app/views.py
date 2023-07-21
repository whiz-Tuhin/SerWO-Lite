from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from python.src.utils.classes.commons.serwo_user_dag import SerWOUserDag
from python.src.utils.classes.commons.serwo_objects import build_serwo_object
from python.src.utils.classes.commons.serwo_objects import build_serwo_list_object
from copy import deepcopy

import json
import networkx as nx
import importlib

node_output_map = dict()

# routine to execute a user function python file
def execute_from_module(basepath, modulepath, nodename, request_input):
    module = importlib.import_module(f"{basepath}/{modulepath}")
    print(f"Calling function {nodename}")

    if isinstance(request_input, list):
        serwo_object = build_serwo_list_object(request_input)
    elif isinstance(request_input, dict):
        new_event = deepcopy(request_input)
        event = dict(body=new_event)
        event['metadata'] = dict(
            info="Dummy metadata"
        )
        serwo_object = build_serwo_object(event)
    else:
        return dict(
            statusCode=500,
            body="request not a valid json",
            metadata=None
        )

    statusCode = 200
    try:
        response = module.user_function(serwo_object)
    except Exception as e:
        print(e)
        statusCode = 500
        return dict(
            statusCode=statusCode,
            body="Error in user compute",
            metadata=None
        )
    return dict(
        statusCode=statusCode,
        body=response.get_body(),
        metadata=response.metadata()
    )


@csrf_exempt
def execute(request):
    if request.method == 'POST':
        try:
            req_body = json.loads(request.body)
            dag_description_path = req_body["path"]
            
            # populate the dict excluding path as a blacklist key
            data = dict()
            for k,v in req_body.items():
                if k != "path":
                    data[k] = v

            # load the serwo user dag
            serwo_dag_obj = SerWOUserDag(dag_description_path)
            serwo_nx_dag = serwo_dag_obj.get_dag()  
            top_sort_nodes = list(nx.topological_sort(serwo_nx_dag))
        
            # execute based on the top sort nodes
            for v in top_sort_nodes:
                if serwo_nx_dag.in_degree(v) == 0:
                    out = execute_from_module(dag_description_path, serwo_nx_dag[v]["Path"], serwo_nx_dag[v]["NodeName"], req_body)
                elif serwo_nx_dag.in_degree(v) == 1:
                    v_pred = serwo_nx_dag.predecessors(v)[0]
                    v_input = node_output_map[v_pred]
                    out = execute_from_module(dag_description_path , serwo_nx_dag[v]["Path"], serwo_nx_dag[v]["NodeName"], v_input)
                else:
                    v_input_list = []
                    for v_pred in serwo_nx_dag.predecessors(v):
                        v_input_list.append(node_output_map[v_pred])
                    out = execute_from_module(dag_description_path , serwo_nx_dag[v]["Path"], serwo_nx_dag[v]["NodeName"], v_input_list)
                
                # return a response in case of failure
                if out["statusCode"] == 500:
                    return JsonResponse(out, status=500)
                
                # store in map
                node_output_map[v] = out

                print("Printing node map here")
                print(node_output_map)

            # Process the JSON payload here
            # For example, you can access the data using data['key_name']
            # Replace 'key_name' with the appropriate key present in your JSON payload
            response_data = {'message': 'Success', 'data': data}
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON payload'}, status=400)

    return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
