__author__ = 'gkour'

import os


def print_step_stats(stats):
    printing_stats = stats.step_stats_df.drop(columns=['CreaturesDist', 'FoodDist']).tail(1)
    print(printing_stats.to_json(orient='records'))


def dataframe2csv(data_frame, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data_frame.to_csv(path_or_buf=file_path, index=False)


def print_epoch_stats(stats):
    last_update = stats.epoch_stats_df.tail(1).to_dict()
    for (key, value) in last_update.items():
        print('{}: {}'.format(key, value))
