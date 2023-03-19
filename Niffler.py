#!/usr/bin/env python3

from typing import Tuple, List, Dict
from sys import argv
from os import walk, mkdir, environ, system
from os.path import isdir, isfile, join, basename
from string import punctuation


# WARNING: Linux/Unix compatible only!
def ensureDependencies(installPath: str, indexPath: str) -> bool:
    try:
        if not isdir(installPath):
            mkdir(installPath)

        if not isfile(indexPath):
            system("touch " + indexPath)

        return True
    except:
        return False


def errorMessage(programName: str) -> None:
    print("\n'Niffler': Waiting for orders...")
    print(f"'Niffler': Try using '{programName} --help' for more information!")


def helpMessage(programName: str, supportedOptions: Dict[Tuple[str, str], str], supportedModifiers: Dict[Tuple[str, str], str]) -> None:
    print("\n'Niffler': A CLI tool for indexing the contents of text files in a searchable Inverted Index.\n")
    print(f"Usage: {programName} <OPTION> [FILE.../WORD]\n")

    print("Options:")
    for keyPair, optionDescription in supportedOptions.items():
        shortVersion, fullVersion = keyPair
        print(f"{'' + shortVersion +  ', ' + fullVersion:<30} {optionDescription}")


    print("\nModifiers:")
    for keyPair, modifierDescription in supportedModifiers.items():
        shortVersion, fullVersion = keyPair
        print(f"{'' + shortVersion +  ', ' + fullVersion:<30} {modifierDescription}")

    print("\nReleased under MIT by @gersonfaneto")


def validateOption(supportedOptions: Dict[Tuple[str, str], str], recievedOption: str, hasComplement: bool = True) -> bool:
    for keyPair, optionDescription in supportedOptions.items():
        if recievedOption in keyPair and hasComplement:
            return True
        elif recievedOption in keyPair and not hasComplement:
            print(f"You selected the '{recievedOption}' option! {optionDescription}")
            return False

    print(f"You selected the '{recievedOption}' option! 'Niffler' doesn't know this one...")
    return False


def validateModifiers(supportedModifiers: Dict[Tuple[str, str], str], recievedModifier: str, hasComplement: bool = True) -> bool:
    for keyPair, _ in supportedModifiers.items():
        if recievedModifier in keyPair and hasComplement:
            return True
        elif recievedModifier in keyPair and not hasComplement:
            print(f"You used the '{recievedModifier}' modifier! By itself it doesn't do anything!")
            return False

    print(f"You used the '{recievedModifier} modifier! 'Niffler' doesn't know this one...")
    return False


def validatePaths(recievedPaths: List[str]) -> Tuple[List[str], List[str]]:
    validPaths: List[str] = []
    invalidPaths: List[str] = []

    for currentPath in recievedPaths:
        if isdir(currentPath):
            for rootPath, _, filePaths in walk(currentPath):
                for filePath in filePaths:
                    if isfile(join(rootPath, filePath)):
                        validPaths.append(join(rootPath, filePath))
                    else:
                        invalidPaths.append(join(rootPath, filePath))
        elif isfile(currentPath):
            validPaths.append(currentPath)
        else:
            invalidPaths.append(currentPath)

    return validPaths, invalidPaths


def validateArguments(programName: str, supportedOptions: Dict[Tuple[str, str], str], supportedModifiers: Dict[Tuple[str, str], str],
                      recievedOptions: List[str], recievedModifiers: List[str], recievedComplements: List[str]) -> bool:
    if len(recievedOptions) == 0:
        if len(recievedModifiers) == 0 and len(recievedComplements) == 0:
            errorMessage(programName)
            return False
        elif len(recievedModifiers) == 1 and len(recievedComplements) == 0:
            validateModifiers(supportedModifiers, recievedModifiers[0], False)
            return False
        else:
            print("'Niffler' didn't detect any orders! Use the '--help' or '-h' flags for detailed usage information!")
            return False

    if len(recievedOptions) > 1:
        print("'Niffler': Sorry! Can only handle ONE operation at a time!")
        return False

    if len(recievedOptions) == 1:
        if recievedOptions[0] in ["-h", "--help"]:
            helpMessage(programName, supportedOptions, supportedModifiers)
            return True

        if len(recievedModifiers) == 1 and len(recievedComplements) == 0:
            return validateOption(supportedOptions, recievedOptions[0], False)

        if len(recievedModifiers) == 1 and len(recievedComplements) > 0:
            if validateModifiers(supportedModifiers, recievedModifiers[0]):
                return validateOption(supportedOptions, recievedOptions[0])
            else:
                return False

        if recievedOptions in ["-s", "--search-index"] and len(recievedComplements) == 1:
            return True
        if recievedOptions in ["-s", "--search-index"] and len(recievedComplements) == 0:
            return validateOption(supportedOptions, recievedOptions[0], False)

        if recievedOptions in ["-S", "--show-index"] and len(recievedComplements) == 0:
            return True
        if recievedOptions in ["-S", "--show-index"] and len(recievedComplements) > 0:
            return validateOption(supportedOptions, recievedOptions[0], False)

        if len(recievedComplements) > 0:
            return validateOption(supportedOptions, recievedOptions[0])
        else:
            return validateOption(supportedOptions, recievedOptions[0], False)

    return True


