# Lost Ark Auto Fish

## Instruction
1. Install [Prerequisites](#prerequisites) 
2. Go to fish spot, enter "trade skill" mode
3. [Run](#run) the code
4. Cast one bait. Done.

## Prerequisites
```bash
$ pip install -r requirements.txt
```
or conda
```bash
$ conda env create -f environment.yml
```

## Run
if conda, activate environment first
```bash
$ conda activate fishing
```
run
```bash
$ python fish_macro.py
```

## Customize & TroubleShooting
- Uncomment debug line to save screenshots and more outputs
- Adjust `center` to fit rendering resolution of the game (default 1080p game resolution)
- Adjust `precision` 
- Adjust min & max threshold of Hue, Saturation, lightness. [More](https://docs.opencv.org/4.5.5/da/d97/tutorial_threshold_inRange.html) info
	- Note: In `opencv` API image is generally in `BGR`, but `pillow` reads as `RGB`. 
- Map `keystroke` to other key and sned more keys
- Change other pattern to recognize

## Pseudocode
1. read pattern
2. loop until durability limit
	1. loop until matching or timeout
		1. capture screenshots
		2. preprocess screenshot (corp, thresholding)
		3. match by `cv2.matchTemplate()`
	2. recast if timeout / or pull if success, wait animation, and recast. 

## Acknowledge
- Thanks to [silvernine209](https://github.com/silvernine209/lostark_fishing_macro) for `shell.SendKeys()` API and the images. 
	- The improvement of this script is saving computing power, increasing consistency of directory, reducing redundant of calls, and changing thresholding methods (also fiing minor bug in cv readmode). 
- Thanks to OpenCV [Template Matching](https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html).