# This program is created by Al9912.

import os
from Utilities.helpers.cleanFolderName import cleanFolderName as CleanFolderName

class savingURL:
    @staticmethod
    def savingURL(moduleFolder, item, module_name):
        fileName = f"{CleanFolderName.clean_folder_name(item["title"])}.txt"
        filePath = os.path.join(moduleFolder, fileName)
        if os.path.exists(filePath):
            print(f"✔️ File '{fileName}' already exists. Skipping...")
        else:
            with open(filePath, 'w') as f:
                print(f"⬇️ Saving as file '{fileName}' from module '{module_name}'")
                f.write(f"Title: {item["title"]}\nLink: {item["external_url"]}")
                f.close()