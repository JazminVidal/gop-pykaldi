# Goodness of Pronunciation Algorithm on EpaDB using Pykaldi

This repository has the code to perform the Goodness of Pronunciation algorithm using Pykaldi. It is meant to facilitate experimentation with EpaDB, a database of non-native English speech by Spanish speakers from Argentina intended for research on mispronunciation detection and development of pronunciation scoring systems. 

The Goodness of Pronunciation (GOP) method [1] estimates scores for each phone in a phrase as the posterior probabilities of the target phones (i.e., the phones the student should pronounce) computed using the acoustic model from an automatic speech recognition (ASR) system trained only on native data.
Traditionally, GOP scores were computed using GMM-based acoustic models. In recent years, though, significant improvements have been shown using DNN-based acoustic models [2]. In these cases, the GOP score for a target phone p that starts at frame T and has a length of D frames is computed as:

$GOP(p)=$ $-\frac{1}{D}$ $\sum_{t=T}^{T+D-1}\log P_t(p|O)$

where O is the full sequence of features for the waveform and $P_t(p|O)$ is an estimate of the posterior probability for phone p at frame t. The start and end frames for each target phone are obtained using a forced-aligner given the word transcription. 

The system uses a PyTorch acoustic model based on Kaldi's TDNN-F acoustic model so a script is provided to convert Kaldi's model to PyTorch.


## Table of Contents
* [Prerequisites](#prerequisites)
* [How to install](#how-to-install)
* [Data preparation](#data-preparation)
* [How to run the GOP recipe](#how-to-run-the-GOP-recipe)
* [Copyright](#copyright)
* [References](#references)

## Prerequisites
1. [Kaldi](http://kaldi-asr.org/) installed.
2. TextGrid managing library installed using pip. Instructions at this [link](https://pypi.org/project/praat-textgrids/).
3. The EpaDB database downloaded (you can ask for it at jvidal@dc.uba.ar). 

## How to install
To install this repository, follow this steps:

1. Clone this repository:
```
git clone https://github.com/JazminVidal/gop-pykaldi.git
```
2. Install the requirements:
```
pip install -r requirements.txt
```
3. Install PyKaldi:
Follow instructions from https://github.com/pykaldi/pykaldi#installation


## Data preparation
Before using the system it is necessary to run the data preparation script. This step handles feature extraction, downloads the Librispeech ASR acoustic model from OpenSLR, converts said model to PyTorch and creates forced alignments and training labels. This should only be done once unless EpaDB is updated, in which case new features, labels, and alignments need to be generated.

To run data preparation use:
```
python run_dataprep.py --config configs/dataprep.yaml
```

## How to run the GOP recipe
For computing GOP, we recreate the official Kaldi recipe in PyKaldi. We use the Kaldi Librispeech ASR model, a TDNN-F acoustic model, ported to PyTorch in the previous stage. 

To run the GOP recipe use:
```
python run_gop.py --config configs/gop.yaml --from STAGE --to STAGE
```
STAGE can be one of the following: prep, gop, evaluate.

To run all stages, use ``` --from prep --to evaluate ```


## Copyright
The code in this repository and the EpaDB database were developed at the Speech Lab at Universidad de Buenos Aires, Argentina and are freely available for research purposes. 

If you use the EpaDB database, please cite the following paper:

*J. Vidal, L. Ferrer, L. Brambilla, "EpaDB: a database for the development of pronunciation assessment systems", [isca-speech](https://www.isca-speech.org/archive/Interspeech_2019/abstracts/1839.html)*

```
@article{vidal2019epadb,
  title={EpaDB: a database for development of pronunciation assessment systems},
  author={Vidal, Jazmin and Ferrer, Luciana and Brambilla, Leonardo},
  journal={Proc. Interspeech 2019},
  pages={589--593},
  year={2019}
}
```

If you use the code in this repository, please cite the following paper:

*M. Sancinetti, J. Vidal, C. Bonomi, L.Ferrer, "A transfer learning approach for pronunciation scoring", [Arxiv](https://arxiv.org/pdf/2111.00976.pdf)*

```
@article{sancinetti2021transfer,
  title={A transfer learning based approach for pronunciation scoring},
  author={Sancinetti, Marcelo and Vidal, Jazmin and Bonomi, Cyntia and Ferrer, Luciana},
  journal={arXiv preprint arXiv:2111.00976},
  year={2021}
}
}
```

## References
* [1] S.M. Witt and S.J. Young, “Phone-level pronunciation scoring and assessment for interactive language learning,” Speech
communication, vol. 30, no. 2-3, pp. 95–108, 2000.
* [2]







