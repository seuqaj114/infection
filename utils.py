def get_ordered_user_list(collection,include_singular=False):
	ordered_user_list = [(user_id,collection[user_id].student_count) for user_id in collection.keys() if collection[user_id].student_count != 1]
	ordered_user_list.sort(key=lambda x: -x[1])

	return ordered_user_list

def dict_print(dictionary):
	for key, value in dictionary.items():
		print key, value

	return 1