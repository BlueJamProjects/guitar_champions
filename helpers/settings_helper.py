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







def update_settings(enable_metronome):
    print("Updating settings")

    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)

    settings_data["enable_metronome"] = str(enable_metronome)
    
    with open("settings/gamesettings.json", "w") as file:
        json.dump(settings_data, file, indent=4)
