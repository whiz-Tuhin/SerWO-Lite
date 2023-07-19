import sys
import json

def user_function(xfaas_object):
    # user logic
    pass


def unmarshall():
    pass

def build_serwo_object(input):
    pass

def build_serwo_list_object(input):
    pass

# DO NOT CHANGE
if __name__ == "__main__":
    input = json.loads(sys.argv[1]) # request json as a string
    
    # building serwo object
    if isinstance(input) is list:
        marshalled_object = build_serwo_list_object(input)
    else:
        marshalled_object = build_serwo_object(input)

    # execute user function
    retobj = user_function(marshalled_object)
    
    # unmarshall
    output = unmarshall(retobj)

    # print to console
    print(output)
