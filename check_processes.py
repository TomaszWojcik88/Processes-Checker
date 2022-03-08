#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from os import path as os_path, listdir as os_listdir, stat as os_stat, system as os_system, chmod as os_chmod, chown as os_chown
from sys import path as sys_path, argv as sys_argv, exit as sys_exit
from socket import gethostname as socket_gethostname
from datetime import datetime, timedelta
from subprocess import Popen, PIPE, STDOUT
from pwd import getpwnam 
import psutil
import argparse
# INTERNAL LIBRARIES #
import config, text, style
GREEN, BLUE, RED, YELLOW, CYAN, ORANGE, NC = style.GREEN, style.BLUE, style.RED, style.YELLOW, style.CYAN, style.ORANGE, style.NC



class Process(object):

	def __init__(self, name, pattern, number_of_instances, start_command, end_command, log_path, log_update, do_check_for_errors_in_logfile):
		self.name = name
		self.pattern = pattern
		self.number_of_instances = number_of_instances
		self.start_command = start_command
		self.end_command = end_command
		self.log_path = log_path
		self.log_update = log_update
		self.do_check_for_errors_in_logfile = do_check_for_errors_in_logfile



class GroupProcess(object):

	def __init__(self, group_name):
		self.group_name = group_name
		self.processes_list = list()



