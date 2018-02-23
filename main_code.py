import cv2
import sys 
import numpy 
import os 

class frec:
    def __init__(self):
        self.model = cv2.face.FisherFaceRecognizer_create()
        self.haar = "haarcascade_frontalface_default.xml"
        self.dir_ = "train_images"
        self.size_prep = 4
        self.size_train = 2
        self.im_width = 112
        self.im_height = 92
        self.names = {}
        self.images = []
        self.lables = []
        self.id = 0

    def prep_image(self):
        try:
            fn_name = sys.argv[1]
        except:
            print("You must provide a name")
            sys.exit(0)
        path = os.path.join(self.dir_, fn_name)
        if not os.path.isdir(path):
            os.mkdir(path)
        haar_cascade = cv2.CascadeClassifier(self.haar)
        webcam = cv2.VideoCapture(0)

        # Generate name for image file
        pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path)
             if n[0]!='.' ]+[0])[-1] + 1

        # Beginning message
        print("\n\033[94mThe program will save 100 samples. \
        Move your head around to increase while it runs.\033[0m\n")

        # The program loops until it has 20 images of the face.
        count = 0
        pause = 0
        count_max = 100
        while count < count_max:

            # Loop until the camera is working
            rval = False
            while(not rval):
                # Put the image from the webcam into 'frame'
                (rval, frame) = webcam.read()
                if(not rval):
                    print("Failed to open webcam. Trying again...")

            # Get image size
            height, width, channels = frame.shape

            # Flip frame
            frame = cv2.flip(frame, 1, 0)

            # Convert to grayscale
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Scale down for speed
            mini = cv2.resize(frame, (int(frame.shape[1] / self.size_prep), int(frame.shape[0] / self.size_prep)))

            # Detect faces
            faces = haar_cascade.detectMultiScale(mini)

            # We only consider largest face

            faces = sorted(faces, key=lambda x: x[3])
            if faces:
                face_i = faces[0]
                (x, y, w, h) = [v * self.size_prep for v in face_i]

                face = frame[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (self.im_width, self.im_height))

                # Draw rectangle and write name
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, fn_name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,
                    1,(0, 255, 0))

                # Remove false positives
                if(w * 6 < width or h * 6 < height):
                    print("Face too small")
                else:

                    # To create diversity, only save every fith detected image
                    if(pause == 0):

                        print("Saving training sample "+str(count+1)+"/"+str(count_max))

                        # Save image file
                        cv2.imwrite('%s/%s.png' % (path, pin), face_resize)

                        pin += 1
                        count += 1

                        pause = 1

            if(pause > 0):
                pause = (pause + 1) % 5
            cv2.imshow('OpenCV', frame)
            key = cv2.waitKey(10)
            if key == 27:
                break
    
    def train_model(self):

        # Part 1: Create fisherRecognizer
        print('Training...')

        # Get the folders containing the training data
        for (subdirs, dirs, files) in os.walk(self.dir_):

            # Loop through each folder named after the subject in the photos
            for subdir in dirs:
                self.names[self.id] = subdir
                subjectpath = os.path.join(self.dir_, subdir)

                # Loop through each photo in the folder
                for filename in os.listdir(subjectpath):

                    # Skip non-image formates
                    f_name, f_extension = os.path.splitext(filename)
                    if(f_extension.lower() not in
                            ['.png','.jpg','.jpeg','.gif','.pgm']):
                        print("Skipping "+filename+", wrong file type")
                        continue
                    path = subjectpath + '/' + filename
                    lable = self.id

                    # Add to training data
                    self.images.append(cv2.imread(path, 0))
                    self.lables.append(int(lable))
                self.id += 1

        # Create a Numpy array from the two lists above
        (self.images, self.lables) = [numpy.array(lis) for lis in [self.images, self.lables]]

        self.model.train(self.images, self.lables)

    def recognize(self): 
        haar_cascade = cv2.CascadeClassifier(self.haar)
        webcam = cv2.VideoCapture(0)
        while True:

            # Loop until the camera is working
            rval = False
            while(not rval):
                # Put the image from the webcam into 'frame'
                (rval, frame) = webcam.read()
                if(not rval):
                    print("Failed to open webcam. Trying again...")

            # Flip the image (optional)
            frame=cv2.flip(frame,1,0)

            # Convert to grayscalel
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Resize to speed up detection (optinal, change size above)
            mini = cv2.resize(gray, (int(gray.shape[1] / self.size_train), int(gray.shape[0] / self.size_train)))

            # Detect faces and loop through each one
            faces = haar_cascade.detectMultiScale(mini)
            for i in range(len(faces)):
                face_i = faces[i]

                # Coordinates of face after scaling back by `size`
                (x, y, w, h) = [v * self.size_train for v in face_i]
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (self.im_width, self.im_height))

                # Try to recognize the face
                prediction = self.model.predict(face_resize)
                print("prediction:" + str(prediction))
                print("names:" + str(self.names))
                print("labels:" + str(self.lables))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

                # [1]
                # Write the name of recognized face
                cv2.putText(frame,
                   '%s - %.0f' % (self.names[prediction[0]],prediction[1]),
                   (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))

            # Show the image and check for ESC being pressed
            cv2.imshow('OpenCV', frame)
            key = cv2.waitKey(10)
            if key == 27:
                break

def main(): 
    fr = frec()
    fr.train_model() 
    fr.recognize()

if __name__ == "__main__":
    main() 
