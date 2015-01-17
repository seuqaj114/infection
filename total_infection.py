from utils import dict_print

def infect_around(user_id,version,collection,infected_set):

	"""
		Recursively infects all the students and coach of 'user_id' with 'version'.

		Adds infected users to 'infected_set'.

		Stops when all users in a network have been infected.
	"""

	#	Test if this user's version is already updated. Acts as a 'visited' list.
	if collection[user_id].version != version:
		collection[user_id].version = version
		infected_set.append(user_id)
	else:
		return 1

	#	Put the 2 below together?

	#	Infect user's students, if exists.
	if collection[user_id].students != None:
		for student_id in collection[user_id].students:
			spread_infection(student_id,version,collection)
	else:
		pass

	#	Infect user's coach, if exists.
	if collection[user_id].coach != None:
		spread_infection(collection[user_id].coach,version,collection)
	else:
		pass

	return 1

def spread_infection(user_id,version,collection):

	"""
		Spreads total infection, i.e., from 'user_id', spreads infection of 'version'
		to all connected users (coaches and students) in its network.

		Returns 'infected_set', the list of users that got infected.
	"""

	infected_set = []

	infect_around(user_id,version,collection,infected_set)

	return infected_set







