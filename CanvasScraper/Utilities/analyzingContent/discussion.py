# This program is created by Al9912.

from bs4 import BeautifulSoup
import os

class discussion:
    @staticmethod
    def discussion(discussionContent, discussions_folder):
        HTMLBody = discussionContent["message"]
        soup = BeautifulSoup(HTMLBody, "html.parser")
        cleanText = soup.get_text(separator="\n", strip=True)
        fileName = f"{discussionContent["title"]}.txt"
        filePath = os.path.join(discussions_folder, fileName)
        if os.path.exists(filePath):
            print(f"✔️ File '{fileName}' already exists. Skipping...")
        else:
            with open(filePath, 'w') as f:
                print(f"⬇️ Saving as file '{fileName}' from module '{discussionContent["title"]}'")
                f.write(f"Title: {discussionContent["title"]}\n\nBody:\n{cleanText}")
                f.close()