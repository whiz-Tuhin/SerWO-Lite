#{\"body\":\"test_string\",\"metadata\":\"test_metadata\"}

# Python base imports
import sys
import json

# XFaaS specific imports
from python.src.utils.classes.commons.serwo_objects import SerWOObject
from python.src.utils.classes.commons.serwo_objects import SerWOObject, SerWOObjectsList
from python.src.utils.classes.commons.serwo_objects import build_serwo_object
from python.src.utils.classes.commons.serwo_objects import build_serwo_list_object

# User function (Add your logic here)
def user_function(xfaas_object):
    try:
        # Add user logic here (remove 'pass' while adding)
        pass
    except Exception as e:
        print(e)
        raise Exception("[SerWOLite-Error]::Error at user function")

# DO NOT CHANGE
if __name__ == "__main__":
    req = sys.argv[1]
    inp_dict = dict()
    input_json = json.loads(req)
    serwo_object = None

    if isinstance(input_json, list):
        serwo_object = build_serwo_list_object(input_json)
    else:
        serwo_object = build_serwo_object(input_json)
    
    response_object = user_function(serwo_object)
    new_body = response_object.get_body()
    new_metadata = response_object.get_metadata()

    outp = dict()
    outp['body'] = new_body
    outp['metadata'] = new_metadata

    print(json.dumps(outp))