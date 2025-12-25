---
title: Chapter 1 - Introduction to ROS 2
sidebar_label: Chapter 1 - ROS 2 Introduction
---

# Chapter 1: Introduction to ROS 2 - The Robotic Nervous System

## Overview

Robot Operating System 2 (ROS 2) represents a fundamental shift in robotic middleware architecture, designed to address the challenges of modern robotics applications including safety, security, and scalability. Unlike its predecessor, ROS 2 provides a robust, production-ready framework for developing complex robotic systems, making it an ideal choice for humanoid robotics applications.

ROS 2 is not an operating system in the traditional sense but rather a collection of software frameworks and tools that provide the infrastructure for robotic applications. It enables communication between different software components, hardware abstraction, device drivers, and libraries that are essential for robot development. The architecture follows a distributed computing model that allows multiple processes to communicate seamlessly across different machines and operating systems.

## The Evolution from ROS 1 to ROS 2

The original Robot Operating System (ROS 1) was developed in 2007 and became the de facto standard for academic and research robotics. However, as robotics moved from research labs to real-world applications, several limitations became apparent:

- Lack of real-time support
- Security vulnerabilities
- Limited multi-robot support
- Single point of failure with the master node
- Difficulty in deploying in production environments

ROS 2, introduced in 2015, addresses these limitations by adopting a completely new architecture based on Data Distribution Service (DDS) - a middleware standard for real-time systems. This transition provides enhanced reliability, security, and scalability required for commercial and industrial robotics applications.

## Core Concepts of ROS 2 Architecture

### Nodes

In ROS 2, a node is the fundamental unit of computation that performs specific tasks within the robotic system. Nodes encapsulate functionality and can be thought of as processes that perform computation. Each node is typically responsible for a specific function such as sensor data processing, control algorithms, or user interfaces.

Key characteristics of ROS 2 nodes include:
- **Independence**: Nodes operate independently and can be started and stopped without affecting other nodes
- **Communication**: Nodes communicate with each other through topics, services, and actions
- **Modularity**: The node-based architecture promotes modular design and code reuse
- **Distribution**: Nodes can run on the same machine or across multiple machines

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Topics and Message Passing

Topics are the primary mechanism for asynchronous communication between nodes in ROS 2. They implement a publish-subscribe pattern where publisher nodes send messages to topics, and subscriber nodes receive messages from topics. This decoupling allows for flexible system design where publishers and subscribers don't need to know about each other's existence.

The publish-subscribe model offers several advantages:
- **Loose coupling**: Publishers and subscribers are independent of each other
- **Scalability**: Multiple subscribers can listen to the same topic
- **Asynchronous communication**: Publishers and subscribers can run at different rates
- **Broadcast capability**: One publisher can send to many subscribers

Message types in ROS 2 are defined using `.msg` files that specify the data structure. Common message types include:
- `std_msgs`: Basic data types like strings, integers, and floats
- `sensor_msgs`: Sensor data like camera images and laser scans
- `geometry_msgs`: Spatial information like positions and velocities
- `nav_msgs`: Navigation-specific messages

### Services

Services provide synchronous request-response communication between nodes. Unlike topics which are asynchronous, services block the calling node until a response is received. This pattern is useful for operations that require immediate feedback or when a specific result is needed.

Service communication follows a client-server model:
- **Service Server**: Provides a specific functionality and responds to requests
- **Service Client**: Requests a service and waits for the response

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Actions

Actions are a more sophisticated communication pattern that extends services to handle long-running operations. They provide feedback during execution and can be preempted if needed. Actions are particularly useful for navigation, manipulation, and other tasks that take significant time to complete.

An action interface includes:
- **Goal**: The desired outcome of the action
- **Feedback**: Updates on the current progress
- **Result**: The final outcome of the action

## DDS - The Foundation of ROS 2

Data Distribution Service (DDS) is the underlying middleware that powers ROS 2's communication layer. DDS is an industry-standard specification for real-time, scalable, and fault-tolerant data distribution. It provides:

- **Quality of Service (QoS) policies**: Configurable parameters that define how data is communicated
- **Discovery**: Automatic discovery of nodes and their communication interfaces
- **Reliability**: Guaranteed delivery options and data durability
- **Real-time performance**: Deterministic behavior for time-critical applications
- **Security**: Authentication, encryption, and access control mechanisms