def readFile(filePath: str) -> List[str]:
    with open(filePath) as currentFile:
        return currentFile.read().splitlines()


def writeCache(cachePath: str, invertedIndex: Dict[str, Dict[str, int]]) -> None:
    with open(cachePath, "w+") as indexCache:
        for word in invertedIndex.keys():
            indexCache.write(f"[{word}]:{invertedIndex[word]}\n")


def readCache(cachePath: str, invertedIndex: Dict[str, Dict[str, int]]) -> None:
    with open(cachePath, "r") as indexCache:
        for line in indexCache.readlines():
            word, wordInfo = line.split(":", 1)
            invertedIndex[word] = eval(wordInfo)


def indexFile(filePath: str, invertedIndex: Dict[str, Dict[str, int]]) -> None:
    fileContent: List[str] = readFile(filePath)

    for line in fileContent:
        for word in line.split():
            newWord: str = "".join(filter(lambda x: x not in punctuation, word.upper()))
            qntOcurrences: int = line.split().count(word)

            if len(newWord) == 0:
                continue

            if newWord in invertedIndex.keys():
                if filePath in invertedIndex[newWord].keys():
                    invertedIndex[newWord][filePath] += qntOcurrences
                else:
                    invertedIndex[newWord][filePath] = qntOcurrences
            else:
                invertedIndex[newWord] = {filePath: qntOcurrences}


def showIndex(invertedIndex: Dict[str, Dict[str, int]]) -> None:
    for word in invertedIndex.keys():
        print(f"{word}: ")
        for filePath, qntOcurrences in invertedIndex[word].items():
            print(f"IN: {filePath} - OCURRENCES: {qntOcurrences}")
        print()


def searchIndex(chosenTerm: str, invertedIndex: Dict[str, Dict[str, int]]) -> None:
    possibleKey: str = chosenTerm.upper()
    if possibleKey.upper() in invertedIndex.keys():
        print(f"\n'Niffler': Found the following ocurrences for '{chosenTerm.title()}'!\n")
        for filePath, qntOcurrences in invertedIndex[possibleKey].items():
            print(f"IN: {filePath} - OCURRENCES: {qntOcurrences}")
    else:
        print(f"\n'Niffler': '{chosenTerm.title()}' not found!\n")


def main() -> None:

    homePath: str = environ['HOME']
    installPath: str = homePath + "/.niffler/"
    invertedIndexCache: str = installPath + "InvertedIndex.niffler"

    programName: str = argv.pop(0)

    supportedOptions: Dict[Tuple[str, str], str] = {
        ("-h", "--help"): "'Niffler' shows you his abilities!",
        ("-a", "--add"): "Give a FILE (or some) to 'Niffler' and it will analyze it!",
        ("-r", "--remove"): "Give a FILE (or some) to 'Niffler' and it will be erased from his knowledge!",
        ("-s", "--search-index"): "Give a WORD to 'Niffler' and he will find its ocurrences on the Index!",
        ("-S", "--show-index"): "Displays 'Niffler' immense knowledge, use with caution!",
    }
    supportedModifiers: Dict[Tuple[str, str], str] = {
        ("-v", "--verbose"): "Extends the output information of some operations."
    }

    recievedOptions: List[str] = list(filter(lambda x: x in [y for z in supportedOptions.keys() for y in z], argv))
    recievedModifiers: List[str] = list(filter(lambda x: x in [y for z in supportedModifiers.keys() for y in z], argv))
    recievedComplements: List[str] = list(set(argv) - set(recievedOptions) - set(recievedModifiers))

    invertedIndex: Dict[str, Dict[str, int]] = {}

    if not ensureDependencies(installPath, invertedIndexCache):
        print("'Niffler': Couldn't create nedded dependencies!")
        exit(1)
    else:
        readCache(invertedIndexCache, invertedIndex)

    if not validateArguments(programName, supportedOptions, supportedModifiers, recievedOptions, recievedModifiers, recievedComplements):
        exit(1)

    validPaths, invalidPaths = validatePaths(recievedComplements)
    chosenOption: str = recievedOptions[0] if len(recievedOptions) > 0 else ""
    chosenModifier: str = recievedModifiers[0] if len(recievedModifiers) > 0 else ""
    chosenWord: str = recievedComplements[0] if len(recievedComplements) > 0 else ""

    if chosenOption in ["-h", "--help"]:
        pass
    elif chosenOption in ["-a", "--add"]:
        if chosenModifier in ["-v", "--verbose"]:
            if len(invalidPaths) > 0:
                print("\n'Niffler': The following files were out of reach!\n")
                for currentPath in invalidPaths:
                    print(f"- {basename(currentPath)}")
            
            if len(validPaths) > 0:
                print("\n'Niffler': Indexing the following files...\n")
                for currentPath in validPaths:
                    print(f"- {basename(currentPath)}")
        for currentPath in validPaths:
            indexFile(currentPath, invertedIndex)
    elif chosenOption in ["-r", "--remove"]:
        pass
    elif chosenOption in ["-s", "--search-index"]:
        searchIndex(chosenWord, invertedIndex)
    elif chosenOption in ["-S", "--show-index"]:
        showIndex(invertedIndex)
    else:
        print(f"'Niffler': Sorry! The option '{chosenOption}' is not implemented yet!")

    writeCache(invertedIndexCache, invertedIndex)


if __name__ == "__main__":
    main()
