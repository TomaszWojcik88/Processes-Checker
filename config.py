#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from os import path



#############
### PATHS ###
#############

# PATHS TO SCRIPT #
folder_to_processes_files = 'hostnames/' #DO NOT CHANGE VALUE
path_to_script = path.dirname(path.realpath(__file__)) # PATH TO SCRIPT GATHERED FROM FUNCTION. DO NOT CHANGE VALUE
# MENU PATHS #
path_menu = path.join( path_to_script, 'menu/menu.py') # DO NOT CHANGE VALUE
path_menu_text = path.join( path_to_script, 'menu/menu_text.py') # DO NOT CHANGE VALUE
path_menu_signs = path.join( path_to_script, 'menu/menu_signs.py') # DO NOT CHANGE VALUE



####################################################
### PS COMMAND - FOR GATHERING LIST OF PROCESSES ###
####################################################

use_psutil_library = True # IF SET TO TRUE, INSTEAD OF USING PS COMMAND FROM SYSTEM, WILL USE PSUTIL LIBRARY FOR GATHERING PROCESSES. bEFORE SET TO TRUE, PSUTIL LIBRARY NEED TO BE INSTALLED FOR PYTHON
ps_command = 'ps -ef' # COMMAND PS THAT WILL GATHER ALL WORKING PROCESSES
column_with_pid_for_ps_command = 1 # COLUMN 2 (COUNTED FROM 0) CONTAINS PID NUMBER // COLUMN IS PART OF OUTPUT FROM PS COMMAND, WHERE COLUMN 2 REPRESENTS PID NUMBER OF EACH LISTED PROCESS



#################################
### CUSTOM LISTS OF PROCESSES ###
#################################

psutil_library = 'psultil library' # BETTER DO NOT CHANGE VALUE
ps_commands = {
				psutil_library: 0, # BETTER DO NOT CHANGE VALUE
				'ps -ef': 1, # PROCESS COMMAND, COLUMN NUMBER OF PID
				'ps -fu root': 1, # TOMEK HERE IS USER NAME
				}
folder_custom_processes_list = 'custom'



#############################
### SHOW PATH TO LOGFILES ###
#############################

how_many_path_to_logs_show_in_show_log_paths_function = 2



######################################
### CHECKING FOR ERROR IN LOGFILES ###
######################################

how_many_last_file_logs_to_check = 1  # NUMBER TELLS HOW MANY LOG FILES TO CHECK OF ONE PROCESS, BEGINNING FROM YOUNGER FILE
# LIST CONTAINS ERROR PHRASES THAT WILL CHECK EACH LINE IN LOG FILES
logs_error_patterns_list = [
						'Error',
						'No connection'
						]



##################
### PANIC KILL ###
##################

command_kill = 'kill -9 ' # COMMAND TO KILL IMMEDIETLY PROCESSES



###########
### TOP ###
###########

refresh_interwal_in_seconds = 10
command_clear = 'clear' # COMMAND FOR BASH TO CLEAR SCREEN



############################
### BACKGROUN MONITORING ###
############################

# FUNCTION BASIC CONFIG #
check_processes_each_how_many_seconds = 5
when_found_broken_processes_next_check_in_seconds = 60 # WHEN FUNCTION FIND BROKEN PROCESS AND SENT MAIL, HERE IS AN INTERVAL BETWEEN NEXT CHECK
# GENERAL VARIABLE NEED TO SENT MAIL
receivers = [ 'tomasz.wojcik.88@gmail.com' ]
subject = 'WARNING! On Hostname %s Some of processes are not working'
# VARIABLE NEED FOR SMTPLIB
use_python_smtplib = True
sender = 'tomasz.wojcik.88@gmail.com'
sender_password = 'Password'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
# VARIABLE NEED FOR MAILX #
use_mailx = False
sent_body_file_name = 'mail_body'



####################################
### CREATE START AND STOP SCRIPT ###
####################################

start_script_name = 'start_script.sh' # NAME OF CREATED START SCRIPT
stop_script_name = 'stop_script.sh' # NAME OF CREATED STOP SCRIPT
header_script_declaration = '#!/bin/bash' # EACH LINUX PROMPT SCRIPT NEED BASH / KSH DECLARATION IN HEADER FILE
access_rights_to_scipt = 777 # HERE YOU CAN CHANGE PERMISSIONS TO CREATED FILE
owner_of_the_script = 'root' # SET HERE USERNAME THAT SHOULD ME OWNER OF CREATED SCRIPT, OR LEFT EMPTY (THEN WILL NOT CHANGE OWNER)
break_between_each_start_stop_command_in_seconds = 1 # BREAK BETWEEN EACH START / STOP COOMMAND PERFORMATION # SET 0 TO OMMIT BREAK COMMAND
command_echo = 'echo' # DO NOT CHANGE VALUE
command_sleep = 'sleep' # DO NOT CHANGE VALUE