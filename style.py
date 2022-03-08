#!/usr/local/bin/python
# -*- coding: utf-8 -*-



###############################
### COLORS (WORKS FOR BASH) ###
###############################

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;35m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
ORANGE= '\033[1;31m'
NC='\033[0m'



################
### STATUSES ###
################
# STATUS SHOULD NOT BE LONGER THAN 21 SIGNS #
### LOG STATUSES ###
status_log_file_not_exist = ' - LOGS NOT EXISTS'
status_log_file_short_not_updating = ' - NOT UPDATING SHORT'
status_log_file_not_updating = ' - NOT UPDATING LONG'
status_log_file_ok = 'LOGS UPDATING'

### PROCESSES STATUSES ###
status_process_ok = 'OK'
status_process_bad = 'BAD'



#################################
### SIGNS - BETTER NOT CHANGE ###
#################################

sign_newline_double = '\n\n'
sing_newline = '\n'
sign_minus_space = ' - '
sign_slash = '/'
sign_star = '*'
sign_space = ' '
sign_semicolon = ';'
sign_colon_space = ': '
sign_pipe = '|'
sign_space_double = '  '
sign_apostrophe = '"'
sign_equal = '='
sign_fullfill = '%s'



##################################################
### HEADER AND FORMAT OUTPUT FOR MAIN FUNCTION ###
##################################################

main_function_header = '|      PROCESS NAME      |INSTANCES| STATUS |LOG UPDATE|'
main_function_one_line_format = '  %20.20s  | %7s | %6.6s | %8s '
main_function_logfile_datetime_format = '%H:%M:%S'



###############################
### PRINT PATHS TO LOGFILES ###
###############################

process_logfile_header = '  %23s  | Last update: | %19.19s '
process_logfile_one_line_format = '|  %60s  |'
date_status_unknown = 'UNKNOWN'
one_line_length = 66
logfile_datetim_format = '%Y/%m/%d %H:%M:%S'



############################
### BACKGROUN MONITORING ###
############################

mail_header = '| INSTANCES  | LAST UPDATE ON LOGS | PROCESS NAME \n'
mail_one_line_format = '|  %3i / %3i | %8s / %8s |  %s \n'