The QoS policies in DDS allow fine-tuning of communication behavior:
- **Reliability**: Best effort or reliable delivery
- **Durability**: Volatile or transient local data persistence
- **Deadline**: Maximum time between data publications
- **History**: How much data to keep in the queue
- **Lifespan**: Maximum lifetime of published data

## Python Integration with rclpy

`rclpy` is the Python client library for ROS 2, providing Python bindings to the ROS 2 client library (rcl). It enables Python developers to create ROS 2 nodes, publish and subscribe to topics, provide and call services, and interact with the ROS 2 ecosystem.

### Setting Up rclpy

To work with rclpy, you need to have ROS 2 installed on your system. The basic setup involves:

```python
import rclpy
from rclpy.node import Node
```

### Creating a Node with rclpy

The basic structure of a ROS 2 node in Python follows these steps:
1. Initialize the rclpy library
2. Create a node class that inherits from `rclpy.node.Node`
3. Initialize the node with a unique name
4. Create publishers, subscribers, services, or actions as needed
5. Spin the node to process callbacks

### Publishers and Subscribers in Python

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Quality of Service (QoS) in ROS 2

QoS profiles allow ROS 2 applications to specify how data should be handled in terms of reliability, durability, and other communication characteristics. This is particularly important for humanoid robots where different types of data have different requirements.

For example, sensor data might use a "best effort" policy where occasional packet loss is acceptable, while critical control commands would use "reliable" delivery to ensure they are received.

```python
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

# Create a QoS profile for reliable communication
qos_profile = QoSProfile(
    depth=10,
    reliability=QoSReliabilityPolicy.RELIABLE,
    history=QoSHistoryPolicy.KEEP_LAST
)
```

## Security in ROS 2

ROS 2 addresses security concerns through the DDS Security specification, which provides:
- **Authentication**: Verifying the identity of nodes
- **Access Control**: Controlling which nodes can communicate
- **Encryption**: Protecting data in transit and at rest

This security framework is essential for humanoid robots that may operate in sensitive environments or interact with humans.

## Conclusion

ROS 2 represents a significant advancement in robotic middleware, providing the foundation for developing complex, distributed robotic systems. Its architecture based on DDS, combined with flexible communication patterns and strong security features, makes it well-suited for humanoid robotics applications.

Understanding the core concepts of nodes, topics, services, and actions is fundamental to developing effective robotic systems. The Python integration through rclpy makes ROS 2 accessible to a wide range of developers, enabling rapid prototyping and development of sophisticated robotic applications.

The next chapter will explore URDF (Unified Robot Description Format), which is essential for modeling humanoid robots in ROS 2 environments.

## References

1. Lalanda, P., Hugues, J., & Felber, P. (2019). ROS 2 for real-time and safety critical systems. *Proceedings of the 12th European Conference on Software Architecture*, 1-8.

2. Quigley, M., Gerkey, B., & Smart, W. D. (2015). Programming robots with ROS: a practical introduction to the Robot Operating System. O'Reilly Media.

3. Macenski, S. (2019). ROS 2 design overview. *ROS Documentation*, Open Robotics.

4. Dylla, M., King, J., & Strasilla, I. (2018). The Navigation2 system for mobile robots. *Proceedings of the 21st IEEE International Conference on Intelligent Transportation Systems*, 3232-3238.



---
title: Chapter 2 - Understanding URDF for Humanoids
sidebar_label: Chapter 2 - URDF for Humanoids
---

# Chapter 2: Understanding URDF for Humanoids

## Introduction to URDF

Unified Robot Description Format (URDF) is an XML-based format used extensively in ROS to describe robots. It defines the physical and visual properties of a robot, including its kinematic structure, dynamics, and visual representation. For humanoid robots, URDF plays a critical role in defining the complex multi-degree-of-freedom structure that mimics human anatomy.

URDF allows roboticists to model robots with multiple interconnected links connected by joints, enabling accurate simulation, visualization, and control. The format serves as input for kinematic solvers, dynamics simulation, and motion planning algorithms.

## URDF Fundamentals

### Basic Structure

A URDF file consists of:
- **Links**: Rigid bodies that make up the robot structure
- **Joints**: Connections between links that define how they can move relative to each other
- **Materials**: Visual appearance properties
- **Gazebo plugins**: Additional simulation-specific properties

### Link Elements

