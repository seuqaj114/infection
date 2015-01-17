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

def recursive_create(coach_id,user_list,hierarchy,std_version):

	for user_id in user_list:
		#print user_list[user_id]
		if user_list[user_id] != None:
			hierarchy[user_id]=User(std_version,coach_id,user_list[user_id].keys(),None)
			recursive_create(user_id,user_list[user_id],hierarchy,std_version)
		else:
			hierarchy[user_id]=User(standard_version,coach_id,[],None)
			pass

	return 0

def spread_infection(user_id,version,hierarchy):

	#	Test if this user's version is already updated.
	if hierarchy[user_id].version != version:
		hierarchy[user_id].version = version
	else:
		return 1

	#	Put the 2 below together?
	if hierarchy[user_id].students != None:
		for student_id in hierarchy[user_id].students:
			spread_infection(student_id,version,hierarchy)
	else:
		pass

	if hierarchy[user_id].coach != None:
		spread_infection(hierarchy[user_id].coach,version,hierarchy)
	else:
		pass

	return 0

def infect_below(user_id,version,hierarchy):
	#	No need to check for version, since infection is done one-way

	hierarchy[user_id].version = version

	if hierarchy[user_id].students != None:
		for student_id in hierarchy[user_id].students:
			infect_below(student_id,version,hierarchy)
	else:
		pass

	return 0


def spread_limited_infection(infect_count,version,hierarchy):

	cnt_list=[(user_id,hierarchy[user_id].student_count) for user_id in hierarchy.keys()]
	print cnt_list
	cnt_list.sort(key=lambda x: abs(x[1]-infect_count))

	#	Set priority in case of a tie???

	#	Propagation only happens to lower levels.
	infect_below(cnt_list[0][0],version,hierarchy)

	for key, value in hierarchy.items():
		print key, value

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

	for key, value in hierarchy.items():
		print key, value

	return hierarchy


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

def get_ordered_user_list(hierarchy,include_singular=False):
	ordered_user_list = [(user_id,hierarchy[user_id].student_count) for user_id in hierarchy.keys() if hierarchy[user_id].student_count != 1]
	ordered_user_list.sort(key=lambda x: -x[1])

	return ordered_user_list

def get_approx_set(ord_user_list,total,hierarchy):

	approx_set = [ord_user_list[0][0]]
	approx_set_sum = ord_user_list[0][1]

	for i in range(1,len(ord_user_list)):
		if ord_user_list[i-1][0] in hierarchy[ord_user_list[i][0]].coach_list:
			continue

		if approx_set_sum + ord_user_list[i][1] >= total:
			break
		else:
			approx_set_sum += ord_user_list[i][1]
			approx_set.append(ord_user_list[i][0])

	print "approx_set = %s" % approx_set
	return approx_set


#	Usar esta apenas de seguida para fazer o limited infection.
#	Fazer recursive para o exact infection e parar quando i*n < o que falta. passar para as recursivas sempre o que falta. usar global para guardar

def search_exact_set(sub_user_list,sub_total,best_set,hierarchy):
	#print "best_set = %s" % best_set
	for i in range(len(sub_user_list)):
		previous_coach = [previous_user in hierarchy[sub_user_list[i][0]].coach_list for previous_user in best_set]
		if any(previous_coach):
			continue
		elif sub_user_list[i][1] > sub_total:
			continue
		elif sub_user_list[i][1] == sub_total:
			best_set.append(sub_user_list[i][0])
			return best_set
		else:
			best_set.append(sub_user_list[i][0])
			a = search_exact_set(sub_user_list[i+1:],sub_total-sub_user_list[i][1],best_set,hierarchy)
			if a == False:
				best_set.pop()
				continue
			else:
				return best_set

	best_set = []
	return False


def get_exact_set(ord_user_list,total,hierarchy):

	exact_set = search_exact_set(ord_user_list,total,[],hierarchy)
	print "exact_set = %s" % exact_set

	return exact_set