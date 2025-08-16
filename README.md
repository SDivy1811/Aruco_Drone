****PX4 Simulation and ROS 2 Integration Guide****

**1. Prerequisites and Installation**


PX4 Autopilot & QGroundControl:
Follow the official documentation to install the necessary tools.

PX4 Autopilot:https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu

QGroundControl:https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/download_and_install.html

ROS 2 & Gazebo Bridge:
This guide assumes you are using ROS 2 Humble with Gazebo Harmonic.
```
bash

sudo apt install ros-humble-ros-gz-harmonic
```




PX4 ROS 2 Messages:
Clone and build the px4_msgs package in your ROS 2 workspace.
```
bash

# Navigate to your ROS 2 workspace source directory
cd ~/ros2_ws/src

# Clone the repository
git clone https://github.com/PX4/px4_msgs

# Navigate back to the workspace root
cd ..

# Build the package
colcon build --packages-select px4_msgs
```






Micro XRCE-DDS Agent:.

Clone the repository:



```
bash

git clone -b v2.4.2 https://github.com/eProsima/Micro-XRCE-DDS-Agent.git
```

**NOTE:**

**1.After runing the above command open the directory Micro-XRCE-DDS-Agent in VScode(or in file manger)**


**2.Go to CMakeLists.txt file  Line 99** 


**3.change set(_fastdds_tag 2.12.x) to set(_fastdds_tag v2.12.1) then run rest of commands**


Build and install:


```
bash

cd Micro-XRCE-DDS-Agent
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig /usr/local/lib/
```






**2. Setting Up the Simulation World**

Navigate to the PX4 Gazebo files:


1.open PX4-Autopilot directory.


2.go to tools>simulation>gz>models>OakD-Lite and replace the model.sdf file with the file(with the same name) given in this git repo.


3.go to tools>simulation>gz>worlds and replace the aruco.sdf file with the file(with the same name) given in this git repo.






**3. Running the Simulation**
Step 1: Launch PX4 with Gazebo
This command will start the PX4 simulation in the aruco world with the x500_depth model.
```
Bash

cd ~/PX4-Autopilot
PX4_GZ_WORLD=aruco make px4_sitl gz_x500_depth
```
A Gazebo simulation window with an ArUco marker should appear.

Step 2: Connect with QGroundControl
Open a new terminal.

Launch the QGroundControl AppImage.
```
Bash

/path/to/QGroundControl-x86_64.AppImage
(Note: Replace /path/to/ with the actual location of your AppImage, e.g., ~/Downloads/  in most cases it will be /Downloads)
```
Wait for the message INFO [commander] Ready for takeoff! in the Px4 terminal.

Takeoff: Press the Up arrow key on your keyboard and press Enter to initiate takeoff. The drone in the simulation should ascend.







4.Bridging Topics


**A.Gazebo to ROS 2 Bridge**
This bridge connects the camera feed from Gazebo to a ROS 2 topic, allowing you to visualize it in RViz.

Open a new terminal.

Run the ros_gz_bridge to connect the camera topic.
```
Bash

ros2 run ros_gz_bridge parameter_bridge \
/world/aruco/model/x500_depth_0/link/camera_link/sensor/IMX214/image@sensor_msgs/msg/Image@gz.msgs.Image
```
Verify the topic: You can confirm the topic is active by listing all available ROS 2 topics.
```
Bash

ros2 topic list
```
Visualize in RViz
Open a new terminal and launch RViz2.
```
Bash

rviz2
```
In the bottom-left corner of the RViz window, click Add.

Select the By topic tab.

Find and add the camera topic: /world/aruco/model/x500_depth_0/link/camera_link/sensor/IMX214/image. 
The image from the drone's camera should now be visible.




**B.PX4 to ROS 2 Bridge (Micro XRCE-DDS)**
This bridge allows you to exchange data between the PX4 autopilot and ROS 2 topics.

Turn off Wi-Fi to ensure a stable UDP connection.

Open a new terminal and start the Micro XRCE-DDS Agent.
```
Bash

MicroXRCEAgent udp4 -p 8888
```
In a separate terminal, run the PX4 simulation as described in Section 3, Step 1.

Open a third terminal and list the topics. You should now see PX4 topics being published on ROS 2.
```
Bash

ros2 topic list

```