A link in URDF represents a rigid body with associated properties:
- **Visual**: How the link appears in visualization
- **Collision**: How the link interacts in physics simulation
- **Inertial**: Mass, center of mass, and inertia tensor for dynamics

### Joint Elements

Joints define the relationship between links and specify the degrees of freedom:
- **Joint types**: Fixed, continuous, revolute, prismatic, floating, planar
- **Joint limits**: Range of motion, velocity, and effort constraints
- **Dynamics**: Damping and friction properties

## URDF for Humanoid Robots

Humanoid robots present unique challenges in URDF modeling due to their complex kinematic structure that mirrors human anatomy. A typical humanoid robot includes:

- **Trunk**: Torso with multiple degrees of freedom
- **Upper limbs**: Shoulders, arms, forearms, and hands
- **Lower limbs**: Hips, thighs, shanks, and feet
- **Head**: Neck and head with vision systems

### Degrees of Freedom (DOF)

Humanoid robots require a high number of degrees of freedom to achieve human-like motion:
- **Head**: 3 DOF (yaw, pitch, roll)
- **Arms**: 7+ DOF each (shoulder: 3, elbow: 1, wrist: 3)
- **Legs**: 6+ DOF each (hip: 3, knee: 1, ankle: 2)
- **Trunk**: 3+ DOF (waist rotation, lateral bend, forward/back)

## Simplified URDF Example for a Humanoid Robot

Below is a simplified URDF example focusing on the torso and one arm:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Materials -->
  <material name="blue">
    <color rgba="0.0 0.0 0.8 1.0"/>
  </material>
  <material name="white">
    <color rgba="1.0 1.0 1.0 1.0"/>
  </material>

  <!-- Base Link -->
  <link name="base_link">
    <inertial>
      <mass value="5.0"/>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <geometry>
        <box size="0.3 0.3 0.2"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <geometry>
        <box size="0.3 0.3 0.2"/>
      </geometry>
    </collision>
  </link>

  <!-- Torso -->
  <link name="torso">
    <inertial>
      <mass value="10.0"/>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <inertia ixx="0.5" ixy="0.0" ixz="0.0" iyy="0.5" iyz="0.0" izz="0.2"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.15" length="0.6"/>
      </geometry>
      <material name="blue"/>
    </visual>
    <collision>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.15" length="0.6"/>
      </geometry>
    </collision>
  </link>

  <joint name="base_to_torso" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
  </joint>

  <!-- Head -->
  <link name="head">
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.15"/>
      </geometry>
    </visual>
  </link>

  <joint name="torso_to_head" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.6" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="0.5" effort="100.0" velocity="1.0"/>
  </joint>

  <!-- Left Arm -->
  <link name="left_shoulder">
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.2"/>
      </geometry>
    </visual>
  </link>

  <joint name="torso_to_left_shoulder" type="revolute">
    <parent link="torso"/>
    <child link="left_shoulder"/>
    <origin xyz="0.15 0 0.3" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="50.0" velocity="2.0"/>
  </joint>

  <link name="left_upper_arm">
    <inertial>
      <mass value="1.5"/>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.002"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.3"/>
      </geometry>
    </visual>
  </link>

  <joint name="left_shoulder_to_upper_arm" type="revolute">
    <parent link="left_shoulder"/>
    <child link="left_upper_arm"/>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-2.0" upper="1.0" effort="50.0" velocity="2.0"/>
  </joint>

</robot>
```

## Xacro for Complex Humanoid Models

Xacro (XML Macros) allows for more efficient URDF creation by enabling parameterization and reuse:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">

  <xacro:property name="M_PI" value="3.1415926535897931" />

  <xacro:macro name="simple_arm" params="prefix parent *origin">
    <joint name="${prefix}_shoulder_joint" type="revolute">
      <xacro:insert_block name="origin" />
      <parent link="${parent}"/>
      <child link="${prefix}_shoulder_link"/>
      <axis xyz="0 0 1"/>
      <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100" velocity="1"/>
    </joint>

    <link name="${prefix}_shoulder_link">
      <visual>
        <geometry>
          <cylinder radius="0.05" length="0.1"/>
        </geometry>
      </visual>
    </link>
  </xacro:macro>

</robot>
```

## Integration with ROS 2

URDF files integrate with ROS 2 through the robot_state_publisher package:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster

