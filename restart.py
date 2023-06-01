from os import system
from os import getcwd
from os import chdir

Directory = getcwd()
Directory = Directory.split('\\')
Directory = Directory[-1]
if Directory != 'sysTerm':
    chdir('sysTerm')
    system("python ./main.py")
elif Directory == 'sysTerm':
    system("python ./main.py")
else:
    print("Error: please check you directory")

exit()