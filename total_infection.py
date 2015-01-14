from uuid import uuid4, UUID

hierarchy={}
standard_version=1.0

class User():
	"""
	User fields:
		-version (float)
		-coach (single id; max_lenght=1; set to None if in topmost layer)
		-students (list of id's; max_lenght=unlimited)
		-name (string)
	"""

	def __init__(self,version,coach,students,name):
		self.version = version
		self.coach = coach
		self.students = students
		self.name = name

	def __str__(self):
		return "(version=%s, coach=%s, students=%s, name=%s)" % (self.version,self.coach,self.students,self.name)

def recursive_add(coach_id,user_list):
	global hierarchy
	global standard_version

	#print coach_id, user_list
	if user_list == None:
		return 0
	else:
		for user_id in user_list:
			print user_list[user_id]
			try:
				hierarchy[user_id]=User(standard_version,coach_id,user_list[user_id].keys(),None)
			except AttributeError:
				hierarchy[user_id]=User(standard_version,coach_id,None,None)
			
			recursive_add(user_id,user_list[user_id])

			"""
			if user_list[user_id] != None:
				hierarchy[user_id]=User(standard_version,coach_id,user_list[user_id].keys(),None)
				recursive_add(user_id,user_list[user_id])
			else:
				hierarchy[user_id]=User(standard_version,coach_id,None,None)
				return 1
			"""
	return 0

def spread_infection(user_id,version):
	global hierarchy

	if user_id == None:
		return 0

	#	Test if this user's version is already updated.
	if hierarchy[user_id].version != version:
		hierarchy[user_id].version = version
	else:
		return 1

	#	Put the 2 below together?

	if hierarchy[user_id].students != None:
		for student_id in hierarchy[user_id].students:
			spread_infection(student_id,version)
	else:
		pass

	if hierarchy[user_id].coach != None:
		spread_infection(hierarchy[user_id].coach,version)
	else:
		pass

	return 0


def set_hierarchy(user_list):

	""" 
	Given an coach-student list, creates the hierarchy dict
	and its Users, like {user_id:User}.

	All the Users are given the same version field at the beginning.
	"""
	global hierarchy

	recursive_add(None,user_list)

	for key, value in hierarchy.items():
		print key, value

