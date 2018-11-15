__author__ = 'gkour'


class Config:
    gamma = 1
    total_episodes = 5000000
    update_frequency = 1
    lr = 1e-4
    max_interactions = 3
    model_path = "./model/mod.ckpt"
    logdir = "./log/tests"
    load_model = False
    eps = 0.1
    num_episodes_stats = 1000
    action_size = 5
    state_size = 3
    sess = None
    optimizer = None
