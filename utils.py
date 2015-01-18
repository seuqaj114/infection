import json

def get_ordered_user_list(collection,include_singular=False):

	"""
		Returns a list of tuples (user_id,User.student_count) from every user
		from 'collection', ordered in decreasing order by 'student_count'.

		If 'include_singular' is False (default) does not include users with no students.
	"""

	ordered_user_list = [(user_id,collection[user_id].student_count) for user_id in collection.keys() if collection[user_id].student_count != 1]
	ordered_user_list.sort(key=lambda x: -x[1])

	return ordered_user_list

def dict_print(dictionary):

	"""
		Because it is boring to print the following every time I want to print a dict.
	"""

	for key, value in dictionary.items():
		print key, value

	return 1

def load_default_data():

	"""
		Loads the default json file "hierarchy.json" into a Python dictionary.
	"""

	return json.load(open("hierarchy.json"))


def sub_dict(coach_id,collection):
	if collection[coach_id].students == []:
		return None
	else:
		return { student_id+" v"+str(collection[student_id].version): sub_dict(student_id,collection) for student_id in collection[coach_id].students }

def visualize_collection(collection):

	"""
		Creates a pretty terminal visualization of the user relationships and their versions."
	"""

	dictionary = { user_id+" v"+str(user.version):sub_dict(user_id,collection) for user_id, user in collection.items() if user.coach == None}

	print json.dumps(dictionary, indent=4)