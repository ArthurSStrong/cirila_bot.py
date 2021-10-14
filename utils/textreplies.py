import csv
from pathlib import Path


data_folder = Path("utils/txt")

AF_DET = data_folder / "afecto_detonador.txt"
AF_RESP = data_folder / "afecto_respuesta.txt"
RESP_DEF = data_folder / "respuestas_por_defecto.txt"
REPLIES = data_folder / "contestaciones.csv"
CHAT_REPLIES = data_folder / "chat_detonador.csv"


def _load_replies(file):
    SORTS = dict()

    for row in csv.DictReader(open(file, "r", encoding="utf-8")):
        SORTS[row["detonador"]] = row["respuesta"]

    return SORTS


def _load_file(file):
    """Load the log file and creates it if it doesn't exist.
     Parameters
    ----------
    file : str
        The file to write down
    Returns
    -------
    list
        A list of strings.
    """

    try:
        with open(file, 'r', encoding='utf-8') as temp_file:
            return temp_file.read().splitlines()
    except Exception:

        with open(file, 'w', encoding='utf-8') as temp_file:
            return []


def get_any_dict(items, key_search):
    for item in list(items.keys()):
        if item in key_search:
            return items[item]
    return None


def get_af_det():
    return _load_file(AF_DET)

def get_af_resp():
    return _load_file(AF_RESP)

def get_def_resp():
    return _load_file(RESP_DEF)

def get_replies():
    return _load_replies(REPLIES)

def get_chat_replies():
    return _load_replies(CHAT_REPLIES)

