# This program is created by Al9912.

import requests
import os
import json
import csv
from bs4 import BeautifulSoup

import Utilities.helpers.Pagination as Pagination
import Utilities.helpers.rewriteDate as rewriteDate
from Utilities.helpers.cleanFolderName import cleanFolderName as CleanFolderName
from Utilities.analyzingContent.discussion import discussion as Discussion
from Utilities.analyzingContent.page import page as Page
from Utilities.analyzingContent.downloadDocuments import downloadDocuments as DownloadDocuments
from Utilities.analyzingContent.savingURL import savingURL as SavingURL

class canvasScrapping:
    def __init__(self, ACCESS_TOKEN, BASE_URL):
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.BASE_URL = BASE_URL
    
    def headerFunc(self):
        return {"Authorization": f"Bearer {self.ACCESS_TOKEN}"}

    # 🎓 Get your list of courses
    def get_courses(self, enrollment_state):
        url = f"{self.BASE_URL}/courses"
        params ={}

        match enrollment_state:
            case "active":
                params = {
                    "enrollment_state": "active",
                    "per_page": 100  # Optional, to get more results at once
                }
            case "all":
                params = {
                    "enrollment_state": "all",
                    "per_page": 100  # Optional, to get more results at once
                }
        # active	    Courses you're currently enrolled in
        # invited	    Courses you've been invited to but haven't accepted
        # completed	    Courses you've completed
        # inactive	    Courses where your enrollment is inactive
        # all	        All of the above

        response = requests.get(url, headers=self.headerFunc(), params=params)

        if response.status_code == 200:
            courses = response.json()
            print("\n\n📚 Your Courses:")
            for course in courses:
                print(f"- {course.get('course_code', 'No name')} (ID: {course['id']})")
            return courses
        else:
            print(f"❌ Failed to get courses. Status code: {response.status_code}")
            print(response.text)

    def download_all_files_from_modules(self, COURSE_ID, COURSE_NAME, filePathUser):
        module_url = f"{self.BASE_URL}/courses/{COURSE_ID}/modules"
        course_folder = ""
        
        while module_url:
            response = requests.get(module_url, headers=self.headerFunc())

            if response.status_code != 200:
                print("❌ Failed to fetch modules.")
                return []

            downloaded_files = []
            modules = response.json()
            course_folder = f"{filePathUser}/{COURSE_NAME}/modules"

            # This is looking each module.
            for module in modules:
                module_name = module['name']
                module_id = module['id']
                items_url = f"{self.BASE_URL}/courses/{COURSE_ID}/modules/{module_id}/items"

                while items_url:
                    items_response = requests.get(items_url, headers=self.headerFunc())
                    moduleFolder = f"{course_folder}/{CleanFolderName.clean_folder_name(module['name'])}"
                    os.makedirs(moduleFolder, exist_ok=True)

                    if items_response.status_code != 200:
                        print(f"⚠️ Could not get items for module {module_name}")
                        continue
                    
                    # Looking for files inside of the module.
                    items = items_response.json()
                    for item in items:
                        match item['type']:
                            # This part will download the pages that label as "File".
                            case "File":
                                DownloadDocuments.downloadFiles(item['url'], moduleFolder, module_name, downloaded_files, headers=self.headerFunc())
                            
                            # This will write down the context of the pages in as text files.
                            case "Page":
                                Page.Page(item['page_url'], self.BASE_URL, COURSE_ID, self.headerFunc(), module_name, moduleFolder)
                            
                            # This will write down the context of the discussion as text files.
                            case "Discussion":
                                discussionContentID = item["content_id"]
                                discussionURL = f"{self.BASE_URL}/courses/{COURSE_ID}/discussion_topics/{discussionContentID}"
                                discussionURL_response = requests.get(discussionURL, headers=self.headerFunc())
                                if discussionURL_response.status_code != 200:
                                    print(f"Page not found on the page: {item["page_url"]}")
                                    continue
                                discussionURLContent = discussionURL_response.json()
                                Discussion.discussion(discussionURLContent, moduleFolder)
                            
                            # This will write down the external URL.
                            case "ExternalUrl":
                                SavingURL.savingURL(moduleFolder, item, module_name)
                                                            
                            # This will download the files when is label as "Assigments".
                            case "Assignment":
                                assigmentContentID = item["content_id"]
                                assigmentURL = f"{self.BASE_URL}/courses/{COURSE_ID}/assignments/{assigmentContentID}"
                                assigmentURL_response = requests.get(assigmentURL, headers=self.headerFunc())
                                assigmentURLContent = assigmentURL_response.json()
                                assigmentFolder = f"{moduleFolder}/{CleanFolderName.clean_folder_name(assigmentURLContent["name"])}"
                                os.makedirs(assigmentFolder, exist_ok=True)
                                # if assigmentURLContent["description"] != "description":
                                try:
                                    soup = BeautifulSoup(assigmentURLContent["description"], "html.parser")
                                    files = []
                                    for a in soup.find_all("a", class_="instructure_file_link"):
                                        filename = a.get_text(strip=True)
                                        api_endpoint = a.get("data-api-endpoint")  # safer way
                                        files.append({
                                            "name": filename,
                                            "api_endpoint": api_endpoint
                                        })
                                    for file in files:
                                        DownloadDocuments.downloadFiles(file["api_endpoint"], assigmentFolder, module_name, downloaded_files, headers=self.headerFunc())
                                except TypeError:
                                    print(f"⚠️ The following item is currently empty:\n⚠️ Item: {item["title"]} | Module: {module_name}")
                                    continue
                    # Handle pagination
                    items_url = Pagination.pagination(items_response.headers.get("Link", ""))
            # Handle pagination
            module_url = Pagination.pagination(response.headers.get("Link", ""))
        
        print(f"The files will be saved at {course_folder}")

        return downloaded_files

    def download_all_files_from_assignments(self, COURSE_ID, COURSE_NAME, filePathUser):
        assignments_url = f"{self.BASE_URL}/courses/{COURSE_ID}/assignments"
        course_folder = f"{filePathUser}/{COURSE_NAME}/Assignments"
        
        while assignments_url:
            response = requests.get(assignments_url, headers=self.headerFunc())
            
            if response.status_code != 200:
                print(f"❌ Could not get assignments for {COURSE_NAME}")
                return
            
            assignments = response.json()
            for assignmentContent in assignments:
                assigmentFolder = f"{course_folder}/{CleanFolderName.clean_folder_name(assignmentContent["name"])}"
                os.makedirs(assigmentFolder, exist_ok=True)
                try:
                    soup = BeautifulSoup(assignmentContent["description"], "html.parser")
                    files = []
                    for a in soup.find_all("a", class_="instructure_file_link"):
                        filename = a.get_text(strip=True)
                        api_endpoint = a.get("data-api-endpoint")  # safer way
                        files.append({
                            "name": filename,
                            "api_endpoint": api_endpoint
                        })
                    for file in files:
                        documentURL = file["api_endpoint"]
                        # print(f"Files URL: {documentURL}")
                        documentURL_response = requests.get(documentURL, headers=self.headerFunc())
                        if documentURL_response.status_code == 200:
                            documentURLContent = documentURL_response.json()
                            file_name = documentURLContent['display_name']
                            file_type = documentURLContent['content-type']
                            download_url = documentURLContent['url']

                            content = requests.get(download_url, headers=self.headerFunc())
                            file_path = os.path.join(assigmentFolder, file_name)
                            if os.path.exists(file_path):
                                print(f"✔️ File '{file_name}' already exists. Skipping...")
                                continue  # Skip this file and go to the next
                            else:
                                with open(file_path, 'wb') as f:
                                    print(f"⬇️ Downloading '{file_name}' from module '{CleanFolderName.clean_folder_name(assignmentContent["name"])}' ({file_type})")
                                    f.write(content.content)
                        else:
                            print(f"⚠️ Could not access file info for {CleanFolderName.clean_folder_name(assignmentContent["name"])}")
                except TypeError:
                    print(f"⚠️ The following item is currently empty:\n⚠️Module: {CleanFolderName.clean_folder_name(assignmentContent["name"])}")
                    continue
            assignments_url = Pagination.pagination(response.headers.get("Link", ""))

    def get_discussions(self, COURSE_ID, COURSE_NAME, filePathUser):
        discussionURL = f"{self.BASE_URL}/courses/{COURSE_ID}/discussion_topics"
        discussions_folder = f"{filePathUser}/{COURSE_NAME}/Discussions"
        os.makedirs(discussions_folder, exist_ok=True)
        discussionURL_response = requests.get(discussionURL, headers=self.headerFunc())
        if discussionURL_response.status_code != 200:
            print(f"Page not found on the page: {discussionURL}")
            return []
        discussionURLContent = discussionURL_response.json()
        try:
            for discussionContent in discussionURLContent:
                Discussion.discussion(discussionContent, discussions_folder)
        except TypeError:
            print(f"⚠️ The following item is currently empty:\n⚠️ Module: {discussionContent["title"]}")

    def get_assignment_grades(self, COURSE_ID, COURSE_NAME):
        assignments_url = f"{self.BASE_URL}/courses/{COURSE_ID}/assignments?include[]=submission"
        assignments_grades = {}
        
        while assignments_url:
            response = requests.get(assignments_url, headers=self.headerFunc())
            tempGrades = {}

            if response.status_code != 200:
                print(f"❌ Could not get assignments for {COURSE_NAME}")
                return

            assignments = response.json()
            for assignment in assignments:
                name = assignment.get("name", "Unnamed Assignment")
                points = assignment.get("points_possible", "N/A")
                submission = assignment.get("submission")

                if submission:
                    score = submission.get("score", "Not graded")
                    graded = rewriteDate.rewriteDate(submission.get("graded_at"), "Not Graded")
                    submitted = rewriteDate.rewriteDate(submission.get("submitted_at"), "No Date")
                    totalGrade = 0
                    if not isinstance(score, float):
                        totalGrade = 0
                    else:
                        if points == 0:
                            totalGrade = 0
                        else:
                            totalGrade = (score / points) * 100
                    print(f"📄 {name} | Score: {score}/{points} | Total Grade: {round(totalGrade, 2)}% | Graded: {graded} | Submitted: {submitted}")
                    tempGrades[name] = {
                        'score' : score,
                        'points' : points,
                        'grade' : totalGrade,
                        'date' : graded,
                        'submitted' : submitted
                    }
                else:
                    print(f"📄 {name} | Score: Not submitted or not graded yet.")
            assignments_grades.update(tempGrades)
            assignments_url = Pagination.pagination(response.headers.get("Link", ""))
        return assignments_grades

    def get_overall_grade(self, course_id):
        url = f"{self.BASE_URL}/courses/{course_id}/enrollments"
        response = requests.get(url, headers=self.headerFunc())

        if response.status_code == 200:
            enrollments = response.json()
            found_grade = False  # Track if we find a grade
            for enroll in enrollments:
                if enroll.get("type") == "StudentEnrollment":
                    grade = enroll.get("grades", {}).get("current_score")
                    if grade is not None:
                        print(f"✅ Your grade: {grade}%")
                        found_grade = True
                        return grade
            if not found_grade:
                print("⚠️ No grade available for this course.")
        else:
            print("❌ Error:", response.status_code)
            print(json.dumps(response.json(), indent=4))
            return 0

    def save_assignment_grades_to_csv(self, assignments_grades, finalGrade, filename, filePathUser, COURSE_NAME):
        clean_name = CleanFolderName.clean_folder_name(COURSE_NAME)
        file_path = f"{filePathUser}/{clean_name}/Grades/{filename}"
        print(f"The CSV file will be saved at {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode="w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Assignment Name", "Grade", "Date Graded", "Date Submitted"])  # header
            for assignment_name, details in assignments_grades.items():
                grade = details['grade']
                date = details['date']
                submitted = details['submitted']
                writer.writerow([assignment_name, grade, date, submitted])
            writer.writerow(["Total", finalGrade])
        print(f"✅ Assignment grades saved to {filename}")