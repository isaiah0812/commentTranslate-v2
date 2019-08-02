import sys
from googletrans import Translator, LANGUAGES

translator = Translator()

args = sys.argv

def makeItNice(file, newFile):

    for x in file:
        if x == "\n":
            newFile.write('\n')
        else:
            newFile.write(x.replace('\n', ' '))


#   Version 2
#
#   Version 2 of this will not have the option to have the source and not the destination
#   destLang=None, srcLang=None -> Detect language to ENGLISH
#   destLang=String, srcLang=None -> Detect language to DESTLANG
#   destLang=String, srcLang=String -> SRCLANG to DESTLANG
def translateThisFile(file, destLang, srcLang):
    newFile = open(file.name[:len(file.name) - 3] + "-translated.py", "w")

    if destLang is None and srcLang is None:
        print("Translating file to ENGLISH...\n")

        for line in file:
            if line != "\n" and len(line) != 0:
                tLine = translator.translate(line).text
            elif line == "\n":
                tLine = line

            newFile.write(tLine)
    elif destLang is not None and srcLang is None:
        print("Translating file to " + LANGUAGES.get(destLang).upper() + "...\n")

        commentLine = ""
        comment = 0
        for line in file:
            if line.strip().startswith("#"):
                if comment == 0:
                    comment = 1
                if len(commentLine) > 0:
                    commentLine += " "
                commentLine += line.strip()[line.find("#") + 1:].strip()
            elif comment == 1:
                tLine = translator.translate(commentLine, dest=destLang).text
                newFile.write("#   " + tLine + "\n")
                newFile.write(line)
                comment = 0
            else:
                newFile.write(line)
    else:
        print("Translating file to " + LANGUAGES.get(destLang).upper() + "...\n")

        for line in file:
            if line != "\n" and len(line) != 0:
                tLine = translator.translate(line, dest=destLang, src=srcLang).text
            elif line == "\n":
                tLine = line

            newFile.write(tLine)

    newFile.close()
    print("File Translated! Check translated.txt")


if len(args) < 2 or len(args) > 4:
    print("Invalid command\n"
          "Usage: comm_translate.py <file name>\n"
          "OR"
          "Usage: comm_translate.py <file name> <destination language>\n"
          "OR"
          "Usage: comm_translate.py <file name> <source language> <destination language>",
          file=sys.stderr)
    exit(1)
elif len(args) == 2:
    f = open(args[1], "r")
    translateThisFile(f, None, None)
    f.close()
elif len(args) == 3:
    f = open(args[1], "r")
    translateThisFile(f, args[2], None)
    f.close()
else:
    f = open(args[1], "r")
    translateThisFile(f, args[3], args[2])
    f.close()