import os
import time
import music
import psutil
import comtypes
import requests
import wikipedia
import webbrowser
from time import sleep
from datetime import timedelta
from json import load, dumps, loads
from subprocess import Popen, DEVNULL
from pycaw.utils import AudioUtilities
from fuzzywuzzy.process import extractOne


def main():
    CommandHistory = []
    Directory = os.getcwd()
    Directory = Directory.split('\\')
    Directory = Directory[-1]
    if Directory != 'systerm':
        os.chdir('systerm')
    summeryLenght = 2
    opera_path = r"C:\\Users\\famal\\AppData\\Local\\Programs\\Opera GX\\opera.exe"
    webbrowser.register('opera', None, webbrowser.BackgroundBrowser(opera_path))
    opera = webbrowser.get('opera')
    with open(r"C:\\Data\\Programming\\Python\\sysTerm\\appPaths.json", "r") as f:
        appsPaths = load(f)
    with open(r"C:\Data\Programming\Python\\sysTerm\\Logs.json", "r") as L:
        Logs = load(L)
    newLogs = {}
    with open(r"C:\\Data\\Programming\\Python\\systerm\\api_key.json", 'r') as key:
        api_key = load(key)['api']
    city_name = 'faisalabad'
    while True:
        argsStr = input('> ')
        CommandHistory.append(argsStr)
        LogW(Logs, newLogs, CommandHistory)
        args = argsStr.split(' ')
        backend(args, appsPaths, opera, summeryLenght, Logs, CommandHistory, city_name, api_key)

def backend(args, paths, opera, summeryLenght, Logs, CommandHistory, city_name, api_key):
    if args[0] != '':
        if args == '':
            pass
        elif args[0].lower() == 'wiki' or args[0].lower() == 'wikipedia' or args[0].lower() == 'w':
            args.pop(0)
            wiki(args, summeryLenght)
        elif args[0].lower() == 'open' or args[0].lower() == 'o':
            args.pop(0)
            openApp(args, paths)
        elif args[0].lower() == 'youtube' or args[0].lower() == 'y':
            args.pop(0)
            openWeb('https://www.youtube.com', opera)
        elif args[0].lower() == 'github' or args[0].lower() == 'g':
            args.pop(0)
            openWeb('https://github.com/OniChan-Baka/', opera)
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
        elif args[0] == 'play' or args[0].lower() == 'mp':
            play(paths)
        elif args[0] == 'pause' or args[0].lower() == 'mpu':
            pause()
        elif args[0] == 'resume' or args[0].lower() == 'mr' or args[0].lower() == 'res':
            resume()
        elif args[0] == 'previous' or args[0].lower() == 'mpr' or args[0].lower() == 'pre' or args[0].lower() == '<':
            previous()
        elif args[0] == 'next' or args[0].lower() == 'mn' or args[0].lower() == '>':
            Next()
        elif args[0] == 'logs' or args[0].lower() == 'l':
            Log(args[1:])
        elif args[0] == 'weather' or args[0].lower == 'temperature' or args[0].lower() == 'temp':
            getWeather(city_name, api_key, args[1:])
        elif args[0] == 'volume' or args[0].lower() == 'v':
            volume(args[1:])
        elif args[0] == 'mode':
            mode(args[1:], paths, opera)
        elif args[0] == 'commitloop': #TODO remove this after development
            for i in range(10):
                commitloop(i)
        elif args[0] == 'commit': #TODO remove this after development
            commit()
        else:
            print("Invalid command.")
    else:
        pass
    
def wiki(args, summeryLenght):
    args = " ".join(args)
    wikipedia.set_lang('en')
    wikipedia.set_rate_limiting(True, min_wait=timedelta(milliseconds=1000))
    print("Getting Info...")
    try:
        print(wikipedia.summary(args, sentences=summeryLenght, auto_suggest=False), "")
    except wikipedia.DisambiguationError as e:
        print(f"There are multiple results for \"{args}\", Here are some suggestions:")
        ops = ''.join(e.options[0::5])
        print(ops)
    except wikipedia.exceptions.PageError as e:
        print("Invalid input, no page found matching the query. please check your spellings and try again.")
    except requests.exceptions.ConnectionError as e:
        print("No internet connection.")

