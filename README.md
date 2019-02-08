# Sugar, Flower, Fish or Gravel

Welcome to the repository for the [Zooniverse cloud classification project](https://www.zooniverse.org/projects/raspstephan/sugar-flower-fish-or-gravel)

## Installation

We highly recommend using Anaconda to manage your Python packages.

### Create a new conda environent
To start from scratch, create a new conda environment with the required packages by typing
```
conda create -n my-new-environment --file requirements.txt
python setup.py install
```


### From an existing conda environment
If you already have a conda environment and simply want to make sure you have all the necessary packages installed for this repository, do:

```
conda install --file requirements.txt
python setup.py install
```

### Development install
If you want to modify the functions inside `pyclouds` you can do a development install by typing
```
python setup.py develop
```


<!-- ## Deep learning algorithms -->

<!-- This repository comes with some -->




<!-- ## Repository structure -->

<!-- - `image_download`: Scripts to download and rescale the images from NASA Worldview -->
<!-- - `zooniverse_raw`: Raw classification files from Zooniverse. Please add download date -->
<!-- - `pyclouds`: Python module containing common functions for processing and analyzing data -->
<!-- - `examples`: Some example images for the four categories. -->
<!-- - `processed_annotations`: Intermediate classification files after some processing -->
<!-- - `notebooks_SR`: Stephan's Python notebooks -->
<!-- - `analysis`: Hauke's Python notebooks, these two directories should become one or have more descriptive names. -->