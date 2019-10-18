# Smart-Checkout-system
This Project uses Atificial Intellegence Image Detection technique to detect and categorise grocery products.

# Required Material
1.   Raspberry Pi "Raspberry Pi 3 Model B+  has been used in this work "
2.   Pi camera
3.   Development computer running windows with VNC viewer installed on it.

# Poject installation and running
0. connect to raspberry pi using VNC viewer.
1. First of all you have to setup greengrass group on raspberry pi
   Please follow the installation guide provided by AWS
   https://docs.aws.amazon.com/greengrass/latest/developerguide/setup-filter.rpi.html  

      ``` While following Above guide you will get your own key file. ```

2. Download This Github repository and copy those key files in the root directory of the project.
3. run the following commands to install the dependencies.
    - sudo apt update
    - sudo apt install python3-picamera
    - sudo apt install python3-pip
    - pip3 install Flask
    - pip3 install AWSIoTPythonSDK
    - pip install opencv-wrapper
    - **to install tensorflow run following command**
      * sudo apt install libatlas-base-dev
      * pip3 install tensorflow
    - pip3 install numpy
    - pip3 install keras
4. connect your Camera to the raspberry pi
      ### Raspberry pi Camera
   ![image](https://raw.githubusercontent.com/kmranrg/ProductDetection/master/static/img/raspberry_pi_model_1.jpg "raspberry pi camera setup")

## Running the Project
Go to your project directory  and run the following command
1. `export FLASK_APP=model.py`
2. `flask run`

## Project Demo Images
<img src="img/Screenshot (276).png" alt="Sending data to greengrass subscription" width="400px"  style="float:left;margin-right:10px;"><img src="img/Screenshot (277).png" alt="detection of product" width="400px" style="float:right;margin-right:10px;"> <img src="img/Screenshot (278).png" alt="detection of product" width="400px" style="float:left;margin-right:10px;"> <img src="img/Screenshot (279).png" alt="Bill of Products" width="400px" style="float:right;margin-right:10px;">
