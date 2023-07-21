#{\"body\":\"test_string\",\"metadata\":\"test_metadata\"}

# Python base imports
import sys
import json

# XFaaS specific imports
from python.src.utils.classes.commons.serwo_objects import SerWOObject

# User function (Add your logic here)
def user_function(xfaas_object):
    try:
        print(xfaas_object.to_json())
        body = xfaas_object.get_body()
        print("func2", body["input_num"]+2)
        metadata = xfaas_object.get_metadata()
        return SerWOObject(body=body,metadata=metadata)
    except Exception as e:
        print(e)
        raise Exception("[SerWOLite-Error]::Error at user function")