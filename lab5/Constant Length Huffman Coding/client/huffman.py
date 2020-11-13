r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""


def getCharacters(inputString):
    variables = []
    for it in inputString:
        if it not in variables:
            variables.append(it)
    return sorted(variables)


def getCodes(inputList):
    codes = {}
    for i, it in enumerate(inputList):
        codes[it] = i
    return codes


def huffmanEncode(inputString):
    variables = getCharacters(inputString)
    codes = getCodes(variables)
    encodedString = []
    for it in inputString:
        encodedString.append(codes[it])
    return encodedString, codes


def huffmanDecode(codes, encodedString):
    inputString = ""
    keys = list(codes.keys())
    values = list(codes.values())
    for it in encodedString:
        inputString += keys[values.index(it)]
    return inputString
