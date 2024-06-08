# AIContentGenerator

Install all the python libraries using 
``pip install -r requirements.txt``

There are some additional libraries that will be required such as ```imagemagick```
After installing it using   
```sudo apt-get install imagemagick``` run the following command:
``cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml``

If you get permission denied error, just add proper permission to the file using chmod

Run the project using python 3.10 or above.
Run the main.py file to start the script
