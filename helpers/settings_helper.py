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
                    current_settings.volume = int(settings_data[key])
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




def update_enable_metronome(name, new_enable_metronome):
    """
    Updates the stored enable_metronome value in the gamesettings.json file
    Takes in a (name, bool) to store the bool as the enable_metronome value
    """

    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)

    try:
        if new_enable_metronome == True:
            final_enable_metronome = 1
        elif new_enable_metronome == False:
            final_enable_metronome = 0
        else:
            print("WARNING - invalid value passed for enable_metronome, corrected to True")
            final_enable_metronome = 1


        # Updates the value if no errors were thrown
        settings_data["enable_metronome"] = str(final_enable_metronome)

        with open("settings/gamesettings.json", "w") as file:
            json.dump(settings_data, file, indent=4)



    except Exception as e:
        print(f"ERROR updating value for enable_metronome: {e}")
        print("enable_metronome was not updated")
    
   


def update_volume(new_volume):
    """
    Updates the stored volume value in the gamesettings.json file
    Takes in an (name, int) with the int int <= 100 and >= 0 to be stored as the enable_metronome value
    """

    print("Updating volume")

    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)

    try:
        if (new_volume // 1) <= 100 and (new_volume // 1 ) >= 0:
            final_volume = (new_volume // 1)
        elif (new_volume // 1) > 100:
            final_volume = 100
        elif (new_volume // 1) < 0:
            final_volume = 0
        else:
            print("WARNING - invalid value passed for volume, corrected to 100")
            final_volume = 100

        print(final_volume)
        # Updates the value if no errors were thrown
        settings_data["volume"] = str(final_volume)

        with open("settings/gamesettings.json", "w") as file:
            json.dump(settings_data, file, indent=4)



    except Exception as e:
        print(f"ERROR updating value for volume: {e}")
        print("volume was not updated")