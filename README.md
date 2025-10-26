# Visually Detect Security Cameras
This project helped me to understand the proces of detecting security cameras using a model like YOLO.
I didn't dive into the full theory of object detection, I was more interested in how much effort it is to train existing models for custom datasets.  
Turns out that with YOLO this is really simple, most of the time goes into labeling the training set.

# Pre-requisites
This contains a bit of personal preference as well.

* uv
  * https://docs.astral.sh/uv/getting-started/installation/
* make-sense
  * https://github.com/SkalskiP/make-sense
* ultralytics (YOLO)
  * https://docs.ultralytics.com/quickstart/

With the above tools you can setup a specific python environment, labels the images that you have and train the model. 
What I ended up doing was the following:

* uv venv
* source .venv/bin/activate
* uv pip install ultralytics

# Getting & labeling the raw data
Since this was mostly to play around I had some fun in taking pictures and the manually annotating them.  
I used make-sense to annotate the images with bounding boxes (rectangles around the object).  

The make-sense tool made this a breeze, for me it was easier to use than the other packages that are available.  
Since you can run it locally it also allows you to work offline and it supports the yolo format, which is nice.  
The setup is easy as well due to the dockerized setup offered. Basically it boils down to (as explained in their readme):

`docker build -t make-sense -f docker/Dockerfile .`  
`docker run -dit -p 3000:3000 --name=make-sense make-sense`

A couple of things that are good to know:

* Don't use the back button (or swipe) on accident you will loose all your work
* Export regularly if you have a big dataset
* The labels used can in a `.txt` file one per line. Index starts at zero when it is parsed

## Removing exif data
Seems like this can also be one shotted with an LLM. The script can be found in `helper-scripts\stripexifdata.py`.

## Splitting / dividing the data
After reading some tutorials and other online sources it seems to be a good idea that your data set is divided,  
into the following parts:

* Training - used to train the model
* Validation - used to validate model performance during training
* Test - used to confirm the working of the model after training

for this I asked an LLM (gemini) to create a simple script for me which you can find in the directory `helper-scripts\dividedataset.py`.  
The script requires what I call `raw data` which should consist of the images that you used for labeling and the exported labels.

## Resizing the data
Turns out this is not really needed since the model does this on the fly. Since I'm also playing around with some LLMs I decided to also  
have a script to resize images which can be found in `helper-scripts\resizeimages.py`. I've been reading contradicting messages on high resolution  
versus lower resolution images for labeling and training. Something to further dive into if I decide to go deepter into the actual workings of these models.

# Training the model
Somehow I assume a lot of effort in doing this, but with YOLO it turns out that it is a single command, which also applies to using the model after training.  
I used the following, since I'm on an arm based Macbook:

* `yolo predict train data=../datasets/seccam001/dataset.yaml model=yolo11s.pt batch=-1 epochs=300 imgsz=640 device=mps`

The above should eventually finish and yield the right files in the output directory, including what is called the weights, which is what you can export or use to find the objects on which you trained it on new images.

# Using the model
Using the custom trained model to find objects is just as easy:

* `yolo predict model=runs/detect/train2/weights/best.pt source=../datasets/seccam001/images/test/ imgsz=640`

# Resources
* https://learnopencv.com/custom-object-detection-training-using-yolov5/#Preparing-the-Dataset
* https://github.com/ultralytics/yolov5
* https://docs.ultralytics.com/modes/val/#arguments-for-yolo-model-validation
* https://medium.com/data-science/chess-rolls-or-basketball-lets-create-a-custom-object-detection-model-ef53028eac7d
* https://docs.ultralytics.com/tasks/detect/
* https://docs.ultralytics.com/modes/train/#train-settings