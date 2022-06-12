import os
# from src.ExperimentStages import *

def generate_arguments(args_dict):
	res = ""
	for arg_name, value in args_dict.items():
		res = res + "--" + arg_name + " " + str(value) + " "
	return res

def run_script(script, args_dict):
	arguments = generate_arguments(args_dict)
	return os.system("python " + script + " " + arguments)

def get_phone_count(phones_list_path):
	phones_list_fh = open(phones_list_path)
	phone_count = 0
	for line in phones_list_fh.readlines():
		line = line.split()
		use_current_phone = int(line[2])
		phone_count += use_current_phone
	return phone_count

def get_run_name(config_yaml, use_heldout=False):
	heldout_suffix = ''
	if use_heldout:
		heldout_suffix = '_heldout'
	return os.path.basename(config_yaml).split('.')[0] + heldout_suffix

def get_experiment_directory(config_yaml, use_heldout=False):
	return "experiments/" + get_run_name(config_yaml, use_heldout) + '/'

def add_data_keys_to_config_dict(config_dict, setup):

	if setup == "dataprep":
		data_dir_key = "output-dir"
		config_dict["ref-labels-dir-path"]   = config_dict["data-root-path"]
	else:
		data_dir_key = "data-dir"

	data_path = config_dict[data_dir_key]
	config_dict["alignments-dir-path"]   = data_path + "alignments/"
	config_dict["alignments-path"]       = config_dict["alignments-dir-path"] + "align_output"
	config_dict["heldout-align-path"]    = config_dict["alignments-dir-path"] + "align_output_heldout"
	config_dict["loglikes-path"]         = config_dict["alignments-dir-path"] + "loglikes.ark"
	config_dict["loglikes-heldout-path"] = config_dict["alignments-dir-path"] + "loglikes_heldout.ark"
	config_dict["acoustic-model-path"]   = data_path + "pytorch_models/acoustic_model.pt"
	config_dict["features-path"]         = data_path + "features/data"
	config_dict["features-conf-path"]    = data_path + "features/conf"
	config_dict["auto-labels-dir-path"]  = data_path + "kaldi_labels/"
	config_dict["utterance-list-path"]   = data_path + "/epadb_full_path_list.txt"
	config_dict["train-list-path"]       = data_path + "/epadb_full_path_list.txt"
	config_dict["test-list-path"]        = data_path + "/heldout_full_path_list.txt"
	config_dict["reference-trans-path"]  = data_path + "/reference_transcriptions.txt"
        

	return config_dict

