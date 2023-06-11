import wikipedia
import webbrowser
import requests
from json import load
from datetime import timedelta
from fuzzywuzzy.process import extractOne
from subprocess import Popen
import os
from pygame import mixer
import pygame.mixer_music as mixer_music
import pygame.constants as constants


def main():
    Directory = os.getcwd()
    Directory = Directory.split('\\')
    Directory = Directory[-1]
    if Directory != 'systerm':
        os.chdir('systerm')
    mixer.init()
    songsDir = "Songs"
    songNum = 0
    songsList = os.listdir(songsDir)
    songsList.sort()
    opera_path = r"C:\\Users\\famal\\AppData\\Local\\Programs\\Opera GX\\opera.exe"
    webbrowser.register('opera', None, webbrowser.BackgroundBrowser(opera_path))
    opera = webbrowser.get('opera')
    with open(r"C:\\Data\\Programming\\Python\\sysTerm\\appPaths.json", "r") as f:
        appsPaths = load(f)
    while True:
        args = input('> ')
        print(' ')
        args = args.split(' ')
        backend(args, appsPaths, opera, songsDir, songsList, songNum)

def backend(args, paths, opera, songsDir, songsList, songNum):
    if args[0] != '':
        if args[0] == 'exit' or args[0].lower() == 'e':
            print("Exiting...")
            mixer.quit()
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
        elif args[0].lower() == 'play' or args[0].lower() == 'p':
            args.pop(0)
            songNum = play(args, songsDir, songsList, songNum)
            mixer_music.set_endevent(constants.USEREVENT)
        elif args[0].lower() == 'next' or args[0].lower() == '>':
            args.pop(0)
            songNum = nextSong(args, songsDir, songsList, songNum)
            mixer_music.set_endevent(constants.USEREVENT)
        elif args[0].lower() == 'previous' or args[0].lower() == '<':
            args.pop(0)
            songNum = previousSong(args, songsDir, songsList, songNum)
            mixer_music.set_endevent(constants.USEREVENT)
        elif args[0].lower() == 'pause' or args[0].lower() == 'pus':
            args.pop(0)
            pauseSong()
        elif args[0].lower() == 'resume' or args[0].lower() == 'res':
            args.pop(0)
            resumeSong()
        elif args[0].lower() == 'stop':
            args.pop(0)
            stopSong()
        elif args[0].lower() == 'restart' or args[0].lower() == 'r':
            restart()
        elif args[0].lower() == 'clear' or args[0].lower() == 'cls':
            clear()

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
    match, percent = extractOne(args, appList) # type: ignore
    if percent >= 80:
        return match

def openWeb(args, opera):
    print("Opening web page...\n")
    if args:
        opera.open_new_tab(args)
    else:
        print("No arguments received.\n")

def play(args, songsDir, songsList, songNum):
    args = " ".join(args)
    print(f"Playing {args}\n")
    if len(args) > 0:
        match, _ = extractOne(args, songsList) # type: ignore
        if match:
            mixer_music.load(f"{songsDir}/{match}")
            mixer_music.play()
            return songNum
        else:
            print("Wrong argument!")
    else:
        print(f"{songsDir}/{songsList[songNum]}")
        mixer_music.load(f"{songsDir}/{songsList[songNum]}")
        mixer_music.play()
        return songNum

def nextSong(args, songsDir, songsList, songNum):
    songNum += 1
    if songNum >= len(songsList):
        songNum = 0
    play(args, songsDir, songsList, songNum)
    return songNum

def previousSong(args, songsDir, songsList, songNum):
    songNum -= 1
    if songNum < 0:
        songNum = len(songsList) - 1
    play(args, songsDir, songsList, songNum)
    return songNum

def pauseSong():
    mixer_music.pause()

def resumeSong():
    mixer_music.unpause()

def stopSong():
    mixer_music.stop()

def restart():
    print("Restarting...\n")
    Directory = os.getcwd()
    Directory = Directory.split('\\')
    Directory = Directory[-1]
    if Directory != 'systerm':
        mixer.quit()
        os.chdir('systerm')
        os.system("python ./restart.py")
    elif Directory == 'systerm':
        mixer.quit()
        os.system("python ./restart.py")
    else:
        print("Error: please check your directory")
    exit()

def clear():
    Directory = os.getcwd()
    Directory = Directory.split('\\')
    Directory = Directory[-1]
    if Directory != 'systerm':
        os.chdir('systerm')
        os.system('python clear.py')
    elif Directory == 'systerm':
        os.system('python clear.py')
    else:
        print("Error: please check your directory")
    exit()


if __name__ == '__main__':
    main()
