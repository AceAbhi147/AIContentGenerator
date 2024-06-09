# AIContentGenerator - README:


## Pre-requisites

### Python libraries
Install all the python libraries using 
``pip install -r requirements.txt``


### Open-AI Access Token
The project using Open-AI access key which should be added in ```image_generator.py``` file to fetch images from Open-AI Dall-E.
Make sure to update it using your key.


### Dependent library for moviepy python library --> ImageMagick
There are some additional libraries that will be required such as ```imagemagick```
After installing it using   
```sudo apt-get install imagemagick``` run the following command:
``cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml``

If you get permission denied error, just add proper permission to the file using chmod

### Service Account setup for Google Drive upload
The project also uploads generated video file to Google Drive, which uses a ``service-account.json`` file that can be configured and downloaded on to the root file of the project.
Simply follow instructions here to configure your own ``service-account.json`` file.
https://youtu.be/tamT_iGoZDQ?si=elyrKhOR-09pDS5x


### Python version
Run the project using python 3.10 or above.
Run the main.py file to start the script


### Changing fonts and color for subtitles
The file ```video_generator``` has a following function:
```
def __create_caption(self, textJSON, framesize, font="Loma-Bold", color='yellow4', highlight_color='yellow',
                         stroke_color='black', stroke_width=1.5):
```
You can change the font used in the subtitles by modifying the ``font`` parameter.
Make sure that the font is available in your system. You can check this using 

```commandline
from moviepy.editor import TextClip

dummy_clip = TextClip('Dummy Text')
available_fonts = dummy_clip.list('font')

for font in available_fonts:
    print(font)
```
You can install new fonts and use that.


You can also change the color of the words and the highlighted word by changing appropriate paramater of the 
``__create_caption`` function.
Just like the above function, you can find the available colors by changing ``font`` to ``color``
in ``dummpy_clip.list('font')``