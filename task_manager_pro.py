import sys
from datetime import date
from tabulate import tabulate
import os


class Task:
	"""
	Class that creates task objects to store task information.
	Instance variable default value set to False for indicating incomplete.
	"""

	def __init__(self, user, heading, description, start_date, due_date, status=False):
		self.user = user
		self.heading = heading
		self.description = description
		self.start_date = start_date
		self.due_date = due_date
		self.status = status

	def finalize(self):
		"""
		Sets status to True indicating task is finalized.
		"""
		self.status = True

	def reassign(self):
		"""
		Method to reassign object user attribute.
		:return: None
		"""
		new_user = valid_user()
		self.user = new_user

	def move_due_date(self):
		"""
		Method to change the object due date attribute.
		"""
		new_due_date = valid_date("New due date (FORMAT: YYYY-MM-DD)")
		self.due_date = new_due_date

	def __str__(self):
		"""
		Method to create string version of object in a list.
		:return: object as string in list.
		"""
		status = "Yes" if self.status else "No"
		to_string = [
				str(self.user),
				str(self.heading),
				str(self.description),
				str(self.start_date),
				str(self.due_date),
				str(status)
		]
		return to_string


def import_users():
	"""
	Function to import user credentials from user.txt
	as a dictionary.
	:return: dictionary key: username value: password
	"""
	user_dict = {}
	with open("documents/user.txt", "r") as user_file:
		user_data = user_file.readlines()
	for user in user_data:
		username, password = user.strip().split(";")
		user_dict[username] = password
	return user_dict


def import_tasks():
	"""
	Function to import data from tasks.txt and unpack into objects
	from the Task class.
	:return: list of task objects
	"""
	tasks_list = []
	with open("documents/tasks.txt", "r") as tasks_file:
		tasks_data = tasks_file.readlines()
	for task in tasks_data:
		user, heading, description, start_date, due_date, status = task.strip().split(";")
		complete = True if status == "Complete" else False
		task_obj = Task(
				user,
				heading,
				description,
				start_date,
				due_date,
				complete
		)
		tasks_list.append(task_obj)
	return tasks_list


def login():
	"""
	Function to verify login credentials.
	:return: Boolean indicating login success or failure.
	"""
	user_dict = import_users()
	print("*** LOGIN ***")
	username = input("Username >_")
	password = input("Password >_")
	if username in user_dict.keys() and password in user_dict.values():
		print("*** LOGIN SUCCESSFUL ***")
		return username, True
	else:
		print("*** USERNAME OR PASSWORD INCORRECT ***")
		return username, False


def valid_int(prompt: str):
	"""
	Function to validate if an input can be cast to integer
	type.
	:param prompt: User is able to customize the input prompt.
	:return: Input cast as integer type.
	"""
	while True:
		try:
			user_input = int(input(prompt))
			return user_input
		except ValueError:
			print("*** ENTER VALID NUMERIC NUMBER ***")


def valid_date(check_date: str):
	"""
	Function to validate if an input is a valid date format.
	:param check_date: String date to be cast to date type.
	:return: Input cast as date type.
	"""
	while True:
		try:
			year, month, day = check_date.split("-")
			date_date = date(int(year), int(month), int(day))
			return date_date
		except ValueError:
			print("*** DATE FORMAT NOT CORRECT ***")


def register_user():
	"""
	Function to create new user credentials.
	Information is written to user.txt file.
	"""
	user_dict = import_users()
	while True:
		new_user = input("Enter new username >_")
		if new_user not in user_dict.keys():
			break
		print("*** USERNAME TAKEN ***")
	while True:
		new_password = input("Enter new password >_")
		verify_password = input("Re-enter password >_")
		if new_password == verify_password:
			break
		print("*** PASSWORD INCORRECT ***")
	with open("documents/user.txt", "a") as user_file:
		user_file.write(f"\n{new_user};{new_password}")
		print("*** NEW USER CREATED ***")


def valid_user():
	"""
	Function to validate if given user is registered.
	"""
	user_dict = import_users()
	while True:
		user = input("Username >_")
		if user in user_dict.keys():
			return user
		print("*** USERNAME DOES NOT EXIST ***")


def add_task(tasks: list, today: date):
	"""
	Function to create new task entry.
	:param tasks: list of task objects.
	:param today: Today's date.
	"""
	user = valid_user()
	heading = input("Task heading >_")
	description = input("Task description >_")
	due_date = valid_date(input("Due date (FORMAT: YYYY-MM-DD) >_"))
	task_obj = Task(
			user,
			heading,
			description,
			today,
			due_date
	)
	tasks.append(task_obj)
	print("*** TASK CREATED ***")


