from utils import dict_print

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

	return 1






