from ctypes import cast, POINTER
from comtypes import COMError, CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume


def get_default_audio_interface():
    devices = AudioUtilities.GetSpeakers()
    try:
        interfaces = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interfaces, POINTER(IAudioEndpointVolume))
    except COMError:
        print("Error: Failed to activate IAudioEndpointVolume interface.")
        return None

def get_simple_audio_interface():
    devices = AudioUtilities.GetSpeakers()
    try:
        interfaces = devices.Activate(ISimpleAudioVolume._iid_, CLSCTX_ALL, None)
        return cast(interfaces, POINTER(ISimpleAudioVolume))
    except COMError:
        interfaces = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interfaces, POINTER(IAudioEndpointVolume))

def set_volume(args):
    volume = get_default_audio_interface()
    if volume:
        if isinstance(args, int) or isinstance(args, float):
            volume.SetMasterVolumeLevel(args, None)  # -65 to 0
        else:
            print("Wrong arguments provided!")

def mute():
    volume = get_simple_audio_interface()
    if volume:
        volume.SetMute(True, None)

def unmute():
    volume = get_simple_audio_interface()
    if volume:
        volume.SetMute(False, None)

def current_volume():
    volume = get_default_audio_interface()
    if volume:
        current_volume = volume.GetMasterVolumeLevel()
        print(f"Current Volume is: {round(((current_volume + 65) * (100 - 0) / (0 - (-65))) + 0)}")