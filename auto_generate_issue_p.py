import requests
import json
import ast
from PyPDF2 import PdfReader
from pprint import pprint
from pathlib import Path
from countdown import countdown

# from itertools import cycle
# from os import listdir
# from os.path import isfile, join
# import re




def read_pdf_template(pdf_template):
    """
    Read attached pdf using PyPDF2, define variables for importing
    """
    reader = ''
    reader = PdfReader(pdf_template)

    global dict
    dict = reader.get_form_text_fields()



def evaluate_template():
    """
    Evaluate imported pdf, generate unique templates
    """
    saved_templates = []
    all_files = ast.literal_eval(str(dict["file_info"]))
    pprint(all_files)
    for k, v in all_files.items():
        saved_templates.append(create_json_template(k, v))

    return saved_templates


def create_json_template(FILE_NAME, temp_value):
    """
    Create json_template using imported values
    """
    BEFORE = temp_value[0]
    AFTER = temp_value[1]


    """
    Create body of template
    """ 
    DEPENDENCY = f"### Dependency \n{dict['dependency']}" if dict['dependency'] else ""
    DETAILS = f"### Details \n{dict['details']}" if dict['details'] else ""
    ACTIONS = (dict['action_items']).replace('{FILE_NAME}', FILE_NAME).replace('{BEFORE}', BEFORE).replace('{AFTER}', AFTER)
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
        body_lines += line + '\\n'
    

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



def set_repo():

    global repo
    repo = str(dict['github_handle']) 
    repo_qstn = True
    while repo_qstn:
        
        repo_qstn = input(f'The working repo is set to: {repo}. Switch? ')
        repo = str(dict['github_handle']) if repo_qstn.lower() == 'n' else 'hackforla'
        print(f'Proceeding with working repo: {repo}')
        break



def generate_issue(num):

    token = dict['secret']
    headers = {"Authorization": "token {}".format(token)}
    data = ast.literal_eval('{'+saved_templates[int(num)]+'}')

    countdown(5)
    print(f'Generating issue {num} of total {len(saved_templates)}:', '\r')
        
    # Script to create issue
    url = f"https://api.github.com/repos/{repo}/website/issues"
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 201:
        print(f"Success! Created issue {num} of {len(saved_templates)}")
    # print(response.content)






    

def main():
    """
    Program that reads input from a specific PDF form, prepares data in markdown format,
    then sends to GitHub for creation of a new issue in user-specified repo 
    """
    print('Issue Generator')

    
    pdf_template = "issue_template_blank.pdf"

    """
    --> TO DO (optionally) Code to allow change to pdf template file, search, etc.
    while True:
        print(f'Ready to read PDF Template: \"{pdf_template}\"')
        pdf_qstn = input('Enter any key to proceed, or \"c\" to change: ')
        if pdf_qstn.lower() == 'c':
            pdf_ans = input("Enter new name of PDF template: ")
            if Path(pdf_ans).suffix == '.pdf' and Path(pdf_ans).is_file():
                pdf_template = pdf_ans
            else:
                print('Entry not valid. Using default')
        break
    """

    
    read_pdf_template(pdf_template)
    set_repo()
    saved_templates = evaluate_template()
    

    

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


if __name__ == "__main__":
    main()