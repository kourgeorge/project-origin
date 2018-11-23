from stats import Stats


def print_step_stats(step_stats_dict):
    for (key, value) in step_stats_dict.items():
        print('{}: {}'.format(key, value), end=' | ')
    print()


# def log_step_stats(file_path, universe):
#     step_stats = Stats.collect_step_stats(universe)
#     exists = os.path.isfile(file_path)
#     if not exists:
#         with open(file_path, 'a', newline='') as myfile:
#             wr = csv.writer(myfile, quoting=csv.QUOTE_NONNUMERIC)
#             wr.writerow(list(step_stats.keys()))
#             myfile.close()
#
#     with open(file_path, 'a', newline='') as myfile:
#         wr = csv.writer(myfile, quoting=csv.QUOTE_NONNUMERIC)
#         wr.writerow(step_stats.values())
#         myfile.close()


def print_epoch_stats(universe):
    epoch_stats = Stats.collect_epoch_states(universe)
    for (key, value) in epoch_stats.items():
        print('{}: {}'.format(key, value))
