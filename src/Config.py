import os
import shutil

import toml

config_folder = "config"

class Config:
    def __init__(self, path_config: str = None):
        if path_config is None:
            path_config = config_folder
        self.path_config = path_config
        self.read_configuration()

    def read_configuration(self):
        list_conf_files = os.listdir(self.path_config)

        self.configuration = {}
        for file in list_conf_files:
            path_file = os.path.join(self.path_config, file)
            conf = toml.load(path_file)
            print(f"Read {path_file}")
            self.configuration.update(conf)


    def get(self, section, key):
        # Access the key within a section in the TOML configuration
        return self.configuration.get(section, {}).get(key, None)


if __name__ == "__main__":

    print("Initializing Config class...")
    config = Config(config_folder)
        
    print("Files in the directory:")
    print(os.listdir(config_folder))
    api_key = config.get('api', 'key')

    print(f"API Key: {api_key}")

