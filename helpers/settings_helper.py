"""
This file contains:

- The Settings object that is used for storing the settings in memory

    The functions:
    - get_settings
    - update_enable_metronome
    - update_volume
    - update_microphone_amplitude

"""


import json

class Settings(object):
    """
    A class to store the current settings.

    Attributes:
        volume (int): The volume level, ranging from 0 to 100.
        enable_metronome (bool): Whether the metronome is enabled or not.
        microphone_amplitude (float): The amplitude of the microphone, ranging from 0.0 to 1.0.
    """
    def __init__(self):
        self.volume = 100
        self.enable_metronome = True
        self.microphone_amplitude = 1




def get_settings():
    """
    Retrieves game settings from 'gamesettings.json' and returns them as a Settings object.

    Returns:
        Settings: An object containing the game settings.

    Raises:
        IOError: If the file 'gamesettings.json' cannot be opened or read.
    """


    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)

    current_settings = Settings()

    # Loops through all the keys from the data and assigns their settings value
    # checks each for validity
    for key in settings_data:

        if key == "volume":

            try:
                # If the volume was in the valid range
                if (int(settings_data[key]) < 101) and (int(settings_data[key]) > -1):
                    current_settings.volume = int(settings_data[key])
                else:
                    print("ERROR - stored volume setting was not in valid range")

            # If the stored value was not a string of an int
            except Exception as e:
                print(f"ERROR - could not process volume setting: {e}")


        elif key == "enable_metronome":

            try:
                # If the enable metronome value was one of the valid values
                if (settings_data[key] == False):
                    current_settings.enable_metronome = False
                elif (settings_data[key] == True):
                    current_settings.enable_metronome = True
                else:
                    print("ERROR - stored enable_metronome setting was not valid")

            # If the stored value was not a string of an int
            except Exception as e:
                print(f"ERROR - could not process enable_metronome setting: {e}")

        elif key == "microphone_amplitude":

            try:
                # If the volume was in the valid range
                if (int(settings_data[key]) < 101) and (int(settings_data[key]) > 0):
                    current_settings.microphone_amplitude = int(settings_data[key])
                else:
                    print("ERROR - stored microphone_amplitude setting was not in valid range")

            # If the stored value was not a string of an int
            except Exception as e:
                print(f"ERROR - could not process microphone_amplitude setting: {e}")



    return current_settings




def update_enable_metronome(name, new_enable_metronome):
    """
    Update the stored enable_metronome value in the gamesettings.json file.

    Args:
        name (str): The name of the setting.
        new_enable_metronome (bool): The new value to store for enable_metronome.

    Raises:
        ValueError: If an invalid value is passed for new_enable_metronome.

    """

    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)

    try:
        if new_enable_metronome == True:
            final_enable_metronome = True
        elif new_enable_metronome == False:
            final_enable_metronome = False
        else:
            print("WARNING - invalid value passed for enable_metronome, corrected to True")
            final_enable_metronome = True


        # Updates the value if no errors were thrown
        settings_data["enable_metronome"] = final_enable_metronome

        with open("settings/gamesettings.json", "w") as file:
            json.dump(settings_data, file, indent=4)

    except Exception as e:
        print(f"ERROR updating value for enable_metronome: {e}")
        print("enable_metronome was not updated")
    
   


def update_volume(new_volume):
    """
    Updates the stored volume value in the gamesettings.json file.

    Args:
        new_volume (int): The new volume value to be stored. Should be an integer 
        between 0 and 100, inclusive.

    Raises:
        ValueError: If the provided volume is not within the valid range (0-100).

    Returns:
        None
    """


    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)

    try:
        if (new_volume // 1) <= 100 and (new_volume // 1 ) >= 0:
            final_volume = int(new_volume)
        elif (new_volume // 1) > 100:
            final_volume = 100
        elif (new_volume // 1) < 0:
            final_volume = 0
        else:
            print("WARNING - invalid value passed for volume, corrected to 100")
            final_volume = 100

        # Updates the value if no errors were thrown
        settings_data["volume"] = final_volume

        with open("settings/gamesettings.json", "w") as file:
            json.dump(settings_data, file, indent=4)

    except Exception as e:
        print(f"ERROR updating value for volume: {e}")
        print("volume was not updated")




def update_microphone_amplitude(new_amplitude):
    """
    Update the stored microphone_amplitude value in the gamesettings.json file.

    Parameters:
        new_amplitude (int): The new value for the microphone amplitude. Must be an integer between 0 and 100 (inclusive).

    Raises:
        ValueError: If the provided new_amplitude is not within the valid range.

    Note:
        If the provided new_amplitude is outside the valid range, it will be corrected to the nearest valid value (0 or 100).

    """
    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)
    try:
        if (new_amplitude // 1) <= 100 and (new_amplitude // 1 ) >= 0:
            final_amplitude = int(new_amplitude)
        elif (new_amplitude // 1) > 100:
            final_amplitude = 100
        elif (new_amplitude // 1) < 1:
            final_amplitude = 0
        else:
            print("WARNING - invalid value passed for microphone_amplitude, corrected to 100")
            final_amplitude = 100
        # Updates the value if no errors were thrown
        settings_data["microphone_amplitude"] = final_amplitude
        with open("settings/gamesettings.json", "w") as file:
            json.dump(settings_data, file, indent=4)
    except Exception as e:
        print(f"ERROR updating value for microphone_amplitude: {e}")
        print("microphone_amplitude was not updated")