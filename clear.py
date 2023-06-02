from os import system
from os import getcwd
from os import chdir

Directory = getcwd()
Directory = Directory.split('\\')
Directory = Directory[-1]
if Directory != 'systerm':
    chdir('systerm')
    system("cls")
    system("clear")
    system("python ./main.py")
elif Directory == 'systerm':
    system("cls")
    system("clear")
    system("python ./main.py")
else:
    print("Error: please check you directory")
exit()