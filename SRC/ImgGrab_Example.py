import ImgGrab_Grabber

pid = 0 # the pid changes constantly due to more images being uploaded (always try {loop} more than last pid).
lastID = 0 # last id, to be changed from console after finishing updating
updating = False # should only be True if updating current images to newest posts

tags = ['1girl', 'rating:general']

URL = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={tags.join("+")}"

grabber = ImgGrab_Grabber.Grabber(URL, __file__, lastID, 0, updating)

grabber.run(pid)
