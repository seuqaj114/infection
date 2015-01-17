from utils import get_ordered_user_list, dict_print

def infect_below(user_id,version,collection):

	"""
		Recursively infects all users below 'user_id' with 'version'.
		Similar to 'infect_around' from total_infection, but does not spread to coaches.

		Stops when there are no students left.
	"""
	
	#	No need to check for version, since infection is done one-way 
	#	(each user is visited exactly once)
	collection[user_id].version = version

	if collection[user_id].students != None:
		for student_id in collection[user_id].students:
			infect_below(student_id,version,collection)
	else:
		pass

	return 1

def spread_limited_infection(infect_count,version,collection,exact=False):

	"""
		Spreads a limited infection according to the number of users to infect, 'infect_count'.

		'exact' defines wether EXACTLY 'infect_count' users must be infected or not.

		Returns a list of infected users.
	"""

	#	Gets list of (user_id,student_count) tuples in decreasing order.
	ord_user_list = get_ordered_user_list(collection)

	if exact == False:
		#	If not exact, get a user set that ROUGHLY approximates to the desired 'infect_count'.
		infection_set = get_approx_set(ord_user_list,infect_count,collection)
	else:
		#	If exact, get a user set that infects EXACTLY 'infect_count' users.
		infection_set = get_exact_set(ord_user_list,infect_count,collection)
		if infection_set == False:
			print "Exact infection impossible!"
			return 0

	#	Infect all levels below each user in 'infection_set'.
	for user_id in infection_set:
		infect_below(user_id,version,collection)

	#	Print updated 'collection'.
	dict_print(collection)

	return infection_set

def get_approx_set(ord_user_list,total,collection):

	"""
		Returns a set of users that, when applied 'infect_below', infects approximately 'total' users.
		
		The approximation is always done from below, i.e., the infection will never happen
		to more than 'total' users, to avoid singularities, e.g.:
			-> if 'total' is 10, and the first 2 users are 9, not imposing the approximation
				to happen from below would cause the program to infect 18 users, instead of 9.

		Algorithm is very rough, and does not take into account all possible combinations,
		just cares about getting a good enough combiation. That's why no recursion was implemented.
	"""

	#	Set of users below which the infection will spread.
	approx_set = []
	#	Number of users to be infected
	approx_set_sum = 0

	for i in range(len(ord_user_list)):

		#	Prevent current user from being selected if the selection of a previous user would cause
		#	this one to be infected aswell (= previous users must not be in current user's coach_list).
		previous_coach = [previous_user in collection[ord_user_list[i][0]].coach_list for previous_user in approx_set]
		if any(previous_coach):
			continue

		#	If the number of users to be infected is greater than 'total', continue search.
		elif approx_set_sum + ord_user_list[i][1] > total:
			continue
		#	If not, add current user to the infection set and update the number of users to be infected.
		else:
			approx_set_sum += ord_user_list[i][1]
			approx_set.append(ord_user_list[i][0])

	print "approx_set = %s" % approx_set
	return approx_set

#	Fazer recursiva para o exact e parar quando i*n < o que falta. passar para as recursivas sempre o que falta. usar global para guardar
def search_exact_set(sub_user_list,sub_total,best_set,collection):

	"""
		Recursively searches for a set of users that, when applied 'infect_below', infects exactly 'total' users.

		The algorithm appends the current user being visited to the 'best_set' stack, and pops it if
		no subsequent search is unsuccessful in finding an exact combination that matches 'sub_total'.
		
		'sub_user_list' is the partition of the list being search by the current recursion level.
		'sub_total' is the infection count to be found in the current recursion level.
	"""

	for i in range(len(sub_user_list)):

		#	Prevent current user from being selected if the selection of a previous user would cause
		#	this one to be infected aswell (= previous users must not be in current user's coach_list).
		previous_coach = [previous_user in collection[sub_user_list[i][0]].coach_list for previous_user in best_set]
		if any(previous_coach):
			continue

		#	If the number of users to be infected is greater that total, move to next student
		#	(hence, lower student count, since 'sub_user_list' is always decreasing).
		elif sub_user_list[i][1] > sub_total:
			continue

		#	If the number of users to be infected is exactly what was being looked for, the counting 
		#	stops and the last user is appended to 'best_set'
		elif sub_user_list[i][1] == sub_total:
			best_set.append(sub_user_list[i][0])
			return True

		#	If the number of users to be infected is still lower than 'sub_total', append current user to
		#	'best_set' (might be poped later) and repeat the search in the sub_user_list after current user,
		# 	for a 'sub_total' of current sub_total minus the number of users to be infected by the current user.
		else:
			best_set.append(sub_user_list[i][0])
			combination_found = search_exact_set(sub_user_list[i+1:],sub_total-sub_user_list[i][1],best_set,collection)

			#	If the lower level search returns false, pop the current user and continue the search with the next user.
			if combination_found == False:
				best_set.pop()
				continue

			#	If the search is successful, keep 'best_set' as is (since it is already complete) and return it.
			else:
				return best_set

	#	If the end of 'sub_user_list' is reached, no exact combination was found in the current recursion level, 
	#	so it returns False in order to pop the previous user.
	best_set = []
	return False


def get_exact_set(ord_user_list,total,collection):

	"""
		Returns a set of users that, when applied 'infect_below', infects exactly 'total' users.
	"""

	exact_set = search_exact_set(ord_user_list,total,[],collection)
	print "exact_set = %s" % exact_set

	return exact_set