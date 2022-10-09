
import os
import json
import pickle
import logging
import utils.definitions as ontology

def save_json(obj, save_path, indent=4):
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)


def load_json(load_path, lower=True):
    with open(load_path, "r", encoding="utf-8") as f:
        obj = f.read()

        if lower:
            obj = obj.lower()

        return json.loads(obj)


def save_pickle(obj, save_path):
    with open(save_path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(load_path):
    with open(load_path, "rb") as f:
        return pickle.load(f)


def save_text(obj, save_path):
    with open(save_path, "w", encoding="utf-8") as f:
        for o in obj:
            f.write(o + "\n")


def load_text(load_path, lower=True):
    with open(load_path, "r", encoding="utf-8") as f:
        text = f.read()
        if lower:
            text = text.lower()
        return text.splitlines()


def get_or_create_logger(logger_name=None, log_dir=None):
    logger = logging.getLogger(logger_name)

    # check whether handler exists
    if len(logger.handlers) > 0:
        return logger

    # set default logging level
    logger.setLevel(logging.DEBUG)

    # define formatters
    stream_formatter = logging.Formatter(
        fmt="%(asctime)s  [%(levelname)s] %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S")

    file_formatter = logging.Formatter(
        fmt="%(asctime)s  [%(levelname)s] %(module)s; %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S")

    # define and add handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    if log_dir is not None:
        file_handler = logging.FileHandler(os.path.join(log_dir, "log"))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger

def aspan_to_act_list( aspan):
    aspan = aspan.split() if isinstance(aspan, str) else aspan
    acts = []
    domain = None
    conslen = len(aspan)
    for idx, cons in enumerate(aspan):
        #cons =vocab.decode(cons) if type(cons) is not str else cons
        if cons == '<eos_a>':
            break
        if '[' in cons and cons[1:-1] in ontology.dialog_acts:
            domain = cons[1:-1]

        elif '[' in cons and cons[1:-1] in ontology.dialog_act_params:
            if domain is None:
                continue
            vidx = idx+1
            if vidx == conslen:
                acts.append(domain+'-'+cons[1:-1]+'-none')
                break
            vt = aspan[vidx]
            #vt = self.vocab.decode(vt) if type(vt) is not str else vt
            no_param_act = True
            while vidx < conslen and vt != '<eos_a>' and '[' not in vt:
                no_param_act = False
                acts.append(domain+'-'+cons[1:-1]+'-'+vt)
                vidx += 1
                if vidx == conslen:
                    break
                vt = aspan[vidx]
                #vt = self.vocab.decode(vt) if type(vt) is not str else vt
            if no_param_act:
                acts.append(domain+'-'+cons[1:-1]+'-none')

    return acts
