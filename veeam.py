# Importing the dependencies
import os
import time
import shutil
import logging
import hashlib

# Function to calculate the hash of a file
def hash_cal(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  #The number is representing bytes: 65536 bytes = 64 kilobytes. This is memory dependant, so for higher "jobs" it requires more memory, but it's faster, lower values will take less memory, but it's slower
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Asking for the path of the log file 
log_path = input("Please enter the full path for the log file: ")

# The basic configuration for the log file with the DEBUG level, format of how the log is displayed, and the handlers that take care of the logs in the file and console
# All logging.info and logging.error in this code are used to push the logs to the log file and console
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    handlers=[
                        logging.FileHandler(f"{log_path}.log"),
                        logging.StreamHandler()
                             ]
                    )

# Getting the path for the main folder
path1 = input(f"Please provide the path of the main folder: ")
logging.info(f"Main folder: {path1}")

# Getting the path for the destination folder
path2 = input(f"Please provide the path of the destination folder: ")
logging.info(f"Destination folder: {path2} ")

# Getting the time in second for the sync period
perd_sync = int(input("Enter the synchronization period in seconds: "))
logging.info(f"Synchronization period: {perd_sync} seconds")

# If the path of the main folder is not found, inform user and exit
if not os.path.exists(path1):
    logging.error(f"The path of the main folder is not correct or it does not exist")
    exit(1)
# If the path of the destination folder is not found, inform user and exit
elif not os.path.exists(path2):
    logging.error(f"The path of the destination folder is not correct or it does not exist")
    exit(1)

while True:
    try:
        #This will check all directories in the main folder and subfolders (Filenames is not used)
        for dirpath, dirnames, filenames in os.walk(path1):
            for name in dirnames:
                main = os.path.join(dirpath, name)
                relative_filepath = os.path.relpath(main, path1)
                destination = os.path.join(path2, relative_filepath)

                # This will create a new directory in case it does not exist (Had to do it because it was not reading the new folders, and only copied them in case there was a file inside that folder)
                if not os.path.exists(destination):
                    os.makedirs(destination)
                    logging.info(f"Created directory {destination}")

        # This will check all files in the main folders and subfolders (Remember the dif between directories and folders)(dirnames is not used)
        for dirpath, dirnames, filenames in os.walk(path1):
            for file in filenames:
                main = os.path.join(dirpath, file)
                relative_filepath = os.path.relpath(main, path1)
                destination = os.path.join(path2, relative_filepath)

                # Only to copy if the file does not exist in the destination or it has a different hash
                if not os.path.exists(destination) or hash_cal(main) != hash_cal(destination):
                    shutil.copy2(main, destination)
                    logging.info(f"Copied file {main} to {destination}")

        # Delete files in the destination folder that do not exist in the main folder
        for dirpath, dirnames, filenames in os.walk(path2):
            for file in filenames:
                destination = os.path.join(dirpath, file)
                relative_filepath = os.path.relpath(destination, path2)
                main = os.path.join(path1, relative_filepath)

                if not os.path.exists(main):
                    os.remove(destination)
                    logging.info(f"Deleted file {destination}")

        #This is an option to stop deleting files in the destination folder that do not exist in the main folder (Will need to comment the lines 80 to 88 before uncommeting this code)
       #for dirpath, dirnames, filenames in os.walk(path2):
            #for filename in filenames:
                #destination = os.path.join(dirpath, filename)
                #relative_filepath = os.path.relpath(destination, path2)
                #main = os.path.join(path1, relative_filepath)

                #if not os.path.exists(main):
                    #logging.info(f"File {destination} does not exist in main folder")

        # Delete directories in the destination folder that do not exist in the main folder (in case the deletion for directories is not needed in the destination folder, comment out this code )
        for dirpath, dirnames, _ in os.walk(path2, topdown=False):  
            for name in dirnames:
                destination = os.path.join(dirpath, name)
                relative_filepath = os.path.relpath(destination, path2)
                main = os.path.join(path1, relative_filepath)

                if not os.path.exists(main):
                    os.rmdir(destination)
                    logging.info(f"Deleted directory {destination}")

        logging.info(f"Synchronized {path1} to {path2}")
    except Exception as error:
        logging.error(f"Error synchronizing directories: {error}")

    time.sleep(perd_sync)
