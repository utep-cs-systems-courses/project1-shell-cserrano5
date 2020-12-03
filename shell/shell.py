

# Crystal Serrano
# Lab 1
# Collaborated with classmates through online meetings
#

#! usr/bin/env python3

import os, sys, re

# function receives array and executes ls command to change directory, cd and cd .. work
def change_directory(input_arr):
    try:
        os.chdir(input_arr[1])
    except FileNotFoundError:
        # os.write(1, ("cd: %s: No such file or directory exists\n" % input_arr[1]).encode())
        pass


# function receives array to operate redirections > and < (output & input)
def redirect(redirect_arr):
    # redirect output
    if '>' in redirect_arr:
        os.close(1)  # closes file descriptor 1, redirects child's stdout
        # open output file for writing
        # if file doesnt exist, create flag will create file, if it does exist, then it'll be written in to
        os.open(redirect_arr[redirect_arr.index('>')+1], os.O_CREAT | os.O_WRONLY)  # create and write only flags
        # file descriptor flag is to be set to ensure fd 1 is inheritable
        os.set_inheritable(1, True)
        exec_command(redirect_arr[0:redirect_arr.index('>')])
    else:
        # redirect input
        os.close(0)  # closes file descriptor 0, disconnect keyboard
        # open input file for reading
        os.open(redirect_arr[redirect_arr.index('<'+1), os.O_RDONLY])
        os.set_inheritable(0, True)  # ensure fd 0 is inheritable
        exec_command(redirect_arr[0:redirect_arr('<')])


# function receives array and executes the command
def exec_command(input):
    for dir in re.split(":", os.environ['PATH']): # tries each directory in path
        program = "%s/%s" % (dir, input[0])
        try:
            os.execve(program, input, os.environ) # try to exec program
        except FileNotFoundError:
            pass  # fail quietly
    os.write(2, ("Command: '%s' not found." % input[0]).encode())
    sys.exit(1)  # terminate with error


# shell
while True:
    # prompts user with $ to indicate they're in the shell and prints path
    p = os.getcwd() + ' $' if 'PS1' not in os.environ else os.environ['PS1']
    os.write(1, p.encode())
    # gets the users input
    try:
        # .split() removes any leading or trailing empty spaces
        user_input_str = input().strip()
        # will split users input into an array
        input_arr = user_input_str.split()
    except EOFError:
        sys.exit(1)  # terminate with error

    if "exit" in input_arr:
        # exits the shell
        sys.exit(0)

    if "cd" in input_arr[0]:
        # changes directory command: ls, cd, cd ..
        change_directory(input_arr)

    elif '|' in input_arr:
        # uses pipe command
        #pipe(input_arr) need to creat pipe function

    else:
        rc = os.fork()
        if rc < 0:
            os.write(2, ('Fork failed.\n' % rc).encode())
            sys.exit(1)  # terminate with error
        elif rc == 0:
            if '/' in input_arr[0]:
                try:
                    os.execve(input_arr[0], input_arr, os.environ)   # tries to execute program
                except FileNotFoundError:
                    pass
            # redirection
            elif '>' in input_arr or '<' in input_arr:
                redirect(input_arr)
            else:
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s" % (dir, input_arr[0])
                    try:
                        os.execve(program, input_arr, os.environ)
                    except FileNotFoundError:
                        pass
