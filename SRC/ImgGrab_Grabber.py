
# Created By: Josh Mlaker
# 
# Description: Grabs images from a Booru API with their standard URL scheme
# Dependencies: Pillow, getIndex

import requests
import getIndex
import os
from PIL import Image

class Grabber:
    # Setup variables for scrapping
    # URL: API's URL
    # group: Where to place the image. Suggested: __file__
    # lastID: The latest ID obtained from scrapping, used for ensuring no duplicates
    # oldestID: The last ID obtained from scrapping, used for ensuring no duplicates
    # updating: If True, uses lastID to determine start point. If False, uses oldestID
    def __init__(self, URL, group, lastID, oldestID = None, updating = True):
        self.URL = URL
        self.lastID = lastID
        self.group = group.split("\\")[-1]
        self.oldestID = oldestID
        self.updating = updating
        self.index = getIndex.index

    # Updates the lastID of an ImgGrab file
    # id: The ID to update
    def update(self, id):
        with open("SRC/" + self.group, "r") as f:
            lines = f.read().split(f"lastID = {self.lastID}")
            new_line = 'lastID = {}'.format(id)
            new_file = lines[0] + new_line + lines[-1]

        with open("SRC/" + self.group, "w") as f:
            f.write(lines[0] + new_line + lines[-1])

    # DEPRECATED. SEE NEXT METHOD
    def runOLDMETHOD(self, pid, index = None):
        if index != None:
            self.index = index

        counter = 0
        newestPost = self.updating
        firstPost = True
        if self.updating: pid = 0

        folder = self.group.split("_")[-1][:-3]

        # loop over pid
        for j in range(10):
            # send API REQUEST for specified pid with tags
            response = requests.get(self.URL + "&pid=" + str(pid + j) + "&json=1")
            # if the API accepted the REQUEST:
            if response.status_code == 200:
                if firstPost:
                    print('Newest post: ' + str(response.json()['post'][0]['id']))
                    firstPost = False
                if response.json()['post'][-1]['id'] >= self.oldestID and not self.updating:
                    continue
                # loop over posts
                for post in response.json()['post']:
                    # for updating purposes, once it reaches the newest post, exit the program
                    if post['id'] <= self.lastID and self.updating:
                        print("Next index: " + str(self.index))
                        print("Count: " + str(counter))
                        getIndex.updateIndex(self.index)
                        return self.index
                    # for updating purposes, print out the newest post's ID
                    if newestPost:
                        newestPost = False
                        self.update(post['id'])
                    if post['id'] >= self.oldestID and not self.updating:
                        continue
                    # get the image url
                    imageUrl = post['file_url']
                    if imageUrl.split('.')[-1] != "mp4":
                        # request the image from http
                        image = requests.get(imageUrl)
                        # create and open a file with the standards I have been using (IMG- + index)
                        file = open("F:/Image-Grabber/" + folder + "/IMG-" + str(self.index) + "." + imageUrl.split('.')[-1], 'wb')
                        # write the image to the new file
                        file.write(image.content)
                        # close the file (to save space)
                        file.close()
                        # increment index
                        self.index += 1
                        counter += 1
            # if the loop is over, print the oldest post's id to the console
            if j == 9:
                print("Oldest ID: " + str(response.json()['post'][-1]['id']))

        # print out next index to replace the current in code
        print("Next index: " + str(self.index))
        getIndex.updateIndex(self.index)
        print("Next pid: " + str(pid + 10))
        print("Count: " + str(counter))
        return self.index

    # Run the scrapper with a page index, and specified index for naming
    # pid: page index
    # index: number for naming scheme. Suggested: getIndex()
    def run(self, pid, index = None):
        if index != None:
            self.index = index

        # Counter for number of runs (should be consistent, if not, problems occurred)
        counter = 0
        # Newest post if updating
        newestPost = self.updating
        # Boolean to track if it's the first run for updating purposes
        firstPost = True

        # If updating, always start at first page
        if self.updating: pid = 0

        # File the folder name to place the file (removing ".py")
        folder = self.group.split("_")[-1][:-3]

        # loop over pid
        for j in range(10):
            # send API REQUEST for specified pid with tags
            response = requests.get(self.URL + "&pid=" + str(pid + j) + "&json=1")
            # if the API accepted the REQUEST:
            if response.status_code == 200:
                # If updating, print the newest post's ID
                if firstPost:
                    print('Newest post: ' + str(response.json()['post'][0]['id']))
                    firstPost = False
                # If not updating, and the last post is too old, skip the page
                if response.json()['post'][-1]['id'] >= self.oldestID and not self.updating:
                    continue
                # loop over posts
                for post in response.json()['post']:
                    # for updating purposes, once it reaches the newest post, exit the program
                    if post['id'] <= self.lastID and self.updating:
                        print("Next index: " + str(self.index))
                        print("Count: " + str(counter))
                        getIndex.updateIndex(self.index)
                        return self.index
                    # for updating purposes, print out the newest post's ID
                    if newestPost:
                        newestPost = False
                        self.update(post['id'])
                    if post['id'] >= self.oldestID and not self.updating:
                        continue
                    # get the image url
                    imageUrl = post['file_url']
                    if imageUrl.split('.')[-1] != "mp4":
                        # request the image from http
                        image = requests.get(imageUrl)
                        # create and open a file with the standards I have been using (IMG- + index)
                        file = open("F:\\Personal\\Image-Grabber\\Layover\\TEMP-IMG." + imageUrl.split('.')[-1], 'wb')
                        # write the image to the new file
                        file.write(image.content)
                        # create copy of image (massively reduced size)
                        try:
                            with Image.open(file.name) as image:
                                image = image.convert("RGB") # JPEG standard
                                image.save("F:\\Personal\\Image-Grabber\\" + folder + "\\IMG-" + str(self.index) + "." + "jpg", "jpeg")
                                image.close()
                        except:
                            print("Unable to convert image")
                        # close the file (to save space)
                        file.close()
                        # increment index
                        self.index += 1
                        counter += 1
            # if the loop is over, print the oldest post's id to the console (while not updating)
            if j == 9:
                print("Oldest ID: " + str(response.json()['post'][-1]['id']))

        # print out next index to replace the current in code
        print("Next index: " + str(self.index))
        # update index in global file
        getIndex.updateIndex(self.index, "index")
        # print out next page ID if the limit is reached or not updating
        print("Next pid: " + str(pid + 10))
        # print the number of images obtained (if abnormal, end is reached)
        print("Count: " + str(counter))
        
        return self.index
