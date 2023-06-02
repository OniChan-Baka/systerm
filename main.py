import wikipedia
import webbrowser
import requests
from json import load
from datetime import timedelta
from fuzzywuzzy.process import extractOne
from subprocess import Popen
from os import system



def main():
    opera_path = r"C:\\Users\\famal\\AppData\\Local\\Programs\\Opera GX\\opera.exe"
    webbrowser.register('opera', None,webbrowser.BackgroundBrowser(opera_path))
    opera = webbrowser.get('opera')
    with open(r"C:\\Data\\Programming\\Python\\sysTerm\\appPaths.json", "r") as f:
        appsPaths = load(f)
    with open(r"C:\\Data\\Programming\\Python\\sysTerm\\spotify.json", "r") as f:
        spotifyInfo = load(f)
    playListUrl = "https://open.spotify.com/playlist/4PPFMow4DCYoIFTrOrBEB3?si=87803a5faa7a4848"
    while True:
        args = input('> ')
        print(' ')
        args = args.split(' ')
        backend(args, appsPaths, opera, spotifyInfo, playListUrl)

def backend(args, paths, opera, spotifyInfo, playListUrl):
    if args[0] != '':
        if args[0] == 'exit' or args[0].lower() == 'e':
            print("Exiting...")
            exit()
        elif args[0].lower() == 'wiki' or args[0].lower() == 'wikipedia' or args[0].lower() == 'w':
            args.pop(0)
            wiki(args)
        elif args[0].lower() == 'open' or args[0].lower() == 'o':
            args.pop(0)
            openApp(args, paths)
        elif args[0].lower() == 'youtube' or args[0].lower() == 'y':
            args.pop(0)
            openWeb('https://www.youtube.com', opera)
        elif args[0].lower() == 'github' or args[0].lower() == 'g':
            args.pop(0)
            openWeb('https://github.com', opera)
        elif args[0].lower() == 'chatgpt' or args[0].lower() == 'chat' or args[0].lower() == 'c':
            args.pop(0)
            openWeb('https://chat.openai.com/?model=text-davinci-002-render-sha', opera)
        elif args[0].lower() == 'whatsapp':
            args.pop(0)
            openWeb('https://web.whatsapp.com/', opera)
        elif args[0].lower() == 'monkeytype' or args[0].lower() == 'type':
            args.pop(0)
            openWeb('https://monkeytype.com', opera)
        elif args[0] == 'url' or args[0] == 'u':
            args.pop(0)
            openWeb(args[0], opera)
        elif args[0].lower() == 'play' or args[0].lower() == 'p': # TODO: after writing the funtions add the funtions here.
            args.pop(0)
            play()
        elif args[0].lower() == 'next' or args[0].lower() == '>': # TODO: after writing the funtions add the funtions here.
            args.pop(0)
            nextSong()
        elif args[0].lower() == 'restart' or args[0].lower() == 'r':
            print("Restarting...\n")
            system('python restart.py')
            exit()
        elif args[0].lower() == 'clear' or args[0].lower() == 'cls':
            system('python clear.py')
            exit()

        else:
            print("Invalid command.\n")
    else:
        print("No arguments received.\n")

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
    print(f"Opening {args}\n")
    if len(args) > 0:
        match = matchkey(args, paths)
        if match:
            Popen(paths[match], shell=True)
        else:
            print(f"No app found for {args}\n")

def matchkey(args, paths):
    appList = paths.keys()
    match, percent = extractOne(args, appList) # type: ignore
    if percent >= 80:
        return match

def openWeb(args, opera):
    print("Opening webPgae...\n")
    if args:
        opera.open_new_tab(args)
    else:
        print("no arguments recived.\n")

def play(): #TODO: after downloading the playlist finish the funtion to play the songs.
    pass

def nextSong(): #TODO: after te play funtion add a funtion to go to the next sond and the previous song.
    pass


if __name__ == '__main__':
    main()
