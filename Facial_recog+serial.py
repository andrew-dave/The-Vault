import serial  # Importing the serial module for communication with Arduino
from picamera2 import Picamera2, Preview  # Importing necessary modules for camera operations
import time  # Importing time module for time-related functions
import matplotlib.pyplot as plt  # Importing matplotlib for image visualization
from PIL import Image  # Importing PIL for image manipulation
import logging  # Importing logging module for logging events

# Configure logging
logging.basicConfig(filename='logfile.txt', level=logging.INFO, format='%(asctime)s-%(message)s')  # Configuring logging format and level
logging.info(" ")  # Logging an empty line for better readability in log file

# Open serial port connection with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change port if necessary

# Define image paths
authorized_image_path = "ac.jpeg"  # Path to authorized image
denied_image_path = "ad.jpeg"  # Path to denied image
picam2 = Picamera2()  # Creating an instance of Picamera2

# Define function to capture picture
def capture_picture():
    print("Capturing picture...")  # Logging message
    picam2.capture_file("/home/vault/frecog/detect face/face.jpg")  # Capturing image
    print("Picture captured.")  # Logging message

# Function to perform face recognition and authorization
def recognize_and_authorize(name, reference_image_path):
    logging.info(f"UID detected: {name}")  # Logging UID detection
    print(f"Authorized Access for {name}")  # Logging authorized access
    print("Starting camera preview...")  # Logging message
    camera_config = picam2.create_preview_configuration()  # Creating camera preview configuration
    picam2.configure(camera_config)  # Configuring camera
    picam2.start_preview(Preview.QTGL)  # Starting camera preview
    picam2.start()  # Starting camera operation
    time.sleep(2)  # Pausing for 2 seconds for stable camera operation
    
    # Capture picture
    capture_picture()  # Calling capture_picture function to capture image
    logging.info("Image Captured")  # Logging image capture
    print("Detecting Face...")  # Logging message
    from opencv.fr import FR  # Importing Face Recognition module
    from opencv.fr.search.schemas import SearchRequest, SearchMode  # Importing necessary modules for search request
    from opencv.fr.compare.schemas import CompareRequest  # Importing CompareRequest module
    from pathlib import Path  # Importing Path module for file operations
    
    # Initialize the SDK
    sdk = FR("https://us.opencv.fr", "eUUBa2nYjJmOTUwZTItYTViMS00Mzc4LTkyZWEtNzc3YmVhM2VlYTMx")  # Initializing Face Recognition SDK
    image_base_path = Path("/home/vault/frecog/detect face")  # Setting base path for images
    image_path = image_base_path / "face.jpg"  # Setting path for captured image
    
    # Creating search and compare requests
    search_request = SearchRequest([image_path], min_score=0.7, collection_id=None, search_mode=SearchMode.FAST)
    compare_request = CompareRequest([image_path], [reference_image_path], search_mode=SearchMode.FAST)
    
    # Performing search and comparison
    result = sdk.search.search(search_request)  # Searching for faces
    score = sdk.compare.compare_image_sets(compare_request)  # Comparing images
    
    # Checking if face is recognized and score is above threshold for authorization
    if result and score > 0.85:
        logging.info(f"Person information: {result[0].person}")  # Logging person information
        logging.info("Access Granted.")  # Logging access granted
        print(result[0].person)  # Printing person information
        print(result[0].score)  # Printing score
        img = plt.imread(authorized_image_path)  # Loading authorized image
    else:
        logging.info("Wrong/No face detected")  # Logging no face detected
        logging.info("Access Denied")  # Logging access denied
        print("No results found.")  # Logging message
        img = plt.imread(denied_image_path)  # Loading denied image

    # Displaying the image
    plt.imshow(img)  # Displaying image
    plt.axis('off')  # Turning off axis
    plt.draw()  # Drawing the image
    plt.pause(2)  # Pausing execution for 2 seconds
    plt.close()  # Closing the plot window
    
    # Sending signal to Arduino for access granted
    if score > 0.85:
        ser.write(b'R')  # Sending 'R' to Arduino indicating access granted

# Main loop for continuous operation
while True:
    if ser.in_waiting > 0:
        # Read data from Arduino
        data = ser.readline().decode().strip()  # Reading data from Arduino
        
        # Checking Arduino response for access denial or authorization for specific users
        if "Access denied" in data:
            logging.info("Access denied")  # Logging access denied
            img = plt.imread(denied_image_path)  # Loading denied image
            plt.figure(figsize=(15,10))  # Creating figure
            plt.imshow(img)  # Displaying image
            plt.axis('off')  # Turning off axis
            plt.draw()  # Drawing the image
            plt.pause(2)  # Pausing execution for 2 seconds
            plt.close()  # Closing the plot window
            break  # Exiting loop if access is denied
        elif "Authorized access for Andrew" in data:
            recognize_and_authorize("Andrew", "/home/vault/frecog/detect face/Andrew.jpg")  # Authorizing Andrew
            break  # Exiting loop after authorization
        elif "Authorized access for Devika" in data:
            recognize_and_authorize("Devika", "/home/vault/frecog/detect face/Devika.jpg")  # Authorizing Devika
            break  # Exiting loop after authorization
