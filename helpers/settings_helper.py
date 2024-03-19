import json

class Settings(object):
    """
    A class to store the current settings
    """
    def __init__(self):
        self.volume = 100
        self.enable_metronome = True




def get_settings():
    """
    Gets the gamesettings.json data and returns it in a Settings object.
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
                    current_settings.volume = settings_data[key]
                else:
                    print("ERROR - stored volume setting was not in valid range")

            # If the stored value was not a string of an int
            except Exception as e:
                print(f"ERROR - could not process volume setting: {e}")




        elif key == "enable_metronome":

            try:
                # If the enable metronome value was one of the valid values
                if (settings_data[key] == "0"):
                    current_settings.enable_metronome = False
                elif (settings_data[key] == "1"):
                    current_settings.enable_metronome = True
                else:
                    print("ERROR - stored enable_metronome setting was not valid")

            # If the stored value was not a string of an int
            except Exception as e:
                print(f"ERROR - could not process enable_metronome setting: {e}")



    return current_settings







def update_enable_metronome(enable_metronome):
    """
    Updates the stored enable_metronome settings value
    Takes one (bool) arg
    """

    # reads the current values of the settings
    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)

    
    # bounds checking and correcting if necessary
    if enable_metronome == True:
        final_enable_metronome = True
    elif enable_metronome == False:
        final_enable_metronome = False
    else:
        print("WARNING - invalid enable_metronome value, corrected to True")
        final_enable_metronome = True

    


    # updates the enable_metronome value to the passed in value
    settings_data["enable_metronome"] = str(int(final_enable_metronome))
    
    # writes the updated settings to the settings file
    with open("settings/gamesettings.json", "w") as file:
        json.dump(settings_data, file, indent=4)



def update_volume(new_volume):
    """
    Updates the stored volume settings value
    Takes one (int) arg <= 100 and > 0
    """

    # reads the current values of the settings
    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)


    # bounds checking and correcting if necessary
    if new_volume > 100:
        print("WARNING - Volume too high, it was corrected to 100")
        final_volume = 100
    elif new_volume < 0:
        print("WARNING - Volume too low, it was correct to 0")
        final_volume = 0
    else:
        final_volume = new_volume

    # updates the volume to the passed in value
    settings_data["volume"] = str(final_volume)
    
    # writes the updated settings to the settings file
    with open("settings/gamesettings.json", "w") as file:
        json.dump(settings_data, file, indent=4)
