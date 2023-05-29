import wikipedia
from datetime import timedelta
import requests
from json import load
from fuzzywuzzy.process import extractOne
from subprocess import Popen


def main():
    with open(r"C:\Data\Programming\Python\sysTerm\appPaths.json", "r") as f:
        appsPaths = load(f)
    while True:
        args = input()
        args = args.split(' ')
        backend(args, appsPaths)

def backend(args, paths):
    print("Arguments received:", args)
    if args[0] != '':
        if args[0] == 'exit' or args[0].lower() == 'x':
            print("Exiting...")
            exit()
        elif args[0].lower() == 'wiki' or args[0].lower() == 'wikipedia' or args[0].lower() == 'w':
            args.pop(0)
            wiki(args)
        elif args[0].lower() == 'open' or args[0].lower() == 'o':
            args.pop(0)
            openApp(args, paths)

        else:
            print("Invalid command.\n")
    else:
        print("No arguments received\n")

def wiki(args):
    args = " ".join(args)
    print(args)
    wikipedia.set_lang('en')
    wikipedia.set_rate_limiting(True, min_wait=timedelta(milliseconds=1000))
    print("Getting Info...")
    try:
        print(wikipedia.summary(args, sentences=2, auto_suggest=False), "\n")
    except wikipedia.DisambiguationError as e:
        print(f"There are multiple results for \"{args}\", Here are some suggestions:")
        ops = '\n'.join(e.options[0::5])
        print(ops)
    except wikipedia.exceptions.PageError as e:
        print("Invalid input, no page found matching the query. please cheack you spellings and try again.\n")
    except requests.exceptions.ConnectionError as e:
        print("No insternet connection.\n")

def openApp(args, paths):
    args = " ".join(args)
    print(f"Opening {args}")
    if len(args) > 0:
        match = matchkey(args, paths)
        if match:
            Popen(paths[match], shell=True)
        else:
            print(f"No app found for {args}\n")

def matchkey(args, paths):
    appList = paths.keys()
    match, percent = extractOne(args, appList)
    if percent > 80:
        return match


if __name__ == '__main__':
    main()
