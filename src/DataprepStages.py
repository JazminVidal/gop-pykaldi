import src.dataprep.align as align
import src.dataprep.create_kaldi_labels as create_kaldi_labels
import src.dataprep.prepare_data as prepare_data
from src.Stages import AtomicStage

class PrepareFeaturesAndModelsStage(AtomicStage):
    _name = "features"

    def run(self):
        prepare_data.main(self._config_dict)

class AlignCrossValStage(AtomicStage):
    _name = "align_crossval"

    def run(self):
        align.main(self._config_dict)

class AlignHeldoutStage(AtomicStage):
    _name = "align_heldout"

    def run(self):
        config_dict = self._config_dict

        config_dict['utterance-list-path'] = config_dict['test-list-path']
        config_dict['alignments-path']     = config_dict['heldout-align-path']
        config_dict['loglikes-path']       = config_dict['loglikes-heldout-path']
        align.main(config_dict)

class CreateLabelsCrossValStage(AtomicStage):
    _name = "labels_crossval"

    def run(self):
        create_kaldi_labels.main(self._config_dict)

class CreateLabelsHeldoutStage(AtomicStage):
    _name = "labels_heldout"

    def run(self):
        config_dict = self._config_dict
        config_dict['utterance-list-path']  = config_dict['test-list-path']
        config_dict['alignments-path']      = config_dict['heldout-align-path']
        create_kaldi_labels.main(config_dict)
