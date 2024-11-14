# Ned2 Quick Start
This documentation provides a quick start guide for the Ned2 robot arm. You will learn how to connect to a Niryo Ned2 robot arm and control it using Python.

Official Ned documentation: https://docs.niryo.com/

Tips: 
- (October 2024): Niryo has moved all documentation. If you click on an old documentation page and it doesn’t exist, add “archive-” before “docs.” so the link starts with: “https://archive-docs…”. 
- if any command or script doesn't work and "ned" is part sof the name, try replacing "ned" with "ned2"

# Turn the robot on and off
- Turning on Ned: 
    - Press the power button at the back of the base (ensure that the emergency stop button, the large red button, is released).
    - Wait for the sound and light feedback. When it’s ready, the ring light will be blinking blue.
    
        * The ROS stack should automatically launch, giving light and sound feedback. If you don’t see the ring light change to a blinking blue pattern after a minute or two, run the following command on Ned’s terminal after SSHing into it from your computer: ```$ roslaunch niryo_robot_bringup niryo_ned2_robot.launch```

- Turning off Ned: 
    - Move the arm to a resting position while holding the “FREEMOTION” button (the rightmost button on the blue “forearm” above the gripper). If you don’t do this, the arm may collapse and hit the table when powered off.
    - Turn off Ned2 by holding the power button until you hear the sound feedback.

# Connect to Ned2 via WIFI or Ethernet
- WIFI connection
    - On your computer, Ned's WiFi name is something like "NiryoRobot" followed by some characters. Connect to Ned's WiFi, and the password is "niryorobot".
        - if you don't see it, check the back of Ned's base to make sure Wi-Fi (hot-spot) mode is on.
    - For more information, check this page: https://archive-docs.niryo.com/applications/ned/v1.0.4/en/source/tutorials/setup_connect_ned_ssh.html 
- Ethernet connection
    - **Using an ethernet cable provides the best connection to use the robot.**
    1. Configure your computer's wired setting by following the steps on this page: https://archive-docs.niryo.com/applications/ned/v1.0.4/en/source/tutorials/setup_connect_ned_ethernet.html
        - When setting your IP address, avoid using the same address as your Ned.
        - The IP addresses for the two Ned arms: 169.254.200.201 and 169.254.200.200. You can find your Ned’s IP address printed on the front sticker on the base.
    2. Restart your wired connection and plug the Ethernet cable between your computer and Ned.

# Control Ned2 using Python on your computer
- Required: 
    1. A connection to Ned via WiFi or Ethernet
    2. pyniryo2 library: https://archive-docs.niryo.com/dev/pyniryo2/v1.0.0/en/source/setup/installation.html

1. Connect to Ned via WIFI or Ethernet 
    - If you are connected to Ned through its wifi, the IP Address you will need to use is 10.10.10.10
    - If you are connected to Ned with an ethernet cable, the static IP of your robot will be 169.254.200.20X (X is depended on which Ned you are connected to)
2. On your computer, write and run your Python scripts.
    - To control Ned, you will need to instantiate the connection between your computer and Ned using the pyniryo API. For example,
        ```
        from pyniryo2 import *        # import the library
        robot_ip = "10.10.10.10"      # change to ethernet IP if needed
        robot = NiryoRobot(robot_ip)  # connect to Ned 
        joint_pos = [0.2, -0.3, 0.1, 0.0, 0.5, -0.8]
        robot.arm.move_joints(joint_pos)  # move Ned!
        ``` 
    - Click to check [sample scripts](URL#todo)

# SSH into Ned2's Raspberry Pi

**We don't recommand programming on Ned directly**.

Why ssh?
- To explore Ned’s Raspberry Pi system.
- Check Ned's ROS nodes, topics, etc. 
- To run sample scripts or launch ROS files.
- For other tasks, ideally without changing anything on Ned.
    
Steps:
1. connect to Ned via WIFI or Ethernet.
2. SSH into Ned
    1. On your computer's terminal, type in command: ```$ ssh niryo@<ned_ip>```
        - ned_ip=10.10.10.10 if connected via WIFT, or 169.254.200.200 or 169.254.200.201 via ethernet. For example: ```$ ssh niryo@169.254.200.201 ```
        
        - If you lose your Wi-Fi connection to the internet, try disconnecting from Ned, then reconnect to a working Wi-Fi network, and finally reconnect to Ned.
        - If you lose the Ethernet connection after your disconnet from Ned, ensure your wired settings are switched back to Automatic (DHCP).

    2. Enter Ned’s password: the default password is “robotics”.
        - Upon successful connection, you should see the prompt: ```niryo@ned2 ~ $```
    
3. Avoid changing any default settings, as these robots are shared by others.

4. Control Ned using python wrapper
    - Python ROS Wrapper is installed on Ned. see examples here: https://archive-docs.niryo.com/dev/ros/v4.1.1/en/source/ros_wrapper.html
    - Unlike pyniryo, the Python ROS Wrapper forces the user to write code directly in the robot, or, at least, copy the code on the robot via a terminal command..
    - You can run the sample python scripts on Ned (Click to check [more details about the scripts](URL#todo)). 

5. Exit the ssh connection: ```$ exit```



# *Use ROS to controal Ned2
Check List:
- Ubuntu 18.04
- ROS melodic
- Niryo ROS Stack 

Quick links
1. Install the Niryo ROS Stack: https://archive-docs.niryo.com/dev/ros/v4.1.1/en/source/installation/ubuntu_18.html
2. Use Ned through simulation: https://archive-docs.niryo.com/dev/ros/v4.1.1/en/source/simulation.html
3. ROS multimachine: https://archive-docs.niryo.com/applications/ned/v1.0.4/en/source/tutorials/moveit_multimachines.html

If you use **Docker**, check this repo (created by Matthew Stachyra): https://github.com/tufts-ai-robotics-group/ned2