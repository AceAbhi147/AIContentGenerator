# AIContentGenerator - README:

&nbsp;
&nbsp;
## Description
This is a python script that creates a video by fetching series of images from Open-AI using access token and stitching them together.
Then creates an audio file and subtitles which is then added to the generated video file.
Finally, the script uploads this video to Google drive.

&nbsp;
&nbsp;
## Pre-requisites

&nbsp;
### 1. Doc file for Subtitles
A doc file, containing information for video's audio and prompts for image generation from Open-AI, should be present in the ``resources\jobs``
folder. This file will be used to generate assets folder for this job under ``resources\jobs`` directory. These assets are then used to generate the final video.
Please take a look at the sample file ``The Script.docx`` present and make sure to adhere to the same format.

This doc contains a ``[changeImage]`` after some texts, which is an indicator to the script to transition to the next image.

&nbsp;
### 2. Python libraries
Install all the python libraries using 
``pip install -r requirements.txt``

&nbsp;
### 3. Open-AI Access Token
The project using Open-AI access key which should be added in ```image_generator.py``` file to fetch images from Open-AI Dall-E.
Make sure to update it using your key.

&nbsp;
### 4. Dependent library for moviepy python library --> ImageMagick
There are some additional libraries that will be required such as ```imagemagick```
After installing it using   
```sudo apt-get install imagemagick``` run the following command:
``cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml``

If you get permission denied error, just add proper permission to the file using chmod

&nbsp;
### 5. Service Account setup for Google Drive upload
The project also uploads generated video file to Google Drive, which uses a ``service-account.json`` file that can be configured and downloaded on to the root file of the project.
Simply follow instructions here to configure your own ``service-account.json`` file.
https://youtu.be/tamT_iGoZDQ?si=elyrKhOR-09pDS5x

&nbsp;
### 6. Python version
Run the project using python 3.10 or above.
Run the main.py file to start the script


&nbsp;
## Additional Information:

&nbsp;
### 1. Multiple jobs
This projects supports video creation for multiple job. 
To do that make sure that the name of the doc containing all the relevant information are unique.

&nbsp;
### 2. Using Whisper library
Whisper library is being used in this project to get the timestamp of each word being spoken, which is used for creating 
subtitles. If the subtitles are not aligned it means the timestamp generated are not accurate. We can configure the library model to be more accurate.
This can be done by making changes to the following line:
```
model = WhisperModel("medium")
```
in ``audio_generator.py`` file in ``get_subtitles_with_timestamp`` function.
Just change the parameter from ``medium`` to ``large``.

&nbsp;
### 3. Changing fonts and color for subtitles
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

&nbsp;
## Sample Video:
https://drive.google.com/file/d/1pfhBN7XqCsEqUJf7cfVuAl-iejrrDn_2/view?usp=sharing
https://drive.google.com/file/d/12_ShRXDho98V5xu6dFvCe2Umo7qzfsme/view?usp=sharing
