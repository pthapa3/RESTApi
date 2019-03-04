# Runs only on Mac OS or Linux Systems.
# select module not supported by Windows File system.

import json
import argparse
import os
import sys
import logging
import select


def get_leaf_dict(json_list, cmd_args):
    # Extracts a leaf dictionary based on the keys provided
    leaf_dict = {}
    for k, v in json_list.items():
        if k not in cmd_args.keys:
            leaf_dict[k] = v
    logging.debug("Leaf dictionary created\n")
    return leaf_dict


def update(dict1, dict2, key):
    # Goes until the leaf dictionary to check if same key exists
    # If exists, updates the values by either updating the dictionary if
    #  leaf value is dictionaries or adds to the current list of dictionary
    #  if the leaf value is list.
    
    logging.debug("Updating values of same keys\n")
    for k in dict1:
        for k1 in dict2:
            if k == k1:
                if isinstance(dict1.get(k), dict):
                    dict1[k].update(dict2.get(k, {}))
                else:
                    dict1[k] = dict1.get(k)+dict2.get(k)

    return {key:dict1}



def traverse(dict1, dict2, key):
    # Traverse through the current dictionary and the nested dictionary
    # being created. If same keys exists it calls update() to update the values
    updated_dict = {}
    logging.debug("Checking if same key exists. If exists, values will be updated accordingly.\n")
    for k, v in dict1.items():
        for k1, v1 in dict2.items():
            if k1 == k:
                updated_dict = update(v, v1, k)
    
    return updated_dict



# Create nested dictionary bottom up
def create_current_dict(json_list, cmd_args):
    # Traverse through each dictionary and creates
    #  nested dictionary dynamically with the keys provided
    #  If the same key exist it will update its values accordingly
    #  otherwise it will just add to the nested_dict
    nested_dict = {}
    for json_dict in json_list:
        
        logging.debug("Creating leaf values as arrays of flat dictionaries\n")
        leaf_dict = get_leaf_dict(json_dict, cmd_args)
        current_dict = {json_dict.get(cmd_args.keys[-1]):[leaf_dict]}
        logging.debug("Leaf values as arrays of flat dictionaries created\n")
        
        for i in range(len(cmd_args.keys)-1):
            current_dict = {json_dict.get(cmd_args.keys[-2-i]): current_dict}
    
        keys = list(current_dict.keys())
        
        for key in keys:
            if key not in nested_dict:
                nested_dict.update(current_dict)
            else:
                
                get_dict = traverse(current_dict, nested_dict, key)
                
                if isinstance(get_dict.get(key), dict):
                    nested_dict[key].update(get_dict.get(key, {}))
                else:
                    nested_dict[key] = nested_dict.get(key) + get_dict.get(key)


    return nested_dict


def check_dup_args(key_args):
    if (len(key_args)==0):
        sys.stderr.write ('\nError: ********** Please enter at least one key to create nested dictionaries **********\n')
        return False
    if (len(set(key_args))!= len(key_args)):
        sys.stderr.write ('\nError: ********** Duplicate keys are NOT supported. **********\n')
        return False
    else:
        return True




def run():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.DEBUG)
    # If input is not given, it will throw an error and terminate the program
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        json_input = sys.stdin.read()
        if json_input:
                json_obj = json.loads(json_input)
                
                logging.debug("Json Array input accepted. Ready to create nested dictionary\n")
                
                arg_parser = argparse.ArgumentParser()
                arg_parser.add_argument('keys', nargs = '*')
                
                cmdline_args = arg_parser.parse_args()
                logging.debug("Key arguments parsed. Validating key arguments\n")
                
                if (check_dup_args(cmdline_args.keys) == False):
                    sys.stderr.write("\nExiting Program\n")
                    exit(0)
                        
                else:
                    try:
                        current_dictionaries  = create_current_dict(json_obj, cmdline_args)
                        array_input = 'Json array input:\n'+ json.dumps(json_obj, indent=4)+'\n'
                        dictionary_output = '\nNested dictionary:\n'+(json.dumps(current_dictionaries, indent=4))
                        sys.stdout.write(array_input)
                        sys.stdout.write(dictionary_output)
                            
                    except Exception as e:
                        sys.stderr.write("Error")
                        logging.error("Exception occurred", exc_info=True)
                                
        else:
            sys.stderr.write('\n\n******** Program Ended... ********\n')
            exit(0)
    else:
        sys.stderr.write('\nError: ********** Please give a valid json file as an input and run it as:\
                         \n cat Yourfilename.json | python nest.py key1 [optional keys......] \n**********\n')



if __name__ == '__main__':
    run()


