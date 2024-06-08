# AIContentGenerator

Install all the python libraries using 
``pip install -r requirements.txt``

The project using Open-AI access key which should be added in ```image_generator.py``` file to fetch images from Open-AI Dall-E.
Make sure to update it using your key.

There are some additional libraries that will be required such as ```imagemagick```
After installing it using   
```sudo apt-get install imagemagick``` run the following command:
``cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml``

If you get permission denied error, just add proper permission to the file using chmod

The project also uploads generated video file to Google Drive, which uses a ``service-account.json`` file that can be configured and downloaded on to the root file of the project.
Simply follow instructions here to configure your own ``service-account.json`` file.
https://youtu.be/tamT_iGoZDQ?si=elyrKhOR-09pDS5x

Run the project using python 3.10 or above.
Run the main.py file to start the script