def write_tasks(tasks: list):
	"""
	Function to write task list objects to tasks.txt file in
	correct format.
	:param tasks: list of task objects.
	"""
	write_string = ""
	for task in tasks:
		complete = "Complete" if task.status else "Ongoing"
		write_string += f"{task.user};"
		write_string += f"{task.heading};"
		write_string += f"{task.description};"
		write_string += f"{task.start_date};"
		write_string += f"{task.due_date};"
		write_string += f"{complete}\n"
	with open("documents/tasks.txt", "w") as task_file:
		task_file.write(write_string.rstrip())


def view_all(tasks: list):
	"""
	Function to view all task information from tasks list
	in a readable format.
	:param tasks: list of task objects
	"""
	headers = ["NO", "USER", "HEADING", "DESCRIPTION", "START DATE", "DUE DATE", "STATUS"]
	tabled_list = []
	for count, task in enumerate(tasks, 1):
		complete = "Complete" if task.status else "Ongoing"
		temp_list = [
				count,
				task.user,
				task.heading,
				task.description,
				task.start_date,
				task.due_date,
				complete
		]
		tabled_list.append(temp_list)
		del temp_list
	print(tabulate(tabled_list, headers=headers, tablefmt="fancy_grid"))


def view_mine(tasks: list, current_user: str):
	"""
	Function to only view the tasks assigned to the user
	currently logged in.
	:param tasks: list of task objects.
	:param current_user: logged-in username.
	:return: filtered object list of only the users tasks.
	"""
	filtered_list = []
	for task in tasks:
		if task.user == current_user:
			filtered_list.append(task)
	view_all(filtered_list)
	return filtered_list


def edit_task_select(filtered_list: list):
	"""
	Function to verify valid task choice from filtered task list.
	:param filtered_list: list of task assigned to user
	"""
	while True:
		task_choice = input("Enter \"b\" to return to main menu or the task no to edit >_")
		if task_choice == "b":
			return
		else:
			try:
				chosen_task = filtered_list[int(task_choice)]
				break
			except ValueError and IndexError:
				print("*** INCORRECT CHOICE ***")
				view_all(filtered_list)
	edit_menu = "*** EDIT MENU ***"
	edit_menu += "\n1) Finalize the task (YOU WILL NO LONGER BE ABLE TO EDIT)"
	edit_menu += "\n2) Change the assigned user"
	edit_menu += "\n3) Change the due date"
	edit_choice = input(f"{edit_menu}\n>_")
	if edit_choice == "1":
		chosen_task.finalize()
	elif edit_choice == "2":
		chosen_task.reassign()
	elif edit_choice == "3":
		chosen_task.move_due_date()


def get_percentage(smaller_value: int, larger_value: int):
	"""
	Function to calculate percentage values.
	:param smaller_value: smaller of the two integers.
	:param larger_value: larger of the two integers.
	:return: result as integer type.
	"""
	if larger_value > 0:
		result = (smaller_value / larger_value) * 100
	else:
		result = 0
	return int(result)


def task_overview(tasks: list, today: date):
	"""
	Function to calculate certain statistics from the tasks.txt file.
	Statistics are written to user_overview.txt.
	- No of tasks
	- No of completed tasks
	- No of ongoing tasks
	- No of overdue tasks
	- Percentage ongoing tasks
	- Percentage overdue tasks
	:param tasks: list of task objects.
	:param today: today's date.
	"""
	write_string = "*** TASKS OVERVIEW ***\n"
	write_string += "=" * 50
	total_tasks = len(tasks)
	write_string += f"\nTOTAL_TASKS: {total_tasks}"
	completed_tasks = 0
	ongoing_tasks = 0
	overdue_tasks = 0
	for task in tasks:
		due_date = valid_date(task.due_date)
		if task.status:
			completed_tasks += 1
		else:
			ongoing_tasks += 1
			if due_date < today:
				overdue_tasks += 1
	percentage_ongoing = get_percentage(ongoing_tasks, total_tasks)
	percentage_overdue = get_percentage(overdue_tasks, total_tasks)
	write_string += f"\nCOMPLETED_TASKS: {completed_tasks}"
	write_string += f"\nONGOING_TASKS: {ongoing_tasks}"
	write_string += f"\nOVERDUE_TASKS: {overdue_tasks}"
	write_string += f"\nPERCENTAGE_ONGOING_TASKS: {int(percentage_ongoing)}%"
	write_string += f"\nPERCENTAGE_OVERDUE_TASKS: {int(percentage_overdue)}%"
	with open("documents/tasks_overview.txt", "w") as report_file:
		report_file.write(write_string)


