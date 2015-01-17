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
		self.student_count = None #turn this to 0 instead of None
		self.coach_list = []

	def __str__(self):
		return "(version=%s, coach=%s, students=%s, name=%s, student_cnt=%s, coach_list=%s)" % \
				(self.version,self.coach,self.students,self.name,self.student_count,self.coach_list)

def recursive_count(user_id,hierarchy):

	count = 1

	for student_id in hierarchy[user_id].students:
		count += recursive_count(student_id,hierarchy)

	return count

def set_student_counts(hierarchy):

	for user_id in hierarchy.keys():
		count = recursive_count(user_id,hierarchy)
		hierarchy[user_id].student_count = count

	print "Student counts set."
	return 1

def set_coach_lists(hierarchy):

	for user_id in hierarchy.keys():
		user = hierarchy[user_id]
		coach_list = []

		while user.coach != None:
			coach_list.append(user.coach)
			user = hierarchy[user.coach]

		hierarchy[user_id].coach_list = coach_list

	return 1

def recursive_create(coach_id,user_list,hierarchy,std_version):

	for user_id in user_list:
		#print user_list[user_id]
		if user_list[user_id] != None:
			hierarchy[user_id]=User(std_version,coach_id,user_list[user_id].keys(),None)
			recursive_create(user_id,user_list[user_id],hierarchy,std_version)
		else:
			hierarchy[user_id]=User(std_version,coach_id,[],None)
			pass

	return 0

def set_hierarchy(user_list,std_version=1.0):

	""" 
	Given an coach-student list, creates the hierarchy dict
	and its Users, like {user_id:User}.

	All the Users are given the same version field at the beginning.
	"""
	hierarchy = {}

	recursive_create(None,user_list,hierarchy,std_version)
	set_student_counts(hierarchy)
	set_coach_lists(hierarchy)

	dict_print(hierarchy)

	return hierarchy
