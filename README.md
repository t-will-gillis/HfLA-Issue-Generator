# HfLA-Issue-Generator
Python &amp; PDF for generating multiple issues at same time

## Copy files to your local repo
1. Make sure you have Python installed locally or this won't run. (At least yet.)
2. Copy both the `auto_generate_issue_p.py` and `issue_template_blank.pdf` to your local.
   
## Enter data in the PDF
Refer to the example template below:

1. Input your GitHub handle
2. Enter the secret for your repo
3. Enter the labels you want on the issues to be generated. Make sure labels match HfLA's repo, place in quotes, comma-separate, and enter in a continuous line.
4. This is the project payload. It is a dictionary that consists of the name of each file that needs to be changed, plus the before and after changes, again with punctuation as shown and written continuously (no newlines):  
    `{ "filename_1.exp":(before, after), "filename_2.exp":(before, after), "filename_3.exp: (before, after) }`
   This dictionary will populate the {FILE_NAME} and {FILE_ACTION} variables for each separate issue. See following.
5. Input the title and use the exact reference {FILE_NAME} so that your issues will each be generated with a unique title:  
    `This is the title of my issue for {FILE_NAME}` 
6. If you need the 'Dependency' section, enter markdown text here. If not, completely delete and it won't show up. Note that until you generate the final issues, you will want to use `#xxxx` as the dependency. If you use the actual dependency's issue number, each of your test issues will be linked to the actual dependency.
7. If you need the 'Details' section, enter markdown text here. If not, completely delete and it won't show up.
8. Enter the 'Overview' section using markdown formatting. In this example, note that due to internal formatting the quotes are escaped for "Tools", and the values `tools` and `technologies` have **triple** backticks.
9. Enter the 'Action Items' using markdown formatting. Note to make sure you have the correct path to the {FILE_NAME} and use the {FILE_ACTION} variable.  FILE_ACTION[0] == before, FILE_ACTION[1] == after.
10. Enter the 'Resources / Instructions' using standard markdown text.  

11. When you are done, save the PDF with a unique name, and make sure line 23 of the .py file references the correct .pdf file name.
    
![issue_template_ex_4777](https://github.com/t-will-gillis/HfLA-Issue-Generator/assets/40799239/92748787-e229-49de-a897-ae6f6843cb55)

## Run the Python file
Run this like a typical python file, i.e. `python auto_generate_issue_p.py`. The interface is self-explanatory, and you will probably need to troubleshoot.

## Additional features 
Additional features might be coming, if there seems to be interest... Some possibilities:
- [ ] Trigger this from a GitHub Action
- [x] ~Include dropdown, multiselection list prepopulated with all of HfLA's labels.~
- [ ] Revise {FILE_ACTION} into {BEFORE} and {AFTER}
- [ ] Attach Python file for searching HfLA's website, and returning a list of filenames matching features that need to change, along with the existing/ BEFORE and the intended final/ AFTER states.
