# Automated Bloodstain Segmentation

This is a tool kiey of Bloodstain Spatter Pattern analysis.

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
  
