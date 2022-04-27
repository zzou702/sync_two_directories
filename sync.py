#!/usr/bin/env python3
from genericpath import exists
from importlib.resources import path
import json
from operator import mod
import os
import sys
import hashlib
import time



def check_directory():
    print(os.getcwd())

    if os.path.isdir(dir1) and os.path.isdir(dir2):
        return 1 # return 1 if both directories inputted exists
    elif (not os.path.isdir(dir1) and (not os.path.isdir(dir2))):
        return 2 # 2return 2 if none of the directories exists
    else:
        return 3 #return 3 if one of the diretory exists

def create_directory():
    if os.path.isdir(dir1) and (not os.path.isdir(dir2)):
        os.mkdir(dir2)
        return dir2
    elif os.path.isdir(dir2) and (not os.path.isdir(dir1)):
        os.mkdir(dir1)
        return dir1

# returns true if there is a sync file in the directory, 
def check_sync_file(directory):

    # to be implemented
    #loop through the directory for each files and check if there is a .sync.json file
    for file in os.listdir(directory):
        if file == ".sync.json":
            return True
    
    return False


def create_sync_file(directory):
    path_to_file = os.path.join(directory, ".sync.json")
    open(path_to_file, 'w')


# Iterate through the directory, checking if there is a sync file, and if there is subdirectories, and iterate through them
def iterate_directory(directory):

    for file in os.listdir(directory):
        #creating a temp file to maintain the full path name
        temp_file = os.path.join(directory, file)

        print(temp_file)

        # if the current file is a directory, iterate again
        if os.path.isdir(temp_file):
            iterate_directory(temp_file)
            
    # 
    if not check_sync_file(directory):
        create_sync_file(directory)


def hash_files(directory):
    for file in os.listdir(directory):
        #skipping past .sync.json file
        if file == ".sync.json":
            continue
        
        #creating a temp file to maintain the full path name
        temp_file = os.path.join(directory, file)

        # if the current file is a directory, iterate again
        if os.path.isdir(temp_file):
            iterate_directory(temp_file)

        print(temp_file)

        #get the modification time of the file
        mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getmtime(temp_file)))
        print(mod_time)

        # read the file in order to produce a hash value
        with open(temp_file, "rb") as f:
            bytes = f.read()
            file_hash = hashlib.sha256(bytes).hexdigest()
            print(file_hash)

        #storing the hash value into the json file - to be implemented
        



# main code
dir1 = os.path.join(os.getcwd(), sys.argv[1])
dir2 = os.path.join(os.getcwd(), sys.argv[2])

print(dir1, dir2)

dir_validity = check_directory()

# checking the validity of the inputted directories
if dir_validity == 1: # Both directories exist
    print("both exists")
    #checking for the sync files in the directories, if it dosn't exist, create one
    iterate_directory(dir1)
    iterate_directory(dir2)
    hash_files(dir1)
    hash_files(dir2)

elif dir_validity == 2:
    print("none exists")
    exit()
elif dir_validity == 3:
    print("one existes")
    # creating a new directory
    create_directory() 

    # if there is no sync files in the directory, create a new one
    iterate_directory(dir1)
    iterate_directory(dir2)

# read through