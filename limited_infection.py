from utils import get_ordered_user_list, dict_print

def infect_below(user_id,version,hierarchy):
	#	No need to check for version, since infection is done one-way

	hierarchy[user_id].version = version

	if hierarchy[user_id].students != None:
		for student_id in hierarchy[user_id].students:
			infect_below(student_id,version,hierarchy)
	else:
		pass

	return 1

def spread_limited_infection(infect_count,version,hierarchy,exact=False):

	ord_user_list = get_ordered_user_list(hierarchy)

	if exact == False:
		infection_set = get_approx_set(ord_user_list,infect_count,hierarchy)
	else:
		infection_set = get_exact_set(ord_user_list,infect_count,hierarchy)
		if infection_set == False:
			print "Exact infection impossible!"
			return 0

	#	Propagation only happens to lower levels.
	for user_id in infection_set:
		infect_below(user_id,version,hierarchy)

	dict_print(hierarchy)

	return 1

def get_approx_set(ord_user_list,total,hierarchy):

	approx_set = []
	approx_set_sum = 0

	for i in range(len(ord_user_list)):
		previous_coach = [previous_user in hierarchy[ord_user_list[i][0]].coach_list for previous_user in approx_set]
		if any(previous_coach):
			continue

		if approx_set_sum + ord_user_list[i][1] >= total:
			continue
		else:
			approx_set_sum += ord_user_list[i][1]
			approx_set.append(ord_user_list[i][0])

	print "approx_set = %s" % approx_set
	return approx_set

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