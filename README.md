# MTTOD-modified

The original code is for the paper "Improving End-to-End Task-Oriented Dialogue System with A Simple Auxiliary Task".

Upon that we add little modification to support Markovian training for the paper "Building Markovian Generative Architectures over Pretrained LM Backbones for Efficient Task-Oriented Dialog Systems".

## checkout source code and data from github repository
To download data.zip properly, git lfs(Large File Storage) extension must be installed.

```
# clone repository as usual
git clone https://github.com/bepoetree/MTTOD.git
cd MTTOD
# check file size of data.zip
ls -l data.zip

# The file size of data.zip is about 33 MB. If not, git-lfs is not installed or failed to checked out correctly.
# please ensure to install git-lfs (in Ubuntu or Debian, execute "apt install git-lfs" with sudo) in your system.
# After then, Retrying LFS checkout with the following commands:
git lfs install
git lfs pull
git checkout -f HEAD
```

## Environment setting

Our python version is 3.6.9.

The package can be installed by running the following command.

```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Data Preprocessing

For the experiments, we use MultiWOZ2.0 and MultiWOZ2.1.
- (MultiWOZ2.0) annotated_user_da_with_span_full.json: A fully annotated version of the original MultiWOZ2.0 data released by developers of Convlab available [here](https://github.com/ConvLab/ConvLab/tree/master/data/multiwoz/annotation).
- (MultiWOZ2.1) data.json: The original MultiWOZ 2.1 data released by researchers in University of Cambrige available [here](https://github.com/budzianowski/multiwoz/tree/master/data).

We use the preprocessing scripts implemented by [Zhang et al., 2020](https://arxiv.org/abs/1911.10484). Please refer to [here](https://github.com/thu-spmi/damd-multiwoz/blob/master/data/multi-woz/README.md) for the details.

```
python preprocess.py -version $VERSION
```

## Training

Our implementation supports a single GPU. Please use smaller batch sizes if out-of-memory error raises.

- MTTOD without auxiliary task (for the ablation)
```
python main.py -version $VERSION -run_type train -model_dir $MODEL_DIR
```

- MTTOD without auxiliary task  + Markovian generation architecture
```
python main.py -version $VERSION -run_type train -model_dir $MODEL_DIR -simplify
```

- MTTOD with auxiliary task
```
python main.py -version $VERSION -run_type train -model_dir $MODEL_DIR -add_auxiliary_task
```

The checkpoints will be saved at the end of each epoch (the default training epoch is set to 10).

## Inference

```
python main.py -run_type predict -ckpt $CHECKPOINT -output $MODEL_OUTPUT -batch_size $BATCH_SIZE
```

All checkpoints are saved in ```$MODEL_DIR``` with names such as 'ckpt-epoch10'.

The result file (```$MODEL_OUTPUT```) will be saved in the checkpoint directory.

To reduce inference time, it is recommended to set large ```$BATCH_SIZE```. In our experiemnts, it is set to 16 for inference.

## Evaluation

The original evaluation scripts implemented by [Zhang et al., 2020](https://arxiv.org/abs/1911.10484).
We use the evaluation scripts by [Tomas et al., 2021](https://arxiv.org/abs/2106.05555v1), which is also the official scripts in https://github.com/budzianowski/multiwoz

```
python evaluator.py -data $CHECKPOINT/$MODEL_OUTPUT
```

To evaluate result for Markovian generation architecture
```
python evaluator.py -data $CHECKPOINT/$MODEL_OUTPUT -simplify
```
## Acknowledgements

This code is based on the released code (https://github.com/thu-spmi/damd-multiwoz/) for "Task-Oriented Dialog Systems that Consider Multiple Appropriate Responses under the Same Context", which distributed under Apache License Version 2.0. 
Copyright 2019- Yichi Zhang.

For the pre-trained language model, we use huggingface's Transformer (https://huggingface.co/transformers/index.html#), which distributed under Apache License Version 2.0. 
Copyright 2018- The Hugging Face team. All rights reserved.

We are grateful for their excellent works.
