# CanvasScrapper

CanvasScrapper is a program that pulls data from your Canvas account and saves it locally on your machine. This is useful for people with limited or unreliable internet connections who want offline access to their course content.

---

## How to Use

### 1. Open the Main Script

Navigate to the following file:

```
CanvasScrapper/canvasScrappingMain.py
```

Open this file in your preferred code editor.

---

### 2. Set Your Canvas URL

Go to **line 8** and locate the following variable:

```python
BASE_URL = "https://yourinstitution.instructure.com/api/v1/"
```

Replace the URL with your **school's or organization's Canvas URL**.

Example:

```
https://schoolname.instructure.com/api/v1/
```

---

### 3. Create an Access Token

Next, go to **line 9**, where you will see:

```python
ACCESS_TOKEN = ""
```

You must generate a Canvas access token.

#### Steps to Generate a Token

1. Log in to Canvas.
2. Go to **Account → Settings**.
3. Scroll down until you find **Approved Integrations**.
4. Click **New Access Token**.
5. Fill in the **Purpose** field (this can be any label or name).
6. The **Expiration Date** is optional.
7. Click **Generate Token**.

Once the token is generated:

* Copy the token.
* Paste it into the `ACCESS_TOKEN` variable in the script.
* Store it somewhere safe and **do not share it with anyone**.

---

### 4. Choose the Download Location

Go to **lines 20 and 21** in the script.

On **line 20**, you can specify where files should be downloaded by entering a directory path inside the parentheses.

Example:

```python
DOWNLOAD_PATH = "/home/user/canvas_files"
```

If you want the files to be saved **in the same directory as the program**, then:

* Comment out **line 20**
* Uncomment **line 21**

---

### 5. Run the Program

Save and close the file.

Open a terminal and navigate to the project directory.

Run the program with:

```bash
python3 canvasScrappingMain.py
```

---

The program will begin downloading your Canvas course data to the specified directory.
