import numpy
import cv2
from cvzone.HandTrackingModule import HandDetector
import boto3
allos = []
cap = cv2.VideoCapture(0)
status, photo = cap.read()

detector = HandDetector(maxHands=1)

ec2 = boto3.resource("ec2")

def myoslaunch():
  instances = ec2.create_instances(
        ImageId="ami-0a2acf24c0d86e927",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SecurityGroupIds=["sg-04e03a0e57f5fe713"]
        #KeyName="KeyPair1"
    )
  myid = instances[0].id
  allos.append(myid)
  print("Total OS : ", len(allos))
  print(myid)

def osdelete():
 if allos:
        osdelete = allos.pop()
        ec2.instances.filter(InstanceIds=[osdelete]).terminate()
        print("Total OS: ", len(allos))
 else:
        print("No instances to delete")
 
# Flag variable to keep track of printing the number of instances
is_printed = False

while True:
    status, photo = cap.read()
    cv2.imshow("mypic", photo)
    
    hand = detector.findHands(photo, draw=False)
    if hand:
        lmlist = hand[0]
        tfingers = detector.fingersUp(lmlist)
        if tfingers == [0, 1, 1, 0, 0]:
            myoslaunch()
            is_printed = False
        elif tfingers == [0, 1, 0, 0, 0]:
            osdelete()
            is_printed = False
        else:
            print("Chala jaa ....")
        
    # Get the number of running instances
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    allos = [instance.id for instance in instances]
    
    # Print the number of running instances only once if not already printed
    if not is_printed:
        print("Number of running instances:", len(allos))
        is_printed = True
    
    if cv2.waitKey(10) == 13:
        break

cv2.destroyAllWindows()
cap.release()









