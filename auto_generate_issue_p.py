"""
Import modules
"""

from os import listdir
from os.path import isfile, join
from itertools import cycle
import re
import requests
import json
import ast
from PyPDF2 import PdfReader
from pprint import pprint
import time, datetime



"""
Read attached pdf using PyPDF2, define variables for importing
"""

reader = ''
reader = PdfReader("issue_template.pdf")
dict = reader.get_form_text_fields()

# print(dict['labels'] + '\n\n\n')



"""
Create json_template body then head
"""

def create_json_template(FILE_NAME, FILE_ACTION):

    before = "```\n" + FILE_ACTION[0] + "\n```"
    after = "```\n" + FILE_ACTION[1] + "\n```"
    INSERT = before + '\nto:\n' + after
    # pprint(INSERT)


    """
    Create body of template
    """ 
    DEPENDENCY = '### Dependency\n' + dict['dependency'] if dict['dependency'] else ''
    DETAILS = '### Details\n' + dict['details'] if dict['details'] else ''
    ACTIONS = (dict['action_items']).replace('{FILE_NAME}', FILE_NAME).replace('{FILE_ACTION}', INSERT)
    RESOURCES = (dict['resources'])

    body = f"""
### Prerequisites
  1. You must be a member of Hack for LA to work on an issue. If you have not joined yet, please follow the steps on our [Getting Started](https://www.hackforla.org/getting-started) page.
  2. Please make sure you have read our Hack for LA [Contributing Guide](https://github.com/hackforla/website/blob/gh-pages/CONTRIBUTING.md) before you claim/start working on an issue.
{DEPENDENCY}
{DETAILS}
### Overview
{dict['overview']}
### Action Items
{ACTIONS}
### Resources/Instructions
{RESOURCES}
"""
    body_lines = ''
    for line in body.splitlines():
        # body_lines += line + '\\' + '\\n'
        body_lines += line +  '\\n'
    

    """
    Create head of template
    """
    TITLE = '"' + dict['title'].replace('{FILE_NAME}', FILE_NAME) + '"'
    LABELS = (dict['labels'])

    json_template = f'''
"title": {TITLE},
"labels": [
    {LABELS}
    ],
"body": 
'''   
    json_template += '"'+body_lines+'"'
    
    return json_template



"""
Generate unique template
"""

saved_templates = []
all_files = ast.literal_eval(str(dict["file_info"]))

for k, v in all_files.items():
    saved_templates.append(create_json_template(k, v))



def generate_issue(num):

    token = dict['secret']
    headers = {"Authorization": "token {}".format(token)}
    data = ast.literal_eval('{'+saved_templates[int(num)]+'}')

 
    # Sleeps for x seconds between generating issues
    def countdown(secs):

        i = 0
        while secs > 0:

            # Prints the timer
            print('HOLDING' + '.' * i, end='\r')
            
            # Delays the program and decrements by quarter second
            time.sleep(.25)
            secs -= .25
            i += 1

        print('HOLDING' + '.' * i +'Ready!')
        print(f'Generating issue {num} of total {len(saved_templates)}:', '\r')

    countdown(7)

        
    
    url = f"https://api.github.com/repos/{repo}/website/issues"
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 201:
        print(f"Success! Created issue {num} of {len(saved_templates)}")
    # print(response.content)




""""
FUTURE 
"""
repo = str(dict['github_handle']) 
repo_qstn = True
while repo_qstn:
    
    repo_qstn = input(f'The working repo is set to: {repo}. Do you want to switch? ')
    repo = str(dict['github_handle']) if repo_qstn.lower() == 'n' else 'hackforla'
    print(repo)
    break



"""
Generate the issues
"""
response = False
while response:

    which_one = input(f"\n\nPrepare which number (0 to {len(saved_templates)-1}, [A]ll, or e[x]it)? ")
    try:
        if which_one == 'x':
            break
        which = int(which_one)
        if which >= 0 and which < len(saved_templates):
            print(f'Displaying template {which_one}\n')
        elif which_one == 'A':
            proceed = input('Generating All- are you sure? ')
            if proceed.lower() == 'y':
                for num in range(len(saved_templates)):
                    generate_issue(num)
                print('Finished!')
                break
        else:
            raise ValueError
    except ValueError:
        print('Retry or e[x]it: ')
  
    pprint(saved_templates[which])
    rvw_temp = input(f'\nThis is the template that will be generated in {repo}\nContinue to generate issue? ')
    if rvw_temp.lower() == 'y':
        generate_issue(which)
    else:
        qstn = input(f'Enter [y]es to start over or e[x]it: ')
        if qstn.lower() == 'y':
            continue
        else:
            break
