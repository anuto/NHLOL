from db.mongo_wrapper import *
from constants import NUMBER_MAP
from datetime import datetime, timedelta

def process_combo(combo, combos):
	combo_length = len(combo)

	if combo_length <= 1:
		return

	if combo_length not in combos:
		combos[combo_length] = []

	combos[combo_length].append(combo)

def print_combos(combos):
	for combo in sorted(combos):
		print(NUMBER_MAP[combo] + " goals in 2024-2025: " + \
			str(len(combos[combo])))


def process_all_multigoals(query = {}):
	multigoals = get_collection('multigoals', query)

	combos = {}

	for row in multigoals:
		combo = row['combo']
		process_combo(combo, combos)

	print_combos(combos)
	return combos

def process_multigoals_by_period(query = {}):
	multigoals = get_collection('multigoals', query)

	combos = {}

	for row in multigoals:
		combo = row['combo']

		period_1 = [goal for goal in combo if goal['periodNumber'] == 1]
		period_2 = [goal for goal in combo if goal['periodNumber'] == 2]
		period_3 = [goal for goal in combo if goal['periodNumber'] == 3]

		process_combo(period_1, combos)
		process_combo(period_2, combos)
		process_combo(period_3, combos)

	print_combos(combos)
	return combos

def process_period_with_time_limit(period_goals, max_delta, combos):
	prev_time_scored = None
	combo = []

	for goal in period_goals:

		time_in_period = goal['timeInPeriod']
		time_scored = datetime.strptime(time_in_period, "%M:%S")

		if prev_time_scored:
			delta = time_scored - prev_time_scored			
			if delta < max_delta:
				combo.append(goal)

			else:
				process_combo(combo, combos)
				combo = [goal]
		else:
			combo.append(goal)

		prev_time_scored = time_scored

	process_combo(combo, combos)
	return combos

def process_multigoals_by_period_with_time_limit(max_delta, query = {}):
	multigoals = get_collection('multigoals', query)

	combos = {}
	max_time_delta = timedelta(seconds = max_delta)

	for row in multigoals:
		combo = row['combo']

		period_1 = [goal for goal in combo if goal['periodNumber'] == 1]
		period_2 = [goal for goal in combo if goal['periodNumber'] == 2]
		period_3 = [goal for goal in combo if goal['periodNumber'] == 3]

		process_period_with_time_limit(period_1, max_time_delta, combos)
		process_period_with_time_limit(period_2, max_time_delta, combos)
		process_period_with_time_limit(period_3, max_time_delta, combos)

	print_combos(combos)
	return combos