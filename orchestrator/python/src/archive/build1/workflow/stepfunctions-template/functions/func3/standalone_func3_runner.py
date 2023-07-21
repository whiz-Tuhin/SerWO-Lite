#!/usr/bin/env python
import contextlib as __stickytape_contextlib

@__stickytape_contextlib.contextmanager
def __stickytape_temporary_dir():
    import tempfile
    import shutil
    dir_path = tempfile.mkdtemp()
    try:
        yield dir_path
    finally:
        shutil.rmtree(dir_path)

with __stickytape_temporary_dir() as __stickytape_working_dir:
    def __stickytape_write_module(path, contents):
        import os, os.path

        def make_package(path):
            parts = path.split("/")
            partial_path = __stickytape_working_dir
            for part in parts:
                partial_path = os.path.join(partial_path, part)
                if not os.path.exists(partial_path):
                    os.mkdir(partial_path)
                    with open(os.path.join(partial_path, "__init__.py"), "wb") as f:
                        f.write(b"\n")

        make_package(os.path.dirname(path))

        full_path = os.path.join(__stickytape_working_dir, path)
        with open(full_path, "wb") as module_file:
            module_file.write(contents)

    import sys as __stickytape_sys
    __stickytape_sys.path.insert(0, __stickytape_working_dir)

    __stickytape_write_module('func3.py', b'import json\nimport helper_func\n\n\ndef function(serwoObject) -> dict:\n    # NOTE - assuming that the body here is in string or bytes\n    body = json.loads(serwoObject.get_body())\n    num = int(body["val"])\n    print("This is function 3")\n    x = helper_func.get_list(num)\n    return {"val": str([x]*10)}\n')
    __stickytape_write_module('helper_func.py', b'import os\n# import numpy as np\n\n\n# def randintlist(x):\n#     return [np.random.randint(x), np.random.randint(x+10), np.random.randint(x+20)]\n\ndef get_list(x):\n    return [x]*10\n')
    import importlib
    import json
    import sys
    import func3 as user_function
    
    
    '''
    NOTE - creating a serwo wrapper object from cloud events
    * a different wrapper object will be constructed for different event types
    * for one particular event type one object will be constructed
        - we will need to find common keys in the event object for one event type across different FaaS service providers
        - objective is to create a list of common keys, access patterns which will be used to create a common object to pass around
        - 
    '''
    # QUESTION - do we need a wrapper parent class around these classes ? (HttpBaseClass.HttpRequestObjec , HttpBaseClass.HttpResponseObject)
    class HttpWrapperRequestObject:
        # TODO - temporary, need to use a combination of design patterns to actually populate this
        def __init__(self, body, headers) -> None:
            self._body = body
            self._headers = headers
        
        def get_body(self):
            return self._body
    
        def get_headers(self):
            return self._headers
    
    class HttpWrapperResponseObject:
        # TODO - temporary, need to use a combination of design patterns to actually populate this
        def __init__(self, body, headers, statusCode) -> None:
            self._body = body
            self._headers = headers
            self._statusCode = statusCode
        
        # QUESTION - do we encode the response body ?
        def get_body(self):
            return self._body
    
        def get_headers(self):
            return self._headers
    
        def get_status_code(self):
            return self._statusCode
    
    # TODO - temporary builder 
    # polymorphism in python - (how to replicate ?)
    def build_serwo_http_request_object(_cloudEventObject, _handler_identifier) -> HttpWrapperRequestObject:
        # add a switch case for different _handler_identifiers
        httpWrapperRequestObject = HttpWrapperRequestObject(_cloudEventObject["body"], _cloudEventObject["headers"])
        return httpWrapperRequestObject
    
    def build_serwo_http_response_object(_responseBody, _responseHeaders, _statusCode, _handler_identifier) -> HttpWrapperResponseObject:
        # add a switch case for different _handler_identifiers
        httpWrapperResponseObject = HttpWrapperResponseObject(_responseBody, _responseHeaders, _statusCode)
        return httpWrapperResponseObject
    
    
    # # Azure handler
    # def main(obj: azure.functions.HttpRequestObject) -> object:
    #      # pre-function handler
    #     serwoObject = build_serwo_http_object(obj, "handler_id_here")
    #     # user function exec
    #     user_compute_result = user_function.function(serwoObject)
    #     # post function handler
    #     pass
    
    # AWS Handler
    def lambda_handler(event, context):
        # TODO: Unmarshal from lambda handler
        # pre-function handler
        serwoRequestObject = build_serwo_http_request_object(event, "handler_id_here")
        # user function exec
    
        statusCode = 200
        try:
            user_compute_result = user_function.function(serwoRequestObject)
        except:
            # if user compute fails then default to status code as 500 and no response body
            statusCode = 500
    
        # post function handler
        # TODO: Marshal and identify the next function
        serwoResponseObject = build_serwo_http_response_object(user_compute_result, serwoRequestObject.get_headers(), statusCode, "handler_id_here")
        # NOTE - leaving empty for now and returning a response is.
        return {
            'statusCode': serwoResponseObject.get_status_code(),
            'body': json.dumps(serwoResponseObject.get_body()),
            'headers': serwoResponseObject.get_headers()
        }
        
    
    if __name__ == "__main__":
        print("Main Method")
        # lambda_handler(event, context)