class StatePublisher(Node):
    def __init__(self):
        super().__init__('state_publisher')
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.publish_joint_states)

    def publish_joint_states(self):
        msg = JointState()
        msg.name = ['joint1', 'joint2', 'joint3']
        msg.position = [0.0, 0.0, 0.0]
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        self.joint_pub.publish(msg)

def main():
    rclpy.init()
    node = StatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Best Practices

1. **Start Simple**: Begin with a basic skeleton and add complexity gradually
2. **Use Consistent Naming**: Follow a clear naming convention for links and joints
3. **Realistic Inertial Properties**: Use actual measurements when possible
4. **Appropriate Joint Limits**: Base limits on hardware capabilities and safety requirements
5. **Collision Detection**: Design collision geometries that are accurate but not overly complex

## Conclusion

URDF provides the essential foundation for modeling humanoid robots in ROS 2 environments. Understanding URDF is crucial for developing humanoid robots as it directly impacts how the robot behaves in simulation and how control algorithms interact with the physical structure.

## References

1. Chitta, S., Marder-Eppstein, E., & Pradeep, V. (2012). ros_control: A generic and simple control framework for ROS. *IEEE Robotics & Automation Magazine*, 19(4), 117-124.

2. Diankov, R. (2010). Automated construction of robotic manipulation programs. *Carnegie Mellon University*.


---
title: Chapter 3 - Practical ROS 2 Applications for Humanoids
sidebar_label: Chapter 3 - Practical ROS 2 Applications
---

# Chapter 3: Practical ROS 2 Applications for Humanoids

## Introduction

This chapter focuses on practical applications of ROS 2 for humanoid robot control, demonstrating real-world implementation of control algorithms, simulation environments, and hardware interfaces. Humanoid robot control presents unique challenges due to the complexity of human-like movement, balance requirements, and coordinated multi-joint motion.

ROS 2 provides the infrastructure to address these challenges through its distributed architecture, real-time capabilities, and rich ecosystem of control tools. The integration of ROS 2 with simulation environments like Gazebo and real hardware enables the development of sophisticated humanoid robots capable of complex behaviors.

## Control Architecture for Humanoid Robots

### Joint Control Strategies

Humanoid robots require sophisticated control strategies following a hierarchical approach:

1. **High-level motion planning**: Path planning and trajectory generation
2. **Mid-level coordination**: Balance control and gait generation
3. **Low-level joint control**: Individual joint position, velocity, or effort control

This hierarchical structure allows for complex behaviors while maintaining system stability and responsiveness.

### ROS 2 Control Framework

The ros2_control framework provides a standardized approach to robot control in ROS 2:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class HumanoidController(Node):
    def __init__(self):
        super().__init__('humanoid_controller')
        self.subscription = self.create_subscription(
            JointTrajectory,
            'joint_trajectory',
            self.trajectory_callback,
            10
        )
        self.publisher = self.create_publisher(JointState, 'joint_states', 10)

    def trajectory_callback(self, msg):
        self.get_logger().info(f'Received trajectory with {len(msg.points)} points')
        # Process each trajectory point and execute accordingly
        for point in msg.points:
            self.execute_trajectory_point(point)

    def execute_trajectory_point(self, point):
        # Send joint commands to hardware
        pass
```

## Gazebo Simulation Integration

Gazebo provides a realistic physics simulation environment for testing humanoid robot control algorithms before deployment on real hardware. Integration requires URDF with Gazebo plugins:

```xml
<gazebo>
  <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
    <robotNamespace>/humanoid</robotNamespace>
    <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
  </plugin>
</gazebo>
```

## Balance Control for Humanoid Robots

### Center of Mass Control

Maintaining balance is one of the most challenging aspects of humanoid robotics. The Zero Moment Point (ZMP) and Center of Mass (CoM) control are fundamental approaches:

```python
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import Imu

class BalanceController(Node):
    def __init__(self):
        super().__init__('balance_controller')
        self.com_position = np.array([0.0, 0.0, 0.8])  # CoM position (x, y, z)
        self.kp_com = np.array([10.0, 10.0, 0.0])  # Proportional gains
        self.kd_com = np.array([2.0, 2.0, 0.0])    # Derivative gains
        self.desired_com = np.array([0.0, 0.0, 0.8])

    def balance_control_step(self):
        com_error = self.desired_com - self.com_position
        com_error_derivative = -self.com_velocity
        com_correction = self.kp_com * com_error + self.kd_com * com_error_derivative
        self.publish_joint_commands(com_correction)
