import os
from src.Stages import AtomicStage


def make_experiment_directory(experiment_dir_path, setup):
    #This will create the experiment directory and the test sample list, 
    #state dict, and gop scores directories inside of it
    test_sample_lists_dir  = experiment_dir_path + "/test_sample_lists/"
    train_sample_lists_dir = experiment_dir_path + "/train_sample_lists/"
    gop_scores_dir         = experiment_dir_path + "/gop_scores/"
    eval_dir               = experiment_dir_path + "/eval/"
    
    if not os.path.exists(test_sample_lists_dir) and setup == "exp":
        os.makedirs(test_sample_lists_dir)
    if not os.path.exists(train_sample_lists_dir) and setup == "exp":
        os.makedirs(train_sample_lists_dir)
    if not os.path.exists(gop_scores_dir):
        os.makedirs(gop_scores_dir)
    if not os.path.exists(eval_dir):
        os.makedirs(eval_dir)

def check_if_config_exists(config_path):
    if not os.path.exists(config_path):
        raise Exception('Config with path %s not found.' %(config_path) )

class CreateExperimentDirectoryStage(AtomicStage):
    _name = "prepdir"
    def run(self):
        make_experiment_directory(self._config_dict["experiment-dir-path"], "exp")