def user_overview(tasks: list, today: date):
	"""
	Function to calculate user specific statistics based on information
	in tasks.txt and user.txt and writing information to user_overview.txt.
	- No of users
	- No of tasks
	- No of tasks per user
	- Percentage of tasks assigned per user
	- Percentage of tasks complete per user
	- Percentage of tasks ongoing per user
	- Percentage of tasks overdue per user
	:param tasks: list of task objects.
	:param today: today's date.
	"""
	users = import_users()
	total_users = len(users)
	total_tasks = len(tasks)
	write_string = "*** USER OVERVIEW ***\n"
	write_string += "=" * 50
	for user in users:
		task_per_user = 0
		complete_per_user = 0
		ongoing_per_user = 0
		overdue_per_user = 0
		write_string += "\n" + ("=" * 50)
		write_string += f"\nSTATISTICS_FOR {user.upper()}\n"
		write_string += "=" * 50
		for task in tasks:
			if user == task.user:
				due_date = valid_date(task.due_date)
				task_per_user += 1
				if task.status:
					complete_per_user += 1
				else:
					ongoing_per_user += 1
					if due_date < today:
						overdue_per_user += 1
		percentage_assigned = (task_per_user / total_tasks) * 100 if total_tasks > 0 else 0
		percentage_complete = (complete_per_user / task_per_user) * 100 if task_per_user > 0 else 0
		percentage_ongoing = (ongoing_per_user / task_per_user) * 100 if task_per_user > 0 else 0
		percentage_overdue = (overdue_per_user / task_per_user) * 100 if task_per_user > 0 else 0
		write_string += f"\nTOTAL_TASKS_ASSIGNED: {task_per_user}"
		write_string += f"\nPERCENTAGE_OF_TASKS_ASSIGNED: {int(percentage_assigned)}%"
		write_string += f"\nPERCENTAGE_OF_TASKS_COMPLETE: {int(percentage_complete)}%"
		write_string += f"\nPERCENTAGE_OF_TASKS_ONGOING: {int(percentage_ongoing)}%"
		write_string += f"\nPERCENTAGE_OF_TASKS_OVERDUE: {int(percentage_overdue)}%\n"
		with open("documents/user_overview.txt", "w") as report_file:
			report_file.write(write_string.rstrip())


def display_statistics(tasks, today):
	"""
	Function that checks if reports files exits, if not files
	are first created and then displayed to the user.
	:param tasks: list of task objects.
	:param today: today's date.
	"""
	path_tasks_report = "documents/tasks_overview.txt"
	path_user_report = "documents/user_overview.txt"
	if not os.path.exists(path_tasks_report):
		task_overview(tasks, today)
	if not os.path.exists(path_user_report):
		user_overview(tasks, today)
	with open(path_tasks_report, "r") as task_reports:
		task_report_data = task_reports.readlines()
	with open(path_user_report, "r") as user_reports:
		user_report_data = user_reports.readlines()
	task_report_headers = [
			"NO OF TASKS",
			"COMPLETED TASKS",
			"ONGOING TASKS",
			"OVERDUE TASKS",
			"% ONGOING",
			"% OVERDUE"
	]
	user_report_headers = [
			"USER",
			"NO OF TASKS",
			"% OF TASKS",
			"% COMPLETE",
			"% ONGOING",
			"% OVERDUE"
	]
	temp_list = []
	for report in task_report_data:
		report_split = report.strip().split()
		if len(report_split) == 2:
			temp_list.append(report_split[1])
	task_table_list = [temp_list]
	temp_list = []
	for report in user_report_data:
		report_split = report.strip().split()
		if len(report_split) == 2:
			temp_list.append(report_split)
	print(tabulate(task_table_list, headers=task_report_headers, tablefmt="fancy_grid"))


def main():
	"""
	Main menu function that allows conditional options to direct user to
	various helper functions.
	Main function runs the login function to validate credentials while
	incorporating a time-out timer.
	"""
	tasks_list = import_tasks()
	current_date = date.today()
	time_out = 5
	while True:
		current_user, valid_login = login()
		if valid_login:
			break
		time_out -= 1
		if time_out == 0:
			sys.exit()
		print(f"{time_out} attempts remaining...")
	print("*** WELCOME TO TASK MANAGER PRO ***")
	main_menu = "*** MAIN MENU ***"
	main_menu += "\n1) Register new user"
	main_menu += "\n2) Add new task"
	main_menu += "\n3) View all tasks"
	main_menu += "\n4) View and edit my tasks"
	main_menu += "\n5) Generate reports"
	main_menu += "\n6) Display current reports"
	main_menu += "\n7) Exit"
	while True:
		choice = input(f"{main_menu}\n>_")
		if choice == "1":
			register_user()
		elif choice == "2":
			add_task(tasks_list, current_date)
			write_tasks(tasks_list)
		elif choice == "3":
			view_all(tasks_list)
		elif choice == "4":
			user_tasks = view_mine(tasks_list, current_user)
			edit_task_select(user_tasks)
			write_tasks(tasks_list)
		elif choice == "5":
			task_overview(tasks_list, current_date)
			user_overview(tasks_list, current_date)
		elif choice == "6":
			display_statistics(tasks_list, current_date)
		elif choice == "7":
			sys.exit()
		else:
			print("*** INVALID SELECTION ***")


if __name__ == "__main__":
	main()
