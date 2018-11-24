__author__ = 'gkour'

import numpy as np


def print_step_stats(stats):
    last_update = stats.step_stats_df.tail(1)
    print(last_update.to_json(orient='records'))


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
    last_update = stats.epoch_stats_df.tail(1).to_dict()
    for (key, value) in last_update.items():
        print('{}: {}'.format(key, value))