class CheckProcesses(object):

	list_of_processes_to_check = list()
	list_of_processes_on_current_hostname = list()


	################################
	### LOAD PROCESSES FROM FILE ###
	################################

	def load_processes_list(self, custom_file=False):
		# CHECK IF FILE EXIST FOR CURRENT HOSTNAME #
		if not custom_file:
			files_of_hostnames = os_listdir( os_path.join( config.path_to_script, config.folder_to_processes_files ) )
			current_hostname_name = socket_gethostname()
			current_hostname_file = None
			for file_hostname in files_of_hostnames:
				if current_hostname_name in file_hostname:
					current_hostname_file = file_hostname
			# IF FILE EXIST THEN GATHER FILE TO DATABASE
			if not current_hostname_file:
				sys_exit( ''.join([ style.sign_newline_double, text.text_15, style.sign_newline_double ]) )
		if custom_file:
			current_hostname_file = custom_file
		with open( os_path.join( config.path_to_script, config.folder_to_processes_files, current_hostname_file ), 'r' ) as current_hostname_file_opened:
			counter = 0
			for line in current_hostname_file_opened:
				counter += 1
				if counter == 1 or counter == 2 or counter == 3: continue # SKIP HEADER LINES
				line = line.rstrip('\r\n')
				process_array = line.split(style.sign_semicolon)
				# BELOW LINE WILL SKIP EMPPTY LINES #
				if not process_array[0] and not process_array[1] and not process_array[2] and not process_array[3] and not process_array[4] and not process_array[5] and not process_array[6] and not process_array[7]: continue
				if not process_array[1] and not process_array[2] and not process_array[6]:
					self.list_of_processes_to_check.append(GroupProcess(process_array[0]))
				else:
					if not process_array[0]: sys_exit( ( ''.join(style.sign_fullfill, style.sign_minus_space, text.text_16) % process_array[0] ) )
					if not process_array[1]: sys_exit( ( ''.join(style.sign_fullfill, style.sign_minus_space, text.text_17) % process_array[0] ) )
					if not process_array[2]: sys_exit( ( ''.join(style.sign_fullfill, style.sign_minus_space, text.text_18) % process_array[0] ) )
					if not process_array[6]: sys_exit( ( ''.join(style.sign_fullfill, style.sign_minus_space, text.text_19) % process_array[0] ) )
					start_command = None
					end_command = None
					log_path = None
					do_check_for_errors_in_logfile = False
					if process_array[3]: start_command = process_array[3]
					if process_array[4]: end_command = process_array[4]
					if process_array[5]: log_path = process_array[5]
					if process_array[7] == 'Y': do_check_for_errors_in_logfile = True
					process = Process( process_array[0], process_array[1], int(process_array[2]), start_command, end_command, log_path, int(process_array[6]), do_check_for_errors_in_logfile )
					self.list_of_processes_to_check[-1].processes_list.append(process)



	##############
	### HEADER ###
	##############

	def header_preparator(self, group_name):
		space_number = int( ( len(style.main_function_header) - len(group_name) ) /2 )
		space_number_2 = space_number -1
		if len(group_name) % 2 == 0: space_number -= 1
		self.output += ''.join([ style.sign_star*len(style.main_function_header), style.sing_newline , style.sign_pipe, style.sign_space*space_number, group_name,
									style.sign_space*space_number_2, style.sign_pipe, style.sing_newline, style.sign_star*len(style.main_function_header), style.sing_newline ])



	##############
	### COLORS ###
	##############

	def no_color(self):
		global GREEN
		GREEN = ''
		global BLUE
		BLUE = ''
		global RED
		RED = ''
		global YELLOW
		YELLOW = ''
		global CYAN
		CYAN = ''
		global ORANGE
		ORANGE = ''
		global NC
		NC = ''

	def color(self):
		global GREEN
		GREEN = style.GREEN
		global BLUE
		BLUE = style.BLUE
		global RED
		RED = style.RED
		global YELLOW
		YELLOW = style.YELLOW
		global CYAN
		CYAN = style.CYAN
		global ORANGE
		ORAGNE = style.ORANGE
		global NC
		NC = style.NC



	############################################
	### MAIN FUNCTIONALITY - CHECK PROCESSES ###
	############################################

	### LIST CURRENTLY WORKING PROCESSES ###
	def list_currently_working_processes(self, ps_command, pid_field):
		# USE PSUTIL #
		if config.use_psutil_library or ps_command == config.psutil_library:
			try:
				list_of_processes_on_current_hostname = list()
				for process in psutil.process_iter():
					if not process.cmdline():
						list_of_processes_on_current_hostname.append( ' '.join([ str(process.pid), str(process.name()) ])  )
					else:
						list_of_processes_on_current_hostname.append( ' '.join([ str(process.pid), str(' '.join(process.cmdline())) ]) )
				self.list_of_processes_on_current_hostname = list_of_processes_on_current_hostname
				self.pid_field = 0
			except ImportError as error:
				sys_exit(''.join([ style.sing_newline, text.text_26, style.sing_newline ]))
		# USE SYSTEM PS COMMAND #
		else:
			self.pid_field = pid_field
			try:
				p = Popen(ps_command.split( ), stdout=PIPE, stderr=STDOUT)
			except OSError:
				sys_exit(''.join([ style.sing_newline, text.text_13, style.sign_apostrophe, ps_command, style.sign_apostrophe, style.sign_space,  style.sing_newline ]) )
			list_of_processes_on_current_hostname = list()
			for line in p.stdout:
				line = line.strip()
				list_of_processes_on_current_hostname.append(str(line))
			self.list_of_processes_on_current_hostname = list_of_processes_on_current_hostname


	### MAIN FUNCTION ###
	def check_processes(self):
		self.output = ''.join([ style.sing_newline, style.sign_star*len(style.main_function_header), style.sing_newline, style.main_function_header, style.sing_newline ])
		for process_group in self.list_of_processes_to_check:
			self.header_preparator(process_group.group_name)
			for process in process_group.processes_list:
				log_time, log_status, log_color = '', '', ''
				how_many_times_is_running_process = 0
				for line in self.list_of_processes_on_current_hostname:
					if process.pattern in line: how_many_times_is_running_process += 1
				status, status_color, command = None, None, ''
				if how_many_times_is_running_process == 0:
					status, status_color = style.status_process_bad, RED
					if process.start_command: command = process.start_command
				elif how_many_times_is_running_process == process.number_of_instances:
					status, status_color = style.status_process_ok, GREEN
					log_time, log_status, log_color = self.check_update_on_logfile(process)
				elif how_many_times_is_running_process < process.number_of_instances:
					status, status_color = style.status_process_all_few_bad, ORANGE
					if process.start_command and process.end_command: command = style.sign_semicolon.join([ process.end_command, process.start_command ])
				elif how_many_times_is_running_process > process.number_of_instances:
					status, status_color = style.status_process_bad, YELLOW
				self.format_output_line( process.name, how_many_times_is_running_process, process.number_of_instances, status, status_color, log_time, log_status, log_color, command)
		# PRESENT OUTPUT #
		self.output += ''.join([ style.sign_star*len(style.main_function_header), style.sing_newline ])
		print ( self.output )


	### ADDITIONAL LIBRARIES ###
	def check_update_on_logfile(self, process):
		if process.log_update > 0:
			final_path_to_log = ''
			path, file = os_path.split(process.log_path)
			if not os_path.exists(path):
				return '', style.status_log_file_not_exist, RED
			path_listed_elements = os_listdir( path )
			path_listed_elements.sort( key = lambda x: os_path.getmtime( os_path.join( path, x ) ), reverse=True )
			for file_name in path_listed_elements:
				if file in file_name:
					final_path_to_log = os_path.join( path, file_name )
					break
			else: return '', style.status_log_file_not_exist, RED
			last_logfile_date = datetime.fromtimestamp( os_stat( final_path_to_log ).st_mtime )
			now_minus_time = datetime.now() - timedelta( seconds=process.log_update )
			half_of_minut_time = datetime.now() - timedelta( seconds=( process.log_update / 2 ) )
			if last_logfile_date > now_minus_time:
				return last_logfile_date.strftime(style.main_function_logfile_datetime_format), style.status_log_file_ok, GREEN
			elif last_logfile_date > half_of_minut_time:
				return last_logfile_date.strftime(style.main_function_logfile_datetime_format), style.status_log_file_short_not_updating, YELLOW
			elif last_logfile_date < now_minus_time:
				return last_logfile_date.strftime(style.main_function_logfile_datetime_format), style.status_log_file_not_updating, RED
		else: return '', '', ''

	def format_output_line(self, process_name, how_many_runtimes, how_many_times_should_run, process_status, process_status_color, log_time, log_status, log_status_color, command):
		one_line = ''.join([ (style.main_function_one_line_format %
								( process_name, style.sign_slash.join([ str(how_many_runtimes), str(how_many_times_should_run) ]), process_status, log_time ) ) ])
		one_line_array = one_line.split(style.sign_pipe)
		# FORMATTING DATA #
		# RUNTIMES #
		runtimes_color = None
		if how_many_runtimes == how_many_times_should_run:
			runtimes_color = CYAN
		elif how_many_runtimes == 0:
			runtimes_color = RED
		elif how_many_runtimes < how_many_times_should_run:
			runtimes_color = ORANGE
		elif how_many_runtimes > how_many_times_should_run:
			runtimes_color = YELLOW
		runtimes_array = str(one_line_array[1]).split(style.sign_slash)
		runtimes = ''.join([ runtimes_color, runtimes_array[0], NC, style.sign_slash, CYAN, runtimes_array[1], NC ])
		# PROCESS #
		status = ''.join([ process_status_color, one_line_array[2], NC ])
		# UPDATES ON LOG FILES #
		log_time = ''.join([ log_status_color, one_line_array[3], NC ])
		# COMMAND OR LOG STATUS #
		if not command:
			command = ''.join([ log_status_color, log_status, NC ])
		# PRESENT DATA #
		self.output += ''.join([ style.sign_pipe, one_line_array[0], style.sign_pipe, runtimes, style.sign_pipe, 
									status, style.sign_pipe, log_time, style.sign_pipe, style.sign_space_double, command, style.sing_newline ])




	########################################
	### CHECK PROCESSES FROM CUSTOM LIST ###
	########################################

	def check_processes_from_custom_list(self):
		# GATHER PS COMMAND TO BE USED #
		menu_output = ''.join([ style.sing_newline, text.text_32, style.sing_newline ])
		keys_of_ps_commands = list(config.ps_commands.keys())
		keys_of_ps_commands.sort()
		for counter, command in enumerate(keys_of_ps_commands):
			menu_output += ''.join([ str(counter+1), style.sign_minus_space, command, style.sing_newline  ])
		print(menu_output)
		while True:
			choosen_option = str(input(text.text_33))
			if not choosen_option.isdigit():
				print(''.join([ style.sing_newline, text.text_34, style.sing_newline ]) )
			elif int(choosen_option) < 1 or int(choosen_option) > len(keys_of_ps_commands):
				print( ''.join([ style.sing_newline, text.text_35, style.sing_newline ]) )
			else:
				ps_command = keys_of_ps_commands[int(choosen_option)-1]
				pid_field = config.ps_commands[ps_command]
				break
		# GATHER FILE WITH LIST OF PROCESSES TO CHECK
		custom_processes_files = os_listdir(os_path.join( config.path_to_script, config.folder_custom_processes_list ) )
		menu_output = ''.join([ style.sing_newline, text.text_32, style.sing_newline ])
		for counter, file in enumerate(custom_processes_files):
			menu_output += ''.join([ str(counter+1), style.sign_minus_space, file, style.sing_newline  ])
		print(menu_output)
		while True:
			choosen_option = str(input(text.text_33))
			if not choosen_option.isdigit():
				print(''.join([ style.sing_newline, text.text_34, style.sing_newline ]) )
			elif int(choosen_option) < 1 or int(choosen_option) > len(keys_of_ps_commands):
				print( ''.join([ style.sing_newline, text.text_35, style.sing_newline ]) )
			else:
				file = os_path.join( config.path_to_script, config.folder_custom_processes_list, custom_processes_files[int(choosen_option)-1] )
				break
		# LOAD CHOOSEN LISTS AND CHECK PROCESSES #
		self.load_processes_list(custom_file=file)
		self.list_currently_working_processes(ps_command, pid_field)
		self.check_processes()



	#################################
	### CHECK LOGFILES FOR ERRORS ###
	#################################

	def search_for_errors_in_logfiles(self):
		self.output = style.sing_newline
		for processes_group in self.list_of_processes_to_check:
			if not any(process.do_check_for_errors_in_logfile for process in processes_group.processes_list): continue
			self.header_preparator(processes_group.group_name)
			for process in processes_group.processes_list:
				if process.do_check_for_errors_in_logfile:
					if process.log_path:
						log_path_full_list = list()
						path, file = os_path.split(process.log_path)
						if not os_path.exists( path ):
							self.output += ''.join([ GREEN, process.name, NC, style.sign_minus_space, path, RED, style.sign_minus_space, text.text_12, NC, style.sing_newline ])
							continue
						path_listed_elements = os_listdir( path )
						path_listed_elements.sort( key = lambda x: os_path.getmtime( os_path.join( path, x ) ), reverse=True )
						how_manylog_files_added = 0
						for file_name in path_listed_elements:
							if file in file_name:
								log_path_full_list.append( os_path.join( path, file_name ) )
								how_manylog_files_added += 1
								if how_manylog_files_added == config.how_many_path_to_logs_show_in_show_log_paths_function:
									break
						else:
							self.output += ''.join( [ YELLOW, process.name, NC, style.sign_space, ORANGE, text.text_20, NC, style.sing_newline ] )
							continue
						for log_path_full in log_path_full_list:
							if os_path.exists(log_path_full):
								self.output += ''.join([ YELLOW, process.name, NC, style.sign_minus_space, log_path_full, style.sing_newline ])
								error_found = 0
								for error in config.logs_error_patterns_list:
									with open(log_path_full) as file:
										line_counter = 0
										for line in file:
											line_counter +=1
											line.strip('\r\n')
											if error in line:
												error_found += 1
												self.output += ''.join([CYAN, str(line_counter), style.sign_colon_space, RED, line.rstrip(), NC, style.sing_newline ])
								if error_found == 0: self.output += ''.join([ GREEN, text.text_4, NC, style.sing_newline ])
					else: self.output += ''.join( [ YELLOW, process.name, NC, style.sign_minus_space, BLUE, text.text_5, NC, style.sing_newline ] )
		print( self.output )



	###############################
	### PRINT PATHS TO LOGFILES ###
	###############################

	def print_log_files_paths(self):
		self.output = ''
		for process_group in self.list_of_processes_to_check:
			self.header_preparator( process_group.group_name )
			for process in process_group.processes_list:
				if process.log_path != None:
					path, file = os_path.split(process.log_path)
					if not os_path.exists( path ):
						output_array = (style.process_logfile_header % ( process.name, style.date_status_unknown ) ).split(style.sign_pipe)
						self.output += ''.join([ style.one_line_length*style.sign_equal, style.sing_newline, style.sign_pipe, GREEN, output_array[0], NC,
													style.sign_pipe, CYAN, output_array[1], NC, style.sign_pipe, BLUE, output_array[2], NC, style.sign_pipe, style.sing_newline ])
						self.output += ''.join([ (style.process_logfile_one_line_format % text.text_12), style.sing_newline ])
						continue
					path_listed_elements = os_listdir( path )
					path_listed_elements.sort( key = lambda x: os_path.getmtime( os_path.join( path, x ) ), reverse=True )
					counter = 0
					for file_name in path_listed_elements:
						if file in file_name:
							full_path = os_path.join( path, file_name )
							file_date = datetime.fromtimestamp( os_stat( full_path ).st_mtime ).strftime(style.logfile_datetim_format)
							if counter == 0:
								output_array = (style.process_logfile_header % ( process.name, file_date ) ).split(style.sign_pipe)
								self.output += ''.join([ style.one_line_length*style.sign_equal, style.sing_newline, style.sign_pipe, GREEN, output_array[0], NC,
															style.sign_pipe, CYAN, output_array[1], NC, style.sign_pipe, BLUE, output_array[2], NC, style.sign_pipe, style.sing_newline ])
							self.output += ''.join([ (style.process_logfile_one_line_format % full_path), style.sing_newline ])
							counter += 1
							if counter == config.how_many_path_to_logs_show_in_show_log_paths_function:
								break
					if counter == 0: 
						output_array = (style.process_logfile_header % ( process.name, style.date_status_unknown ) ).split(style.sign_pipe)
						self.output += ''.join([ style.one_line_length*style.sign_equal, style.sing_newline, style.sign_pipe, GREEN, output_array[0], NC,
													style.sign_pipe, CYAN, output_array[1], NC, style.sign_pipe, BLUE, output_array[2], NC, style.sign_pipe, style.sing_newline ])
						self.output += ''.join([ (style.process_logfile_one_line_format % text.text_8), style.sing_newline ])
				else: 
					output_array = (style.process_logfile_header % ( process.name, style.date_status_unknown ) ).split(style.sign_pipe)
					self.output += ''.join([ style.one_line_length*style.sign_equal, style.sing_newline, style.sign_pipe, GREEN, output_array[0],
												NC, style.sign_pipe, CYAN, output_array[1], NC, style.sign_pipe, BLUE, output_array[2], NC, style.sign_pipe, style.sing_newline ])
					self.output += ''.join([ (style.process_logfile_one_line_format % text.text_7), style.sing_newline])
		self.output += ''.join([ style.one_line_length*style.sign_equal, style.sing_newline ])
		print(self.output)



	###################
	### PANIC CLOSE ###
	###################

	def panic_close(self):
		pids_of_working_processes = list()
		for process_group in self.list_of_processes_to_check:
			# CHECK NUMBER OF INSTANCES WORKING #
			for process in process_group.processes_list:
				for running_process in self.list_of_processes_on_current_hostname:
					if process.pattern in running_process:
						if config.use_psutil_library: pid_column = config.ps_commands[config.psutil_library]
						else: pid_column = config.column_with_pid_for_ps_command
						pids_of_working_processes.append( (running_process.split( )[pid_column]) )
		if pids_of_working_processes:
			pids_of_working_processes_set = list(set(pids_of_working_processes))
			print( ''.join([ style.sing_newline, config.command_kill, style.sign_space.join(pids_of_working_processes_set), style.sing_newline ]) )
		else:
			print( ''.join([ style.sing_newline, text.text_14, style.sing_newline ]) )



	###########
	### TOP ###
	###########

	def top(self):
		from time import sleep as time_sleep
		while True:
			os_system( config.command_clear )
			self.list_currently_working_processes(config.ps_command, config.column_with_pid_for_ps_command)
			self.check_processes()
			time_sleep(config.refresh_interwal_in_seconds)



	##################################
	### CREATE START / STOP SCRIPT ###
	##################################

	def create_start_or_stop_script(self, if_start):
		# PREPARE VARIABLES #
		data_for_file = ''.join([ config.header_script_declaration, style.sing_newline ])
		if if_start:
			start_or_stop_message = text.text_21
			script_name = os_path.join( config.path_to_script, config.start_script_name )
			final_message = ''.join([ style.sing_newline, text.text_23, style.sing_newline, script_name, style.sing_newline ])
		elif not if_start:
			start_or_stop_message = text.text_22
			script_name = os_path.join( config.path_to_script, config.stop_script_name )
			final_message = ''.join([ style.sing_newline, text.text_24, style.sing_newline, script_name, style.sing_newline ])
			self.list_of_processes_to_check.reverse()
		# CREATE DATA FOR SCRIPT #
		for process_group in self.list_of_processes_to_check:
			data_for_file += ''.join([ config.command_echo, style.sign_space, style.sign_apostrophe, process_group.group_name, style.sign_minus_space, start_or_stop_message, style.sign_apostrophe, style.sing_newline ])
			if not if_start: process_group.processes_list.reverse()
			for process in process_group.processes_list:
				if process.start_command and if_start:
					data_for_file += ''.join([ process.start_command, style.sing_newline ])
				elif process.end_command and not if_start:
					data_for_file += ''.join([ process.end_command, style.sing_newline ])
				if config.break_between_each_start_stop_command_in_seconds > 0:
					data_for_file += ''.join([ config.command_sleep, style.sign_space, str(config.break_between_each_start_stop_command_in_seconds), style.sing_newline ])
		data_for_file += ''.join([ config.command_echo, style.sign_space, style.sign_apostrophe, text.text_25, style.sign_apostrophe, style.sing_newline ])
		# SAVE DATA TO FILE #
		try:
			with open( script_name, 'w' ) as created_script_file:
				created_script_file.write(data_for_file)
		except:
			sys_exit(''.join([style.sing_newline, text.text_6, style.sing_newline, script_name, style.sing_newline]))
		# SET PERMISSIONS TO SCRIPT #
		if config.owner_of_the_script:
			try:
				os_chown( script_name, getpwnam(config.owner_of_the_script).pw_uid, 0 )
			except:
				sys_exit(''.join([style.sing_newline, text.text_1, style.sing_newline, script_name, style.sing_newline, text.text_3, style.sing_newline]))
		os_chmod( script_name, config.access_rights_to_scipt )
		print(final_message)



	#############################################
	### MONITOR ALL PROCESSES IN BACKGROUNDES ###
	#############################################

	def monitor_processes_in_background(self):
		from time import sleep as time_sleep
		if config.use_python_smtplib:
			import smtplib
			from email.mime.text import MIMEText
			from email.mime.multipart import MIMEMultipart
		if config.use_mailx:
			from os import remove as os_remove
		while True:
			self.list_currently_working_processes(config.ps_command, config.column_with_pid_for_ps_command)
			list_of_broken_processes = list()
			for process_group in self.list_of_processes_to_check:
				# CHECK PROCESSES
				for process in process_group.processes_list:
					number_of_found_instances = 0
					# COUNT NUMBER OF INSTANCES #
					for running_process in self.list_of_processes_on_current_hostname:
						if process.pattern in running_process:
							number_of_found_instances += 1
					if number_of_found_instances == process.number_of_instances:
						# CHECK UPDATE ON LOGFILE #
						if process.log_update > 0 and process.log_path:
							final_path_to_log = ''
							path, file = os_path.split(process.log_path)
							path_listed_elements = os_listdir( path )
							path_listed_elements.sort( key = lambda x: os_path.getmtime( os_path.join( path, x ) ), reverse=True )
							for file_name in path_listed_elements:
								if file in file_name:
									final_path_to_log = os_path.join( path, file_name )
									break
							last_logfile_date = datetime.fromtimestamp( os_stat( final_path_to_log ).st_mtime )
							now_minus_time = datetime.now() - timedelta( seconds=process.log_update )
							if last_logfile_date < now_minus_time:
								last_update_time = datetime.now() - last_logfile_date
								treshold = timedelta(seconds=process.log_update)
								list_of_broken_processes.append( ( process.name, number_of_found_instances, process.number_of_instances, last_update_time, treshold ) )
						else:
							continue
					elif number_of_found_instances != process.number_of_instances:
						list_of_broken_processes.append( ( process.name, number_of_found_instances, process.number_of_instances) )
			# IF FOUND BROKEN PROCESS SEND MAIL #
			if list_of_broken_processes:
				# PREPARE MAIL BODY #
				mail_body = style.mail_header
				for broken_process in list_of_broken_processes:
					if len(broken_process) == 3:
						name, number_of_working_processes, number_of_expected_working_processes = broken_process
						mail_body += ''.join([ ( style.mail_one_line_format  % ( number_of_working_processes, number_of_expected_working_processes, '', '', name ) ) ])
					elif len(broken_process) == 5:
						name, number_of_working_processes, number_of_expected_working_processes, last_update, update_treshold = broken_process
						mail_body += ''.join([ ( style.mail_one_line_format  % ( number_of_working_processes, number_of_expected_working_processes,
												str(last_update)[:7], str(update_treshold), name ) ) ])
				# SENT MAIL #
				# USING PYTHON LIBRARIES #
				if config.use_python_smtplib:
					try:
						receivers_data = ';'.join(config.receivers)
						msg = MIMEMultipart()
						msg['From'] = config.sender
						msg['To'] = receivers_data
						msg['Subject'] = ( config.subject % socket_gethostname() )
						msg.attach(MIMEText(mail_body, 'plain'))
						server = smtplib.SMTP(config.smtp_server, config.smtp_port)
						server.ehlo()
						server.starttls()
						server.ehlo()
						server.login(config.sender, config.sender_password)
						text = msg.as_string()
						server.sendmail(config.sender, config.receivers, text)
					except:
						sys_exit( text.text_11 )
				# USING MAILX #
				if config.use_mailx:
					try:
						file_body_path = os_path.join( config.path_to_script, config.sent_body_file_name )
						with open( file_body_path, 'w') as file:
							file.write(mail_body)
						command = ''.join([ '( cat ', file_body_path, ' ) | mailx -s "', ( config.subject % socket_gethostname() ), '" "', ( ','.join(config.receivers) ), '"' ])
						os_system(command)
						os_remove(file_body_path)
					except KeyError:
						sys_exit( text.text_16 )
				time_sleep(config.when_found_broken_processes_next_check_in_seconds)
			time_sleep(config.check_processes_each_how_many_seconds)





	############
	### INIT ###
	############

	def __init__(self, arguments):
		if arguments.use_color:
			self.color()
		if arguments.no_color:
			self.no_color()
		if arguments.custom_list:
			self.check_processes_from_custom_list()
			arguments.basic = False
		if arguments.print_log_paths:
			self.load_processes_list()
			self.print_log_files_paths()
			arguments.basic = False
		if arguments.check_errors:
			self.load_processes_list()
			self.search_for_errors_in_logfiles()
			arguments.basic = False
		if arguments.top:
			self.load_processes_list()
			self.top()
		if arguments.panic_close:
			self.load_processes_list()
			self.list_currently_working_processes(config.ps_command, config.column_with_pid_for_ps_command)
			self.panic_close()
			arguments.basic = False
		if arguments.create_start_script:
			self.load_processes_list()
			self.create_start_or_stop_script(if_start=True)
			arguments.basic = False
		if arguments.create_stop_script:
			self.load_processes_list()
			self.create_start_or_stop_script(if_start=False)
			arguments.basic = False
		if arguments.background_monitor_with_mail:
			self.load_processes_list()
			self.monitor_processes_in_background()
			arguments.basic = False
		if arguments.basic:
			self.load_processes_list()
			self.list_currently_working_processes(config.ps_command, config.column_with_pid_for_ps_command)
			self.check_processes()


