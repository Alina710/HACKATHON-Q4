---
title: Robot Structure and URDF
sidebar_position: 3
---

### **What is URDF?**

**URDF** (Unified Robot Description Format) is an **XML-based** format used to describe the **physical structure** of a robot in a standardized way. It defines how a robot looks, moves, and interacts with its environment, providing all the necessary details about the robot's parts (links) and how they are connected (joints).

URDF allows the robot's structure to be defined in a way that both **humans** and **ROS tools** (like RViz, Gazebo, etc.) can interpret. It’s a core part of robotic modeling and simulation, especially for complex robots, including **humanoid robots**.

### **Components of URDF**

A URDF file is made up of the following core components:

1. **Links**: Represents the rigid parts of the robot. These are the individual "pieces" that make up the robot, such as arms, legs, torso, wheels, etc.

   Each **link** can have several properties:

   * **Visual properties**: Define how the link looks (e.g., color, texture).
   * **Collision properties**: Define the shape used for collision detection.
   * **Inertial properties**: Define the mass, inertia, and center of gravity.

2. **Joints**: Define how the links are connected and how they move relative to each other. Joints represent the robot's degrees of freedom (DOF).

   Common joint types include:

   * **Revolute**: Allows rotational movement (e.g., a robot's elbow).
   * **Prismatic**: Allows linear sliding (e.g., a sliding drawer).
   * **Fixed**: The link does not move relative to the parent link.
   * **Continuous**: A joint that allows continuous rotation without limits (e.g., wheels).

---

### **Example URDF for a Simple Robot**

Let’s walk through a simple **URDF** example for a two-link robot arm. The robot will consist of two parts: a base and an arm with a revolute joint.

#### **Robot URDF Example**:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">

  <!-- Link 1: Base -->
  <link name="base">
    <visual>
      <geometry>
        <box size="0.2 0.2 0.1" />
      </geometry>
      <material name="blue"/>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.2 0.1" />
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0" />
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Link 2: Arm -->
  <link name="arm">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.5"/>
      </geometry>
      <material name="green"/>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5" />
      <inertia ixx="0.002" ixy="0" ixz="0" iyy="0.002" iyz="0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Revolute Joint: Base to Arm -->
  <joint name="base_to_arm" type="revolute">
    <parent link="base"/>
    <child link="arm"/>
    <origin xyz="0 0 0.25" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit effort="10.0" velocity="1.0" lower="0" upper="1.57"/>
  </joint>

</robot>
```

### **Explanation of the URDF Elements**:

1. **`<robot>`**: The root element that defines the robot’s name.

2. **`<link>`**: Defines the physical parts of the robot. Each link can have:

   * **Visual properties**: A `box` for the base and a `cylinder` for the arm to represent their shapes. Each link also has a **material** tag to define its color.
   * **Collision properties**: Defines the shapes used for collision detection, which may differ from visual properties in more advanced models.
   * **Inertial properties**: Defines the mass and inertia of each link, which is essential for realistic simulation and physics calculations.

3. **`<joint>`**: Defines the relationship between two links. In this case:

   * The joint type is `revolute`, meaning the arm will rotate relative to the base.
   * The **origin** tag defines the position and orientation of the joint (in this case, 0.25 meters along the Z-axis).
   * The **axis** tag specifies the axis of rotation.
   * The **limit** tag defines the joint’s limits (in this case, the arm can rotate between 0 and 1.57 radians, which is 90 degrees).

### **URDF in ROS 2**

In ROS 2, **URDF** files can be loaded and used for robot visualization, simulation, and control. We typically use **RViz** to visualize the robot and **Gazebo** for physical simulations.

### **Loading and Visualizing URDF in RViz**

To visualize the robot using RViz, we need to load the URDF model. Here is how you can do that:

1. **Run RViz** with ROS 2:

   Open a terminal and type:

   ```bash
   ros2 run rviz2 rviz2
   ```

2. **Set up the URDF in ROS 2**:

   You can load a URDF file into **RViz** using a **robot state publisher** node. Create a launch file that loads your URDF.

#### **Launch File Example** (Python-based)

Create a new Python launch file to load the URDF into RViz. Save this as `launch_display_urdf.py`.

```python
import launch
from launch import LaunchDescription
from launch.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': open('path_to_urdf/simple_robot.urdf').read()}]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        )
    ])
```

#### **Launch the File**:

Now, use the ROS 2 launch system to run the URDF and RViz:

```bash
ros2 launch your_package_name launch_display_urdf.py
```

This command will launch the **robot_state_publisher** to load the URDF and open **RViz** to visualize it.

---

### **URDF for Humanoid Robots**

Humanoid robots, such as **ASIMO** or **Atlas**, have very complex structures with many joints. URDF allows for precise modeling of these structures, including:

* **Joint limits** (e.g., the range of motion for arms and legs)
* **Degrees of freedom (DOF)** (the number of independent movements)
* **Mass and inertia** (essential for simulating balance and control)
* **Center of gravity** (important for stability)

When working with humanoid robots in ROS 2, you would typically use URDF to model each part of the robot and define the connections (joints) between them. You might also define controllers to handle the complex movements required for walking, balancing, and interacting with humans.

---

### **ROS 2 Tools that Use URDF**

ROS 2 integrates **URDF** with several important tools:

* **RViz**: Visualizes the robot's structure and current state.
* **Gazebo**: Simulates the robot in a physics-based environment.
* **MoveIt!**: A motion planning library that uses the robot’s URDF to plan complex movements like grasping, arm motion, and navigation.
* **ros2_control**: A framework for controlling robot hardware, which uses URDF for defining robot capabilities.

---

### **Summary**

URDF is essential in ROS 2 for describing the physical structure of robots. It enables **visualization** in RViz, **simulation** in Gazebo, **motion planning** in MoveIt, and **control algorithms** using ros2_control. By using URDF, you can create a precise, digital representation of your robot’s hardware, allowing you to develop sophisticated robotic systems.


