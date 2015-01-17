from utils import dict_print

class User():
	"""
	User fields:
		-version (float)
		-coach (single id; max_lenght=1; set to None if in topmost layer)
		-students (list of id's; max_lenght=unlimited)
		-name (string)
		-student_count (integer) -> number of students in lower graph + self
	"""

	def __init__(self,version,coach,students,name):
		self.version = version
		self.coach = coach
		self.students = students
		self.name = name
		self.student_count = 1
		self.coach_list = []

	def __str__(self):
		return "(version=%s, coach=%s, students=%s, name=%s, student_cnt=%s, coach_list=%s)" % \
				(self.version,self.coach,self.students,self.name,self.student_count,self.coach_list)

def recursive_count(user_id,collection):

	count = 1

	for student_id in collection[user_id].students:
		count += recursive_count(student_id,collection)

	return count

def set_student_counts(collection):

	for user_id in collection.keys():
		count = recursive_count(user_id,collection)
		collection[user_id].student_count = count

	print "Student counts set."
	return 1

def set_coach_lists(collection):

	for user_id in collection.keys():
		user = collection[user_id]
		coach_list = []

		while user.coach != None:
			coach_list.append(user.coach)
			user = collection[user.coach]

		collection[user_id].coach_list = coach_list

	return 1

def recursive_create(coach_id,user_hierarchy,collection,std_version):

	for user_id in user_hierarchy:
		if user_hierarchy[user_id] != None:
			collection[user_id]=User(std_version,coach_id,user_hierarchy[user_id].keys(),None)
			recursive_create(user_id,user_hierarchy[user_id],collection,std_version)
		else:
			collection[user_id]=User(std_version,coach_id,[],None)

	return 1

def set_collection(hierarchy,std_version=1.0):

	""" 
	Given an coach-student list, creates the collection dict
	and its Users, like {user_id:User}.

	All the Users are given the same version field at the beginning.
	"""
	collection = {}

	recursive_create(None,hierarchy,collection,std_version)
	set_student_counts(collection)
	set_coach_lists(collection)

	dict_print(collection)

	return collection

def add_user(new_user_id,coach_id,collection):
	collection[new_user_id] = User(collection[coach_id].version,coach_id,[],None)
	collection[coach_id].students.append(new_user_id)

	user = collection[new_user_id]
	coach_list = []

	while user.coach != None:
		coach_list.append(user.coach)
		user = collection[user.coach]
		user.student_count += 1

	collection[new_user_id].coach_list = coach_list
