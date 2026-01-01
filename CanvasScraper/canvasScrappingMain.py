# This program is created by Al9912.

from Utilities.canvasScrapping import canvasScrapping as CanvasScrapping
from Utilities.helpers.cleanFolderName import cleanFolderName as CleanFolderName
import Utilities.helpers.internetCheck as internetCheck
from titleCard import titleCard as TitleCard
# 🔧 Your school’s Canvas URL and your personal access token
BASE_URL = "https://yourinstution.instructure.com/api/v1/"  # Use the canvas URL that is presented on the web browser but leave "api/v1" alone.
ACCESS_TOKEN = ""  # Token for accessing canvas.
# To get the access token, go to your Canvas account, then go to Settings, select “New Access Token.”
# enter the purpose (the expiration date and time are optional), and finally generate the token.

# Instantiate the class with credentials (class-based API)
CS = CanvasScrapping(ACCESS_TOKEN, BASE_URL)

def main(CourseInfo, selection):
    COURSE_ID = CourseInfo

    # Uncomment and change the path if you want to change the download location.
    filePath = ""  # This is the path where the files will be downloaded.
    # filePath = os.path.dirname(os.path.abspath(__file__)) # Gets the current directory of the script.

    if selection != True:
        if COURSE_ID.get('name') is not None:
            print(f"\n📘 {COURSE_ID.get('name')}")
            print("\nModules:")
            CS.download_all_files_from_modules(COURSE_ID["id"], COURSE_ID.get('course_code'), filePath)
            print("\nAssignments:")
            CS.download_all_files_from_assignments(COURSE_ID["id"], COURSE_ID.get('course_code'), filePath)
            print("\nDiscussions:")
            CS.get_discussions(COURSE_ID["id"], COURSE_ID.get('course_code'), filePath)
            print("\nAssignment Grades:")
            assignmentGrades = CS.get_assignment_grades(COURSE_ID["id"], COURSE_ID.get('course_code'))
            print("\nOverall Grades:")
            overallGrade = CS.get_overall_grade(COURSE_ID["id"])
            print("\nSaving Grades in CSV File")
            fileName = f"{CleanFolderName.clean_folder_name(COURSE_ID.get('course_code'))} Grades.csv"
            CS.save_assignment_grades_to_csv(assignmentGrades, overallGrade, fileName, filePath, COURSE_ID.get('course_code'))
    else:
        for ID in COURSE_ID:
            if ID.get('name') is not None:
                print(f"\n📘 {ID.get('name')}")
                print("\nModules:")
                CS.download_all_files_from_modules(ID["id"], ID.get('course_code'), filePath)
                print("\nAssignments:")
                CS.download_all_files_from_assignments(ID["id"], ID.get('course_code'), filePath)
                print("\nDiscussions:")
                CS.get_discussions(ID["id"], ID.get('course_code'), filePath)
                print("\nAssignment Grades:")
                assignmentGrades = CS.get_assignment_grades(ID["id"], ID.get('course_code'))
                print("\nOverall Grades:")
                overallGrade = CS.get_overall_grade(ID["id"])
                print("\nSaving Grades in CSV File")
                fileName = f"{CleanFolderName.clean_folder_name(ID.get('course_code'))} Grades.csv"
                CS.save_assignment_grades_to_csv(assignmentGrades, overallGrade, fileName, filePath, ID.get('course_code'))
    
    return 0

def selectedClassesOrAllClasses(searchType, selection):
    continueLoop = True
    COURSE_ID = CS.get_courses(searchType)
    match selection:
        # All Classes.
        case True:
            return COURSE_ID
        # Specific Classes.
        case False:
            while continueLoop:
                numberOfClasses = 0
                loop = 0
                print("\n\nWhich of the following clasees do you want to see?:")
                for ID in COURSE_ID:
                    numberOfClasses += 1
                    print(f"{numberOfClasses} : {ID['course_code']}")
                print(f"{numberOfClasses + 1} : Go Back")
                answerSelectCourse = int(input("Answer: "))
                if 1 <= answerSelectCourse <= numberOfClasses:
                    for IDOne in COURSE_ID:
                        loop += 1
                        if answerSelectCourse == loop:
                            continueLoop = False
                            return IDOne
                elif numberOfClasses + 1 == answerSelectCourse:
                    print("Going back to the previous menu...")
                    continueLoop = False
                    return None
                else:
                    print("⚠️ This is not the following choices. Please try again.")
        case _:
            print("⚠️ Error: This is not boolean value. Please try again.")
    # return 0

def seeAllClassesOrSpecificClass():
    continueLoop1 = True
    while continueLoop1:
        answerAllOrSpecific = int(input("\n\nDo you want to check all the classes or an specific class?\n1 = All\n2 = Specific Class\n3 = Go Back\nAnswer: "))
        match answerAllOrSpecific:
            # All Classes.
            case 1:
                continueLoop1 = False
                return True
            # Specific Classes.
            case 2:
                continueLoop1 = False
                return False
            case 3:
                print("Going back to the previous menu...")
                continueLoop1 = False
                return None
            case _:
                print("⚠️ This is not the following choices. Please try again.")

def mainMenu():
    while True:
        try:
            userResponce = input("\nDo you want current or all courses?\n1 = current\n2 = all\n3 = Exit\nAnswer: ")
            number = int(userResponce)
            searchType = ""
            match number:
                # The case one is for only the current classes.
                case 1:
                    searchType = 'active'
                    print(f"SearchType: {searchType}")
                    selection = seeAllClassesOrSpecificClass()
                    if selection is None:
                        continue  # back to main menu
                    chosen = selectedClassesOrAllClasses(searchType, selection)
                    if chosen is None:
                        continue  # back from course picker
                    main(chosen, selection)
                    input("Press enter to continue...")
                    break
                # The case two is for the all classes it was taken and current ones.
                case 2:
                    searchType = 'all'
                    print(f"SearchType: {searchType}")
                    selection = seeAllClassesOrSpecificClass()
                    if selection is None:
                        continue  # back to main menu
                    chosen = selectedClassesOrAllClasses(searchType, selection)
                    if chosen is None:
                        continue  # back from course picker
                    main(chosen, selection)
                    input("Press enter to continue...")
                    break
                case 3:
                    print("Exiting...")
                    break
                case _:
                    print("⚠️ Error: You did not slected any of the following choices. Please try again.")
        except ValueError:
            print("⚠️ Error: Invalid Value. Please try again.")

if internetCheck.check_internet():
    TitleCard.titleCard()
    mainMenu()
else:
    print("❌ No internet connection")
    input("Press enter to continue...")