#####################
### LOAD FUNCTION ###
#####################

def load_arguments():
	try:
		parser = argparse.ArgumentParser(prog='PCS Tool', description='Application for checking and monitoring of indicated processes')
		parser.add_argument('-5', '--basic', help=argparse.SUPPRESS, default=True, action='store_true')
		parser.add_argument('-0', '--no_color', help='No color (BASH Color)', default=False, action='store_true')
		parser.add_argument('-1', '--use_color', help='Use color (BASH Color, default option)', default=True, action='store_true')
		parser.add_argument('-a', '--custom_list', help='Check processes from custom file list with processes', default=False, action='store_true')
		parser.add_argument('-b', '--print_log_paths', help='Print paths to logfiles', default=False, action='store_true')
		parser.add_argument('-c', '--check_errors', help='check basic logs for errors phrases of choosen processes', default=False, action='store_true')
		parser.add_argument('-d', '--top', help='works like top, refresh each several seconds ([ctrl+c] to break)', default=False, action='store_true')
		parser.add_argument('-e', '--panic_close', help='panic close - command for kill all processes', default=False, action='store_true')
		parser.add_argument('-f', '--create_start_script', help='create start script', default=False, action='store_true')
		parser.add_argument('-g', '--create_stop_script', help='create stop script', default=False, action='store_true')
		parser.add_argument('-i', '--background_monitor_with_mail', help='work in background as monitor and mail if broken process found', default=False, action='store_true')
		arguments = parser.parse_args()
		self_main = CheckProcesses(arguments)
	except KeyboardInterrupt:
		sys_exit( menu_signs.sign_empty.join([ menu_signs.sign_newline_double, menu_text.error_keyboard_interrupt, menu_signs.sign_newline_double ]) )
	except IndexError as error:
		sys_exit( menu_signs.sign_empty.join([ menu_signs.sign_newline, menu_text.error_index_error, menu_signs.sign_newline_double, str(error), menu_signs.sign_newline_double ]))
	### HASH BELOW 2 LINES IF YOU WANT TO SEE MORE DETAILED INFO ABOUT ERRORS ###
	#except Exception as error:
	#	sys_exit(menu_signs.sign_empty.join([ menu_signs.sign_newline, menu_text.error_other_type_of_error, menu_signs.sign_newline_double, str(error), menu_signs.sign_newline_double ]))




if __name__ == "__main__":
	load_arguments()
