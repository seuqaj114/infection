from utils import dict_print

class User():
	"""
	User fields:
		-version (float)
		-coach (single id; max_lenght=1; set to None if in topmost layer)
		-students (list of id's)
		-name (string)
		-student_count (integer) -> number of students below self in relationship tree + itself
		-coach_list (list of id's) -> list of users above self	in the relationship tree
	"""

	def __init__(self,version,coach,students,name):
		self.version = version
		self.coach = coach
		self.students = students
		self.name = name

		#	'student_count' defaults to 1
		self.student_count = 1
		#	'coach_list' defaults to []
		self.coach_list = []

	def __str__(self):
		return "(version=%s, coach=%s, students=%s, name=%s, student_cnt=%s, coach_list=%s)" % \
				(self.version,self.coach,self.students,self.name,self.student_count,self.coach_list)

def recursive_count(user_id,collection):

	"""
		Recursively counts the number of students below a user 'user_id'.
		Each recursive call returns the count at lower levels, and adds it to the current layer's count.
		Stops when reaches users with no students.
	"""

	count = 1

	for student_id in collection[user_id].students:
		count += recursive_count(student_id,collection)

	return count

def set_student_counts(collection):

	"""
		Counts and sets the number of students below each user in the relationship tree (in every layer,
			not only its 'User.students'.
	"""

	for user_id in collection.keys():
		count = recursive_count(user_id,collection)
		collection[user_id].student_count = count

	return 1

def set_coach_lists(collection):

	"""
		Given 'collection', sets users' coach lists, i.e., all the users standing above that user
		in the relationship tree.
		Goes up the relationship tree until it hits a user with no coach, hence, at the top.
	"""

	for user_id in collection.keys():
		user = collection[user_id]
		coach_list = []

		#	Test if user is at the top of its tree.
		while user.coach != None:
			coach_list.append(user.coach)
			user = collection[user.coach]

		collection[user_id].coach_list = coach_list

	return 1

def recursive_create(coach_id,user_hierarchy,collection,std_version):

	"""
		Recursively gets users from 'user_hierarchy' and creates 'collection's
		user_id:User pairs.
	"""

	for user_id in user_hierarchy:
		#	If 'user_id' coaches students,
		if user_hierarchy[user_id] != None:
			collection[user_id]=User(std_version,coach_id,user_hierarchy[user_id].keys(),None)
			recursive_create(user_id,user_hierarchy[user_id],collection,std_version)
		else:
			collection[user_id]=User(std_version,coach_id,[],None)

	return 1

def set_collection(user_hierarchy,std_version=1.0):

	""" 
	Given an relationship tree dictionary, 'user_hierarchy', creates the 'collection' dict
	of entries of the form {user_id:User}. 

	'user_hierarchy's keys must be unique across the whole user space.

	If unspecified, all the Users are given 'std_version' at the beginning.
	"""

	collection = {}

	#	Completely sets up 'collection' from 'user_hierarchy'.
	recursive_create(None,user_hierarchy,collection,std_version)
	set_student_counts(collection)
	set_coach_lists(collection)

	return collection

def add_user(new_user_id,coach_id,collection):

	"""
		Adds a new user 'new_user_id' to the 'collection' dictionary.
	"""

	#	Creates the new user's object, and adds 'new_user_id' to its coache's 'students' list.
	collection[new_user_id] = User(collection[coach_id].version,coach_id,[],None)
	collection[coach_id].students.append(new_user_id)

	#	Sets new user's coach list
	user = collection[new_user_id]
	coach_list = []

	while user.coach != None:
		coach_list.append(user.coach)
		user = collection[user.coach]
		user.student_count += 1

	collection[new_user_id].coach_list = coach_list

	return 1
