#!/usr/bin/env python3

from typing import Tuple, List, Dict
from sys import argv
from os import mkdir, environ, system
from os.path import isdir, isfile

SupportedArguments: Dict[Tuple[str, str], str] = {
    ("-a", "--add"): "Give a file (or some) to 'Niffler' and it will analyze it!",
    ("-r", "--remove"): "Give a file to 'Niffler' and it will erase from his knowledge!",
    ("-s", "--search-index"): "Give a term/word to 'Niffler' and he will find its ocurrences on the Index!",
    ("-S", "--show-index"): "Displays 'Niffler' immense knowledge, use with caution!",
}

ProgramName: str = argv.pop(0)
Arguments: List[str] = [
    x for x in argv if x.startswith("-") or x.startswith("--")
]


def validateArguments(recievedArgs: List[str]) -> bool:
    if len(recievedArgs) == 0:
        print("Error: 'Niffler' must recieve a command to execute!")
        exit(1)

    if len(recievedArgs) > 1:
        print("Error: 'Niffler' can only run ONE operation at a time!")
        exit(1)

    for keyPair, argDescription in SupportedArguments.items():
        if recievedArgs[0] in keyPair:
            print(argDescription)
            return True
    return False


# WARNING: Linux/Unix compatible only!
def ensureDependencies() -> bool:
    try:
        HOME_PATH: str = environ['HOME']
        INSTALL_PATH: str = HOME_PATH + "/.niffler/"
        INDEX_PATH: str = INSTALL_PATH + "InvertedIndex.niffler"
        IGNORE_PATH: str = INSTALL_PATH + "Ignore.niffler"

        if not isdir(INSTALL_PATH):
            mkdir(INSTALL_PATH)

        if not isfile(INDEX_PATH):
            system("touch " + INDEX_PATH)

        if not isfile(IGNORE_PATH):
            system("touch " + IGNORE_PATH)

        return True
    except:
        return False


def main() -> None:
    if not ensureDependencies():
        print("Error: Couldn't create nedded dependencies!")
        exit(1)

    if not validateArguments(Arguments):
        print(f"Usage: {ProgramName} <OPTION> [FILES...]")


if __name__ == "__main__":
    main()
