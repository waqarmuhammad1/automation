import json

build = None   # command for running a user's program
email = None
error = None
test_dict = {} # (key, val) where key is the name of the test case and val is its entire json object
output_list = [] # output value for every test case in json file
assert_list = [] # assert value for every test case in josn file
exit_list = [] # exit value for every test case in josn file


def parse_config(path):
    global build, email, test_dict, error

    try:
        file = open(path)
    except:
        error = 'config file not found'
        return -1

    json_file = json.load(file)

    # Check that mandatory build property is present and filled out
    try:
        build = json_file['build']
    except:
        error = 'build property is required'
        return -1
    if len(build) <= 0:
        error = 'build property value cannot be empty'
        return -1

    try:
        email = json_file['email']  # see if optional email property is present in the file
    except:
        email = None

    for (key, val) in json_file.items():
        if key not in ['build', 'email']: # save all other properties as test case objects
            test_dict[key] = val

    return 0

def isolate_result_checks(test_cases): # (key, val) where key is the name of the test case and val is its entire json object
    global output_list, assert_list, exit_list, error
    for case in test_cases:
      # A valid test case must have either a valid exit status code to check, or a valid output + assertion to check
      try:
        output = test_cases[case]['output']
      except:
        output = None
      output_list.append(output)
      
      try:
        assertion = test_cases[case]['assert']
        if assertion not in ["==","!=","<","<=",">",">="]:
            error = "assertion in " + case + " must be of one of the forms: [==,!=,<,<=,>,>=]"
            return -1
        if output == None:
            error = 'error in test case ' + case + '. assertion provided without an output property'
            return -1
      except:
        assertion = None
        if output != None:
            error = 'error in test case ' + case + '. output provided without an assertion property'
            return -1
      assert_list.append(assertion)
	
      try:
        exit = test_cases[case]['exit']
      except:
        exit = None
      exit_list.append(exit)

      if assertion is None or output is None:
        if exit is None:
            error = 'error in test case ' + case + '. No expected exit code or output provided'
            return -1

    return 0


#  return the build command with all input values appended
def get_build(test_case):
    global build
    command = build
    for key in test_case:
        if key not in ['exit', 'output', 'assert']:
            command = command + ' ' + str(test_case[key])
    return command

