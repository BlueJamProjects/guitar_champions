import json

def update_settings(enable_metronome):
    print("Updating settings")

    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)

    settings_data["enable_metronome"] = str(enable_metronome)
    
    with open("settings/gamesettings.json", "w") as file:
        json.dump(settings_data, file, indent=4)



def get_settings():
    with open("settings/gamesettings.json", "r") as file:
        settings_data = json.load(file)

    return settings_data