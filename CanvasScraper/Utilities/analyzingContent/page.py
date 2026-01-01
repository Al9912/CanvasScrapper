# This program is created by Al9912.

import os
import requests
from bs4 import BeautifulSoup
from Utilities.helpers.cleanFolderName import cleanFolderName as CleanFolderName

class page:
    @staticmethod
    def Page(item, BASE_URL, COURSE_ID, headers, module_name, moduleFolder):
        PageUrlName = item
        PageURL = f"{BASE_URL}/courses/{COURSE_ID}/pages/{PageUrlName}"
        PageURL_response = requests.get(PageURL, headers=headers)
        if PageURL_response.status_code != 200:
            print(f"Page not found on the page: {PageUrlName}")
        PageURLContent = PageURL_response.json()
        # print(f"\n\nPage:\n{json.dumps(PageURLContent, indent=4)}")
        # input("Press enter to continue...")

        HTMLBody = PageURLContent["body"]
        soup = BeautifulSoup(HTMLBody, "html.parser")
        cleanText = soup.get_text(separator="\n", strip=True)
        # print(f"Title: {PageURLContent["title"]}")
        # print(f"Body:\n{cleanText}")
        # input("Press enter to continue...")
        # print("\n")
        fileName = f"{CleanFolderName.clean_folder_name(PageUrlName)}.txt"
        filePath = os.path.join(moduleFolder, fileName)
        if os.path.exists(filePath):
            print(f"✔️ File '{fileName}' already exists. Skipping...")
        else:
            with open(filePath, 'w') as f:
                print(f"⬇️ Saving as file '{fileName}' from module '{module_name}'")
                f.write(f"Title: {PageURLContent["title"]}\n\nBody:\n{cleanText}")
                f.close()