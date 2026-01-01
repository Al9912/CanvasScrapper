# This program is created by Al9912.

import os
import requests

class downloadDocuments:
    @staticmethod
    def downloadFiles(item, moduleFolder, module_name, downloaded_files, headers):
        file_url = item
        file_response = requests.get(file_url, headers=headers)

        if file_response.status_code == 200:
            file_data = file_response.json()
            file_name = file_data['display_name']
            file_type = file_data['content-type']
            download_url = file_data['url']

            content = requests.get(download_url, headers=headers)
            file_path = os.path.join(moduleFolder, file_name)
            if os.path.exists(file_path):
                print(f"✔️ File '{file_name}' already exists. Skipping...")
                # Skip this file and go to the next
            else:
                with open(file_path, 'wb') as f:
                    print(f"⬇️ Downloading '{file_name}' from module '{module_name}' ({file_type})")
                    f.write(content.content)

            downloaded_files.append(file_path)
        else:
            print(f"⚠️ Could not access file info for {item['title']}")