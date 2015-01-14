from uuid import uuid4, UUID

hierarchy={}
standard_version=1.0
count=0

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
		self.student_count = None

	def __str__(self):
		return "(version=%s, coach=%s, students=%s, name=%s, student_cnt=%s)" % \
				(self.version,self.coach,self.students,self.name,self.student_count)

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

def infect_below(user_id,version):
	#	No need to check for version, since infection is done one-way

	global hierarchy

	hierarchy[user_id].version = version

	if hierarchy[user_id].students != None:
		for student_id in hierarchy[user_id].students:
			infect_below(student_id,version)
	else:
		pass

	return 0


def spread_limited_infection(infect_count,version):
	global hierarchy

	cnt_list=[(user_id,hierarchy[user_id].student_count) for user_id in hierarchy.keys()]
	print cnt_list
	cnt_list.sort(key=lambda x: abs(x[1]-infect_count))

	#	Set priority in case of a tie???

	#	Propagation only happens to lower levels.
	infect_below(cnt_list[0][0],version)

	for key, value in hierarchy.items():
		print key, value

	return 0


def set_hierarchy(user_list):

	""" 
	Given an coach-student list, creates the hierarchy dict
	and its Users, like {user_id:User}.

	All the Users are given the same version field at the beginning.
	"""
	global hierarchy

	recursive_add(None,user_list)
	set_student_counts()

	for key, value in hierarchy.items():
		print key, value


def recursive_count(user_id):
	global count
	global hierarchy

	count+=1

	if hierarchy[user_id].students != None:
		for student_id in hierarchy[user_id].students:
			recursive_count(student_id)
	else:
		pass

	return 0

def set_student_counts():
	global hierarchy
	global count

	for user_id in hierarchy.keys():
		count = 0
		recursive_count(user_id)
		hierarchy[user_id].student_count = count

	print "Student counts set."



