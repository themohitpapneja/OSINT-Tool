from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request as urllib
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import logging as logger
import sys
class Instagram:
    def __init__(self):
        self.vars()
        
    def vars(self):
        self.username = input("Enter Login Username/Email_ID: ")
        self.password = input("Enter Valid Password: ")
        self.OtherUserId = input("Enter User_ID To Scrape: ")
        if len(self.username)==0:
            logger.error("Enter Username/Email_ID")
            return
        if len(self.password)==0:
            logger.error("Enter Valid Password")
            return
        if len(self.OtherUserId)==0:
            logger.error("Enter User_ID To Scrape")
            return
        self.postsUrls = []
        self.images = []
        self.videos = []
        self.followers = []
        self.following = []
        self.execute()
    
    def execute(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            self.driver = webdriver.Chrome('./chromedriver' , options=chrome_options)
            self.driver.get("https://www.instagram.com/")
            sleep(4)
            self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.username)
            self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.password)
            self.driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
            sleep(10)
            self.driver.find_element_by_xpath("//button[text()='Not Now']").click()
            sleep(5)
        except:
            logger.error("Username/Email_ID or Password is Invalid")
            self.driver.close()
            return
        self.driver.find_element_by_xpath("//button[text()='Not Now']").click()
        sleep(5)
        self.driver.get("https://www.instagram.com/"+self.OtherUserId)
        sleep(4)
        profile_detail = self.driver.find_element_by_xpath("//ul[@class='k9GMp ']")
        print(profile_detail.text)
        sleep(4)
        self.driver.find_element_by_partial_link_text("follower").click()
        sleep(5)
        print ("\nFollower Username's --------------\n")
        xpath = "/html/body/div[4]/div/div"
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        follow= self.driver.find_elements_by_xpath("//div[@class='PZuss']")
        self.get_number = 0
        while True:
            count = self.get_number
            self.rows = self.driver.find_elements_by_xpath("//div[@class='PZuss']//li")
            self.driver.execute_script("arguments[0].scrollIntoView();", self.rows[-1])  
            self.get_number = len(self.rows)
            self.followers_temp = [e.text for e in self.rows]  
            sleep(3)
            if self.get_number == count:
                break
        for i in self.followers_temp:
            username, sep, name = i.partition('\n')
            self.followers.append(username)
        print (self.followers)
        print("\nFollowing Username's ----------------\n")
        self.driver.get("https://www.instagram.com/"+self.OtherUserId)
        self.driver.find_element_by_partial_link_text("following").click()
        sleep(5)
        xpath = "/html/body/div[4]/div/div"
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        follow= self.driver.find_elements_by_xpath("//div[@class='_1XyCr']")
        self.get_number_2 = 0
        while True:
            count = self.get_number_2
            self.rows_2 = self.driver.find_elements_by_xpath("//div[@class='_1XyCr']//li")
            self.driver.execute_script("arguments[0].scrollIntoView();", self.rows_2[-1])
            self.get_number_2 = len(self.rows_2)
            self.following_temp = [e.text for e in self.rows_2]  
            sleep(3)
            if self.get_number_2 == count:
                break
        for i in self.following_temp:
            username, sep, name = i.partition('\n')
            self.following.append(username)
        print (self.following)
        self.driver.get("https://www.instagram.com/"+self.OtherUserId)
        print("\nScrolling..............")
        while True:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            path = self.driver.find_elements_by_xpath("//*[@class='v1Nh3 kIKUG  _bz0w']//a")
            print("\nRetriving posts url .......")  
            for p in path:
                url = p.get_attribute("href")
                if url not in self.postsUrls:
                    self.postsUrls.append(url)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
        print("Total posts found = " + str(len(self.postsUrls)))
        for url in self.postsUrls:
            self.driver.execute_script("window.open('"+url+"', '_self')")
            self.driver.implicitly_wait(3)
            post_details = []
            try:
                likes = self.driver.find_element_by_xpath("//button[@class='sqdOP yWX7d     _8A5w5    ']").text
            except:
                likes = views = self.driver.find_element_by_xpath("//div[@class='HbPOm _9Ytll']").text
                pass
            age = self.driver.find_element_by_xpath("//div[@class='k_Q0X NnvRN']").text
            xpath_comment = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]'
            comment = self.driver.find_element_by_xpath(xpath_comment).text
            post_details.append({'link': url,'likes/views': likes,'age': age, 'comment': comment})
            sleep(10)
            print("\n")
            print (post_details)
            imagesXpath = self.driver.find_elements_by_xpath("//img[@class='FFVAD']")
            for x in imagesXpath:
                img = x.get_attribute("srcset")
                img = img.split(",")
                img = img[-1][:-6]
                if img not in self.images and img is not None:
                    self.images.append(img)
                    break
            videosXpath = self.driver.find_elements_by_xpath("//video[@class='tWeCl']")
            for v in videosXpath:
                self.images = self.images[:-1]
                video = v.get_attribute("src")
                if video is not self.videos and video is not None:
                    self.videos.append(video)
                    break
    
        print("\nTotal Images found = "  + str(len(self.images)))
        print("\nTotal Videos found = " + str(len(self.videos)))
        url = self.driver.current_url
        userName = url.split("/")
        userName = userName[-2]
        print ('\nFile saving into curent Directory.........')
        imgLen = len(self.images)
        for  i in range(imgLen):
            fileName = self.OtherUserId + userName + str(i)+".jpeg"
            urllib.urlretrieve(self.images[i],fileName)
            print("\nSaving image = "+str(fileName))
        vidLen = len(self.videos)
        if vidLen>=1:
            for i in range(vidLen):
                fileName_2= self.OtherUserId + userName + str(i)+".mp4"
                urllib.urlretrieve(self.videos[i],fileName_2)
                print("\nSaving video = "+str(fileName_2))
        print("\n Execution Completed---------------------")
        self.driver.close()
        
        

Instagram()
