# Automated Bloodstain Segmentation

This is a tool kit for Automatic Bloodstain Spatter Pattern analysis.

It provides automatic dectection and segmentation of stains then various stain and pattern metrics are computed.

Includes a table view and annotated image view.

# To Run

Depends on python3, opencv, matplotlib, numpy, pyqt4, progressbar, scipy

### UI Tool

<code> python app.py </code>

### Command line interface
Analyse on image 

<code> python stain_segmentation.py -f [file from base] -F [full file path] -o [output path] -b [True | False] -s [scale] </code>
 
 see --help for details
  
### Batch Processing
Analyse a folder of images

<code> python batch_processing.py -F [path to folder] -o [output folder] -s [scale]

see --help for details

# CNN Pattern Classifcation
Included in this repo there is an implementation for a converlotional neural network that classifies between Cast off, expirated and impact patterns.

It uses transfer learning with ResNet using Pytorch. The code is basically the transfer learning tutorial from pytorch see here( https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html) for more details.

It depends on pytorch and has been set up with GPU enabled.

To run it first change the path of the dataset then to train use

<code> python transfer_resnet.py </code>

to evaluate use 

<code> python transfer_resnet.py --model [path to your model here] </code>

This requires the image to be cropped to 1000-1000 around the highest density of stains. Code to automate this is in the branch "cropping-at-highest-density" inside this repo.

  
#### Contact

For more information see the report attached to this repo or email me at clairelouisebarnaby@gmail.com

For further work on this repo see https://docs.google.com/document/d/1_ieyeSxFw5pi7pMLjonNRQM7eUtoN1-qwqkRn5WOLdY/edit?usp=sharing