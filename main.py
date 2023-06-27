import os
import psutil
import requests
import wikipedia
import webbrowser
from json import load
from datetime import timedelta
from subprocess import Popen, DEVNULL
from fuzzywuzzy.process import extractOne


def main():
    Directory = os.getcwd()
    Directory = Directory.split('\\')
    Directory = Directory[-1]
    if Directory != 'systerm':
        os.chdir('systerm')
    opera_path = r"C:\\Users\\famal\\AppData\\Local\\Programs\\Opera GX\\opera.exe"
    webbrowser.register('opera', None, webbrowser.BackgroundBrowser(opera_path))
    opera = webbrowser.get('opera')
    with open(r"C:\\Data\\Programming\\Python\\sysTerm\\appPaths.json", "r") as f:
        appsPaths = load(f)
    while True:
        args = input('> ')
        print(' ')
        args = args.split(' ')
        backend(args, appsPaths, opera)

def backend(args, paths, opera):
    if args:
        if args == '':
            pass
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
        elif args[0].lower() == 'restart' or args[0].lower() == 'r':
            restart()
        elif args[0].lower() == 'clear' or args[0].lower() == 'cls':
            clear()
        elif args[0] == 'exit' or args[0].lower() == 'e':
            print("Exiting...")
            os._exit(0)
        elif args[0] == 'code' or args[0].lower() == 'c':
            code(paths, opera)
        else:
            print("Invalid command.\n")
    else:
        print("No arguments received.\n")

def wiki(args):
    args = " ".join(args)
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
        print("Invalid input, no page found matching the query. please check your spellings and try again.\n")
    except requests.exceptions.ConnectionError as e:
        print("No internet connection.\n")


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
    match, percent = extractOne(args, appList)
    if percent >= 80:
        return match

def openWeb(args, opera):
    print("Opening web page...\n")
    if args:
        opera.open_new_tab(args)
    else:
        print("No arguments received.\n")

def code(paths, opera):
    if paths and 'spotify' in paths.keys():
        spotifyopen = False
        for p in psutil.process_iter():
            if p.name() == 'Spotify.exe':
                spotifyopen = True
        if not spotifyopen:
            Popen(paths['spotify'], shell=True)
    if paths and 'vscode' in paths.keys():
        vsopened = False
        for p in psutil.process_iter():
            if p.name() == 'Code.exe':
                vsopened = True
        if not vsopened:
            Popen(paths['vscode'], shell=True, stdout=DEVNULL, stderr=DEVNULL)
    opera.open_new_tab('https://github.com/OniChan-Baka')
    opera.open_new_tab('https://chat.openai.com/')
    


def restart():
    print("Restarting...\n")
    Directory = os.getcwd()
    Directory = Directory.split('\\')
    Directory = Directory[-1]
    if Directory != 'systerm':
        os.chdir('systerm')
        os.system("python ./restart.py")
        os._exit(0)
    elif Directory == 'systerm':
        os.system("python ./restart.py")
        os._exit(0)
    else:
        print("Error: please check your directory")

def clear():
    Directory = os.getcwd()
    Directory = Directory.split('\\')
    Directory = Directory[-1]
    if Directory != 'systerm':
        os.chdir('systerm')
        if os.name == 'posix':
            if 'TERM' in os.environ and os.environ['TERM'] == 'xterm-256color':
                os.system('clear')
            else:
                os.system('clear')
        elif os.name == 'nt':
            os.system('cls')
        else:
            print("Clear command not supported on this platform.")
    elif Directory == 'systerm':
        if os.name == 'posix':
            if 'TERM' in os.environ and os.environ['TERM'] == 'xterm-256color':
                os.system('clear')
            else:
                os.system('clear')
        elif os.name == 'nt':
            os.system('cls')
        else:
            print("Clear command not supported on this platform.")
    else:
        print("Error: please check your directory")


if __name__ == '__main__':
    main()
