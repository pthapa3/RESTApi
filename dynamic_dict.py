import json
from pprint import pprint
import argparse
import os 
import sys
from collections import OrderedDict
from collections import defaultdict
import ast




def get_leaf_dict(json_list, cmd_args):
	leaf_dict = {}
	for k, v in json_list.items():
		if k not in cmd_args.keys:
			 leaf_dict[k] = v
	
	return leaf_dict


def update(my_dict1, my_dict2, key):
	
	for k in my_dict1:
		for k1 in my_dict2:
			if k == k1:
				if isinstance(my_dict1.get(k), dict):
					my_dict1[k].update(my_dict2.get(k, {}))
				else:
					my_dict1[k] = my_dict1.get(k)+my_dict2.get(k)
	return {key:my_dict1}



def traverse(dict1, dict2, key):
	# print('key:', key)
	updated_dict = {}
	for k, v in dict1.items():
		for k1, v1 in dict2.items():
			if k1 == k:
				updated_dict = update(v, v1, k)
					
	return updated_dict



# Create nested dictionary bottom up
def create_nested_dict(json_list, cmd_args):
	dynamic_dict = {}
	for json_dict in json_list:
	
		leaf_dict = get_leaf_dict(json_dict, cmd_args)
		nested_dict = {json_dict.get(cmd_args.keys[-1]):[leaf_dict]}
		
		for i in range(len(cmd_args.keys)-1):

			nested_dict = {json_dict.get(cmd_args.keys[-2-i]): nested_dict}
		
		 

		keys = list(nested_dict.keys())
		
		for key in keys:
			if key not in dynamic_dict:
				dynamic_dict.update(nested_dict)
			else:
				
				get_dict = traverse(nested_dict, dynamic_dict, key)

				print ('get dict: ', get_dict)

				if isinstance(get_dict.get(key), dict):
					dynamic_dict[key].update(get_dict.get(key, {}))
				else:
					dynamic_dict[key] = dynamic_dict.get(key) + get_dict.get(key)

			
	return dynamic_dict





json_input = sys.stdin.read()





json_obj = json.loads(json_input)
print ("hello\n")

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('keys', nargs = '*')

cmdline_args = arg_parser.parse_args()


nested_dictionaries  = create_nested_dict(json_obj, cmdline_args)

# print('Json array input:\n', json.dumps(json_obj, indent=4), '\n')
# print('Nested dictionary:\n',json.dumps(nested_dictionaries, indent=4))












