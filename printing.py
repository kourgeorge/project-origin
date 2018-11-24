__author__ = 'gkour'


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


def print_epoch_stats(stats):
    for (key, value) in stats.epoch_stats_df.tail(1):
        print('{}: {}'.format(key, value))
