def get_ordered_user_list(hierarchy,include_singular=False):
	ordered_user_list = [(user_id,hierarchy[user_id].student_count) for user_id in hierarchy.keys() if hierarchy[user_id].student_count != 1]
	ordered_user_list.sort(key=lambda x: -x[1])

	return ordered_user_list

def dict_print(dictionary):
	for key, value in dictionary.items():
		print key, value

	return 1