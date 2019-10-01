import os
from sys import argv
import re

try:
    from colored import fg
except:
    exit('Seems that you didn\'t install colored.\n Intall it with command:\npip install colored.')

try:
    main_path = argv[1]
except:
    exit('Error, first argument must be path.\nType:\n\ntree.py --help\n\nfor more inforamtion.')
all_paths = {}
file_color = fg('yellow')
dir_color = fg('blue')
tree_color = fg('green')
max_depth = 0
ignore_files = ''
ignore_dirs = ''
ignore_empty_dirs = False

if ('--help' in argv):
    help_str = f'''
tree.py is a program that can show you a tree of your folders and files

Uses python3 tree.py <path> [param] <value> [param] <value>

Params:

    --max_depth, <value:int> it is used to set maximum depth of drawing the tree

    --ignore_dirs, <value:string or regexp> it is used to ignore some directories
    that matches with regexp

    --ignore_files, <value:string or regexp> it is used to ignore some files
    that matches with regexp

    --ignore_empty_dirs, use it if you want to ignore empty directories
    '''
    print(help_str)
    exit()

if (not re.search('.*/.*', main_path)):
    exit('Error, first argument must be path.\nType:\n\ntree.py --help\n\nfor more inforamtion.')

if ('--max_depth' in argv):
    max_depth = int(argv[argv.index('--max_depth') + 1])

if ('--ignore_files' in argv):
    ignore_files = argv[argv.index('--ignore_files') + 1].strip('\'\'')

if ('--ignore_dirs' in argv):
    ignore_dirs = argv[argv.index('--ignore_dirs') + 1].strip('\'\'')

if ('--ignore_empty_dirs' in argv):
    ignore_empty_dirs = True

def collect_paths(path, deep, last=False):
    string = ''
    if (all_paths.get(path) is None):
        return string
    if (last):
        file_deep = deep - 1
        file_t = '  '
    else:
        file_deep = deep
        file_t = ''
    if (all_paths[path][0] == []):
        if (all_paths[path][1] != []):
            for i in all_paths[path][1][:-1]:
                string += tree_color + file_deep * '|  ' + file_t + '├──' + file_color + i + '\n'
            string += tree_color + file_deep * '|  ' + file_t + '└──' + file_color + all_paths[path][1][-1]
        return string
    else:
        is_there_files = False
        if (all_paths[path][1] != []):
            is_there_files = True
        if (not max_depth or max_depth >= deep + 1):
            for i in all_paths[path][0][:-1]:
                new_path = (path + '/' + i).replace('//', '/')
                if (all_paths.get(new_path) is None):
                    string += tree_color + deep * '|  ' + '├──' + dir_color + i + '\n'
                elif (all_paths[new_path][1] == []):
                    if (not ignore_empty_dirs):
                        string += tree_color + deep * '|  ' + '├──' + dir_color + i + '\n'
                else:            
                    string += tree_color + deep * '|  ' + '├──' + dir_color + i + '\n' + collect_paths(new_path, deep + 1) + '\n'
            new_path = (path + '/' + all_paths[path][0][-1]).replace('//', '/')    
            string += tree_color + deep * '|  ' + '└──' + dir_color + all_paths[path][0][-1] + '\n' + collect_paths(new_path, deep + 1, not is_there_files) + ('\n' if all_paths[path][1] != [] else '')
        if (is_there_files):
            for i in all_paths[path][1][:-1]:
                string += tree_color + deep * '|  ' + '├──' + file_color + i + '\n'
            string += tree_color + deep * '|  ' + '└──' + file_color + all_paths[path][1][-1]
        return string 
    


for path, dirs, files in os.walk(main_path):
    if (len(ignore_dirs)):
        dirs = [folder for folder in dirs if not re.search(ignore_dirs, folder)] 
    if (ignore_files != ''):
        files = [f for f in files if not re.search(ignore_files, f)] 
    all_paths[path] = (dirs, files)
    


print(collect_paths(main_path, 0))
