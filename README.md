# CanvasScrapper

This program will pull all the data on you canvas and save it on your machine locally. Perfect for people whose internet connection is limited.

How to use instructions:

1) Go to the file canvasScrappingMain.py inside the folder CanvasScrapper
2) Once the file is open, go to line 8 where it says BASE_URL = "https://yourinstution.instructure.com/api/v1/".
3) Then you need to change the URL to your company's or school's Canvas URL.
4) Once you finish the URL, go to line 9. Which is the name "ACCESS_TOKEN"; you can get the Access Token by going to the:
  a) Account -> Settings.
  b) Then scroll down until you find "Approved Integrations".
  c) Click "New Access Token."
  d) Fill the purpose box (This can be used as a name or label). Expiration date is optional.
  e) Finally, click "Generate Token". Once genarate please save the token in a safe place and don't share to anyone.
5) Then go to lines 20 and 21. On line 20, you can decide where your files will be downloaded (inside the parentheses). If you want to save the files in the same place as this program, you need to comment out line 20 and uncomment line 21.
6) Then save and close the file and run the program in the terminal. Make sure that you are in the directory of the program and run "python3 canvasScrappingMain.py."
