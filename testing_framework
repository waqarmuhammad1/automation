import json

class JASON_HANDLER():

    def write_dict_to_jaosn(self,data_dict):
        with open('TestCaseResult.json', 'w') as fp:

            json.dump(data_dict, fp, indent=4, sort_keys=True)


if __name__=='__main__':
    test_results = {"Test Case1": {"File": "TestFramework.py", "Function": "getTriangle()", "Input": ['5', '3', '4'],
                              "Output": "Scalene", "Error": "0", "Status": "Pass"},
               "Test Case2": {"File": "TestFramework.py", "Function": "getTriangleType()", "Input": ['5', '5', '0'],
                              "Output": "", "Error": "Side length cannot be zero", "Status": "Fail"}}

    obj_JasonHandler = JASON_HANDLER()
    obj_JasonHandler.write_dict_to_jaosn(test_results)
    print('successfully saved')
