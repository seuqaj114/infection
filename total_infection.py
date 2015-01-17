from utils import dict_print

def spread_infection(user_id,version,collection):

	#	Test if this user's version is already updated.
	if collection[user_id].version != version:
		collection[user_id].version = version
	else:
		return 1

	#	Put the 2 below together?
	if collection[user_id].students != None:
		for student_id in collection[user_id].students:
			spread_infection(student_id,version,collection)
	else:
		pass

	if collection[user_id].coach != None:
		spread_infection(collection[user_id].coach,version,collection)
	else:
		pass

	return 1






