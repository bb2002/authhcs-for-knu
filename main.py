import selenium
import time
from datetime import datetime
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def makeChrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
    driver.implicitly_wait(time_to_wait=5)
    return driver

def searchSchool(driver, schoolName):
    driver.get(url="https://hcs.eduro.go.kr/")
    driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/ul[1]/li[2]/div/button").click()       # "대학" 버튼을 누른다.
    driver.find_element_by_xpath("//*[@id=\"btnConfirm2\"]").click()                                        # 자가 진단 참여하기를 누른다.
    driver.find_element_by_xpath("//*[@id=\"WriteInfoForm\"]/table/tbody/tr[2]/td/button").click()          # 학교 검색

    school_search_box = driver.find_element_by_xpath("//*[@id=\"schoolName\"]")
    school_search_box.send_keys(schoolName)
    school_search_box.send_keys(Keys.ENTER)
    driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a').click()             # 학교 선택
    driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[2]/input').click()
    time.sleep(1)           # 학교 선택 완료.

def fillFields(driver, name, student_id, password):
    name_box = driver.find_element_by_xpath('//*[@id="user_name_input"]')
    name_box.send_keys(name)

    student_id_box = driver.find_element_by_xpath('//*[@id="user_no_input"]')
    student_id_box.send_keys(student_id)

    driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
    time.sleep(1)

    passwd_box = driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr/td/input')
    passwd_box.send_keys(password)
    passwd_box.send_keys(Keys.ENTER)

    time.sleep(2)

def ansQuestions(driver):
    driver.find_element_by_xpath('//*[@id="container"]/div/section[2]/div[2]/ul/li/a/span[1]').click()
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="survey_q1a1"]').click()
    driver.find_element_by_xpath('//*[@id="survey_q2a1"]').click()
    driver.find_element_by_xpath('//*[@id="survey_q3a1"]').click()
    time.sleep(0.5)

    driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
    time.sleep(1)

with open("config.json", "r") as fconfig:
    students = json.load(fconfig)

    for student in students:
        print("=-= {0} {1} {2} Result =-=".format(student["school"], student["name"], student["student_id"]))
        try:
            driver = makeChrome()
            print(" Make browser:    [OK]")
            
            searchSchool(driver, student["school"])
            print(" Search school:   [OK]")
            fillFields(
                driver, 
                student["name"],
                student["student_id"], 
                student["password"])

            print(" Write fields:    [OK]")
            ansQuestions(driver)        # 답변 완료
            print(" Submit answer:   [OK]")

            screenshotName = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + student["school"] + "_" + student["student_id"] + ".png"
            print(" Save screenshot:   [OK]")

            driver.save_screenshot("./screenshot/" + screenshotName)
            driver.close() 
        except Exception as ex:
            print("Fatal Error!")
            print(ex)

        














