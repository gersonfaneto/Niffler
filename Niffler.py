#!/usr/bin/env python3

from sys import argv
from os import mkdir, environ, system
from os.path import isdir, isfile

Arguments = {
    ("-a", "--add"): "Give a file (or some) to 'Niffler' and it will analyze it!",
    ("-r", "--remove"): "Give a file to 'Niffler' and it will erase from his knowledge!",
    ("-s", "--search-index"): "Give a term/word to 'Niffler' and he will find it's ocurrences on the Index!",
    ("-S", "--show-index"): "Displays 'Niffler' immense knowledge, use with caution!",
}

ProgramName = argv.pop(0)


def validateArgument(recievedArg: str) -> bool:
    for keyPair, argDescription in Arguments.items():
        if recievedArg in keyPair:
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

    if len(argv) == 0 or not validateArgument(argv[0]):
        print(f"Usage: {ProgramName} <OPTION> [FILES...]")


if __name__ == "__main__":
    main()
