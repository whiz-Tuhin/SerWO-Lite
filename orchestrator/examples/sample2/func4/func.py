#{\"body\":\"test_string\",\"metadata\":\"test_metadata\"}

# Python base imports
import sys
import json

# XFaaS specific imports
from python.src.utils.classes.commons.serwo_objects import SerWOObject

# User function (Add your logic here)
def user_function(xfaas_object):
    try:
        count = 0
        for idx, item in enumerate(xfaas_object.get_objects()):
            print(f"func4 call{idx}", item.get_body()["input_num"]+1)
            count += item.get_body()["input_num"]+1
        return SerWOObject(body={"input_num": count},metadata=xfaas_object.get_metadata())
    except Exception as e:
        print(e)
        raise Exception("[SerWOLite-Error]::Error at user function")