def openApp(args, paths):
    args = " ".join(args)
    pargs = args[0].upper() + args[1:]
    print(f"Opening {pargs}")
    if len(args) > 0:
        match = matchkey(args, paths)
        if match:
            Popen(paths[match], shell=True)
        else:
            print(f"No app found for {args}")

def matchkey(args, paths):
    appList = paths.keys()
    match, percent = extractOne(args, appList)
    if percent >= 80:
        return match

def openWeb(args, opera):
    print("Opening web page...")
    if args:
        opera.open_new_tab(args)
    else:
        print("No arguments received.")

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
    print("Restarting...")
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
def play(paths):
    if paths and 'spotify' in paths.keys():
        sopened = False
        for p in psutil.process_iter():
            if p.name() == 'Spotify.exe':
                sopened = True
        if not sopened:
            Popen(paths['spotify'], shell=True)
            openedyet = False
            while not openedyet:
                for p in psutil.process_iter():
                    if p.name() == 'Spotify.exe':
                        openedyet = True
            music.play()
            
        elif sopened:
            music.play()

def pause():
    print("Paused")
    music.pause()

def resume():
    print("Resumed")
    music.resume()

def previous():
    print("Previous")
    music.previous()

def Next():
    print("Next")
    music.Next()

def LogW(Logs, newLogs, CommandHistory):
    oldLogs = dict(Logs)
    newLogs[str(time.ctime())] = CommandHistory[-1]
    oldLogs.update(newLogs)
    with open(r"C:\Data\Programming\Python\\sysTerm\\Logs.json", "w") as L:
        L.write(dumps(oldLogs, indent=4))

def Log(args):
    if len(args) > 0:
        if args[0] == 'show':
            with open(r"C:\Data\Programming\Python\\sysTerm\\Logs.json", "r") as R:
                logsR = loads(R.read())
                history = list(logsR.values())[-10:]
                n = 0
                for i in history:
                    n += 1
                    print(f"{n}: {i}")
        else:
            print("wrong argument provided!")
    else:
        print('No arguments specified!')
def getWeather(city_name, api_key, args):
    if len(args) > 0:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={args[0]}&appid={api_key}'
        weather_response = requests.get(url)
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            temp = int(weather_data['main']['temp']-273.15)
            print(f'Temperature in {city_name} is: {temp}°C')
        else:
            print('Failed to fetch weather data. Status code:', weather_response.status_code)
    else:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        weather_response = requests.get(url)
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            temp = int(weather_data['main']['temp']-273.15)
            print(f'Temperature in {city_name} is: {temp}°C')
        else:
            print('Failed to fetch weather data. Status code:', weather_response.status_code)

def study():
    print("study")
    music.playcustom("https://open.spotify.com/playlist/0rlvZxefuTfi14ydHLgIxT")

def mode(args, paths, opera):
    if len(args) == 1:
        if args[0] == "code":
            code(paths, opera)
        if args[0] == "study":
            study()
    elif len(args) > 1:
        print("Too many arguments!")
    else:
        print("No arguments provided!")

def commit():
    os.system("git add .")
    os.system("git commit -m \"This is a automated commit\"")
    os.system("git push")
def commitloop(i):
    with open("C:\\Data\\Programming\\Python\\systerm\\requirments.txt", "w") as f:
        f.write(f"""wikipedia
fuzzywuzzy
requests
pygame
json{i}""")
    os.system("git add .")
    os.system("git commit -m \"This is a automated commit\"")
    os.system("git push")

def set_system_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        AudioUtilities.IAudioEndpointVolume._iid_, 
        comtypes.CLSCTX_ALL, 
        None
    )
    volume = interface.QueryInterface(AudioUtilities.IAudioEndpointVolume)
    volume.SetMasterVolumeLevelScalar(volume_level, None)

def volume(args):
    if len(args) == 1:
        if isinstance(args[0], int):
            set_system_volume(args[0])
        elif args[0] == 'up' or "u":
            pass
        elif args[0] == 'down' or "d":
            pass
    elif len(args) > 1:
        print("Too many arguments!")
    elif len(args) < 1:
        print("no arguments provided!")


if __name__ == '__main__':
    main()
