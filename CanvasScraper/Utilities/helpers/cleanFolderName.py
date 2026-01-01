# This program is created by Al9912.

class cleanFolderName:
    @staticmethod
    def clean_folder_name(name):
        # Remove or replace characters that are not allowed in folder names
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()