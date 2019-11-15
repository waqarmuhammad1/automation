import os
import sys
import stat
from git import Repo  # pip install --user gitpython
import read_config
from flask import Flask, jsonify, request, json
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

# Flask application initialization
app = Flask(__name__)

CORS(app)

api = Api(app)
#################################

#user_input_dict = {} # dictionary that stores additional arguments provided by the user. We may extend its usage beyond issue 37 in the last sprint.
#user_input_dict['branch'] = None # assume that user doesn't provide branch. Then, we will default to cloning from the master branch.

#gitURL = sys.argv[1] #git@git.cs.slu.edu:courses/fall19/csci_5030/sample_application.git
#extra_user_input = sys.argv[2:] # a list that stores addional arguments provided by the user. extra_user_input[0] will be the branch name. We will decide on other possible arguments later.
#print(gitURL)
#print(extra_user_input)
#if extra_user_input:
#    user_input_dict['branch'] = extra_user_input[0]
#print(user_input_dict)
#path = "temp"
#reader = read_config



class Run(Resource):
    def post(self):
        
        request_data = json.loads(request.data.decode())
        git_url = request_data['url']
        pull_git(git_url)
        reader = read_config
        if (reader.parse_config('config.json') == -1):
          print(reader.error)
          sys.exit()
        test_cases = reader.test_dict
        if (reader.isolate_result_checks(test_cases) == -1):
          print(reader.error)
          sys.exit()
        output_list = reader.output_list
        assert_list = reader.assert_list
        exit_list = reader.exit_list
        result_list = [] # renamed Chao's assert_list to result_list because another assert_list was introduced above (see Issue 27 on Gitlab)
        i = 0
        test_case_status = {}
        for case in test_cases:
            command = reader.get_build(test_cases[case])
            
            result_list.append(True)
        
            if output_list[i] != None and assert_list[i] != None:
                output = os.popen(command).read()[:-1]
                exec('result_list[i] = (output'+assert_list[i]+"output_list[i])")
        
            if exit_list[i] != None:
                output = os.system(command)
                exec('result_list[i] = result_list[i] and output == exit_list[i]') # For the case of both output and exit comparison, combine the results
            if result_list[i] == True:
                test_case_status[case] = 'Success'
            else:
                test_case_status[case] = 'Failed'
            i += 1
            
            
        print(test_case_status)
        return test_case_status

class get_commits(Resource):

    def post(self):
        request_data = json.loads(request.data.decode())
        git_url = request_data['url']
        repo, path = pull_git(git_url)
        
        result_list = []
        #Generates a list of previous commit ID in which commitIDs[0] is the most recent successful one
        commitIDs = list(repo.iter_commits('HEAD', max_count = 5))
        i = 0
        for commit in commitIDs:
            data = str(i) + ":::" + str(commit)
            print(data)
            result_list.append(data)
            i += 1
        os.chdir("..")

        rmtree(path)
        return result_list


# remove the temp directory including all files
def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)

def pull_git(data):
    user_input_dict = {} # dictionary that stores additional arguments provided by the user. We may extend its usage beyond issue 37 in the last sprint.
    user_input_dict['branch'] = None # assume that user doesn't provide branch. Then, we will default to cloning from the master branch.

    gitURL = data #git@git.cs.slu.edu:courses/fall19/csci_5030/sample_application.git
    extra_user_input = None#sys.argv[2:] # a list that stores addional arguments provided by the user. extra_user_input[0] will be the branch name. We will decide on other possible arguments later.
    print(gitURL)
    print(extra_user_input)
    if extra_user_input:
        user_input_dict['branch'] = None#extra_user_input[0]
    print(user_input_dict)
    path = "temp"
        
    #rmtree(top)
    # Create a temp directory, clone user repo into it, and list its contents                                                    
    if  os.path.isdir(path):  #removes any existing temp folder from previously failed runs                                       
        rmtree(path)
        os.mkdir(path)
    if not user_input_dict['branch']:
        repo = Repo.clone_from(gitURL, path) # clone from master
    else:
        repo = Repo.clone_from(gitURL, path, single_branch = True, b = user_input_dict['branch']) # otherwise clone from the specified branch by the user
    os.chdir(path)  # changes to temp directory
    return repo, path



api.add_resource(Run,'/run')
api.add_resource(get_commits, '/get_commits')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1',threaded = True)


# Create a temp directory, clone user repo into it, and list its contents                                                    
#if  os.path.isdir(path):  #removes any existing temp folder from previously failed runs                                       
#    rmtree(path)
#os.mkdir(path)

#if not user_input_dict['branch']:
#    repo = Repo.clone_from(gitURL, path) # clone from master
#else:
#    repo = Repo.clone_from(gitURL, path, single_branch = True, b = user_input_dict['branch']) # otherwise clone from the specified branch by the user


#os.chdir(path)  # changes to temp directory

#if (reader.parse_config('config.json') == -1):
#  print(reader.error)
#  sys.exit()
  
#test_cases = reader.test_dict
#if (reader.isolate_result_checks(test_cases) == -1):
#  print(reader.error)
#  sys.exit()
  
#output_list = reader.output_list
#assert_list = reader.assert_list
#exit_list = reader.exit_list
#result_list = [] # renamed Chao's assert_list to result_list because another assert_list was introduced above (see Issue 27 on Gitlab)

#i = 0
#for case in test_cases:
#    command = reader.get_build(test_cases[case])
#    result_list.append(True)
#        
#    if output_list[i] != None and assert_list[i] != None:
#        output = os.popen(command).read()[:-1]
#        exec('result_list[i] = (output'+assert_list[i]+"output_list[i])")
#        
#    if exit_list[i] != None:
#        output = os.system(command)
#        exec('result_list[i] = result_list[i] and output == exit_list[i]') # For the case of both output and exit comparison, combine the results
#    i += 1
#print(result_list)

#Generates a list of previous commit ID in which commitIDs[0] is the most recent successful one
#commitIDs = list(repo.iter_commits('HEAD', max_count = 5))
#i = 0
#for commit in commitIDs:
#    print( str(i) + ":::" + str(commit))
#    i += 1


# Current roll-back functionality (hard reset)

#if False in result_list: # if one of the test cases failed, revert to previous commit (at least for now!) 
#    print("I'm here!") # debugging; just to see when the if-statement gets invoked.
#    repo.git.reset('--hard', commitIDs[1]) # completely removes the last commit. New HEAD now is the previous commit.
#    if not user_input_dict['branch']:
#        repo.git.push('-f', gitURL)
#    else:
#        repo.git.push('-f', gitURL, user_input_dict['branch'])

    # REMARK:  We have to be cautious with reset and then push -f. See post by VonC at https://stackoverflow.com/questions/9804211/can-not-push-changes-after-using-git-reset-hard. It is dangerous if master or branch that we are pushing to has been fetched by someone else into their repos.

#os.chdir("..")

#rmtree(path)