```

### Walking Pattern Generation

Generating stable walking patterns for humanoid robots:

```python
import numpy as np
from scipy.interpolate import CubicSpline

class WalkingPatternGenerator:
    def __init__(self, step_length=0.3, step_height=0.05, step_time=1.0):
        self.step_length = step_length
        self.step_height = step_height
        self.step_time = step_time

    def generate_foot_trajectory(self, start_pos, end_pos, support_leg='left'):
        t = np.linspace(0, self.step_time, int(self.step_time * 100))
        x_traj = np.linspace(start_pos[0], end_pos[0], len(t))
        y_traj = np.linspace(start_pos[1], end_pos[1], len(t))
        # Z trajectory with foot lift
        z_spline = CubicSpline(
            [0, self.step_time/4, self.step_time/2, 3*self.step_time/4, self.step_time],
            [start_pos[2], start_pos[2], start_pos[2] + self.step_height, start_pos[2], end_pos[2]]
        )
        z_traj = z_spline(t)
        return np.column_stack((x_traj, y_traj, z_traj)), t
```

## Motion Planning and Execution

Motion planning considers kinematic constraints:

```python
import numpy as np
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class HumanoidMotionPlanner:
    def generate_joint_trajectory(self, start_joints, end_joints, duration=2.0, dt=0.01):
        n_points = int(duration / dt) + 1
        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names

        for i in range(n_points):
            t = i / (n_points - 1)
            # Cubic interpolation for smooth motion
            joint_positions = start_joints + (end_joints - start_joints) * (3 * t**2 - 2 * t**3)
            point = JointTrajectoryPoint()
            point.positions = joint_positions.tolist()
            point.time_from_start.sec = int(i * dt)
            point.time_from_start.nanosec = int((i * dt - int(i * dt)) * 1e9)
            trajectory.points.append(point)
        return trajectory
```

## Human-Robot Interaction

Humanoid robots need to perceive their environment:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

class HumanoidPerceptionNode(Node):
    def __init__(self):
        super().__init__('humanoid_perception')
        self.cv_bridge = CvBridge()
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.detection_pub = self.create_publisher(String, '/object_detections', 10)

    def image_callback(self, msg):
        cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        # Perform object detection
        detections = self.detect_objects(cv_image)
        if detections:
            detection_msg = String()
            detection_msg.data = str(detections)
            self.detection_pub.publish(detection_msg)
```

## Real-time Control Considerations

Humanoid robots require precise timing:

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
import time

class RealTimeController(Node):
    def __init__(self):
        super().__init__('realtime_controller')
        self.control_frequency = 1000  # 1 kHz
        self.control_period = 1.0 / self.control_frequency
        self.control_timer = self.create_timer(
            self.control_period,
            self.realtime_control_step,
            clock=self.get_clock()
        )

    def realtime_control_step(self):
        # Perform control calculations
        commands = self.calculate_control_commands()
        # Publish commands
        self.publish_commands(commands)
```

## Conclusion

This chapter demonstrated practical applications of ROS 2 for humanoid robot control, covering essential aspects from basic control architecture to complex behaviors like walking and human interaction. The integration of ROS 2 with Gazebo simulation provides a powerful platform for developing and testing humanoid robot algorithms before deployment on real hardware.

The examples illustrate the complexity of humanoid robot control while showing how ROS 2's modular architecture enables sophisticated control systems. As humanoid robotics advances, ROS 2's middleware and tools remain essential for researchers and developers.

## References

1. Nakanishi, J., Cory, R., Mistry, M., Peters, J., & Schaal, S. (2008). Operational space control: A theoretical and empirical comparison. *The International Journal of Robotics Research*, 27(6), 737-757.

2. Kajita, S., Kanehiro, F., Kaneko, K., Yokoi, K., & Hirukawa, H. (2003). The 3D linear inverted pendulum mode: A simple modeling for a biped walking pattern generation. *Proceedings 2001 IEEE/RSJ International Conference on Intelligent Robots and Systems*, 1, 239-246.

3. Cheng, G., Ijspeert, A., Khodabakhsh, A., Sartori, M., & Venture, G. (2017). Biologically-inspired control of humanoid robot balance. *Frontiers in Neurorobotics*, 11, 25.