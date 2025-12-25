---
title: Introduction to ROS 2
sidebar_position: 1
---
### **ROS 2 Node Example**

A **node** is the basic unit of computation in ROS 2. It’s a program that performs a specific task, such as controlling a motor or processing sensor data.

Let’s create a simple ROS 2 node that prints "Hello, ROS 2!" every 2 seconds.

#### **Hello ROS 2 Node Example** (Python)

```python
import rclpy
from rclpy.node import Node

class HelloRos2Node(Node):
    def __init__(self):
        super().__init__('hello_ros2_node')
        self.get_logger().info('Hello, ROS 2!')
        # Create a timer to call the callback function every 2 seconds
        self.timer = self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info('ROS 2 is running...')

def main(args=None):
    rclpy.init(args=args)
    hello_ros2_node = HelloRos2Node()
    rclpy.spin(hello_ros2_node)  # Keep the node running
    hello_ros2_node.destroy_node()  # Clean up when done
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

In this example:

* The node is named `hello_ros2_node`.
* The node logs the message "Hello, ROS 2!" at startup.
* It also uses a **timer** to log "ROS 2 is running..." every 2 seconds.

### **ROS 2 Topics (Publisher-Subscriber)**

Topics in ROS 2 are used for **asynchronous communication**. Nodes can publish messages to topics, and other nodes can subscribe to those topics to receive data. This is part of the **Publisher-Subscriber** model.

#### **Publisher Node** Example (Publishing Data)

Let’s create a **publisher** node that sends integer data (representing the number of "frames" processed by a robot’s camera) every second.

**camera_publisher.py**:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class CameraPublisherNode(Node):
    def __init__(self):
        super().__init__('camera_publisher_node')
        self.publisher_ = self.create_publisher(Int32, 'camera_frames', 10)  # Topic name: camera_frames
        self.timer = self.create_timer(1.0, self.publish_frame_count)  # Publish every 1 second
        self.frame_count = 0

    def publish_frame_count(self):
        msg = Int32()
        msg.data = self.frame_count
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing frame count: {self.frame_count}")
        self.frame_count += 1

def main(args=None):
    rclpy.init(args=args)
    camera_publisher_node = CameraPublisherNode()
    rclpy.spin(camera_publisher_node)
    camera_publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

In this example:

* The **camera_publisher_node** publishes the frame count as an integer to the topic `camera_frames`.
* The node sends an updated frame count every second.

#### **Subscriber Node** Example (Receiving Data)

Next, let's create a **subscriber** node that listens to the `camera_frames` topic and prints the received frame count.

**camera_subscriber.py**:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class CameraSubscriberNode(Node):
    def __init__(self):
        super().__init__('camera_subscriber_node')
        # Subscribe to the camera_frames topic
        self.subscription = self.create_subscription(
            Int32,  # Message type
            'camera_frames',  # Topic name
            self.listener_callback,  # Callback function
            10  # Queue size
        )

    def listener_callback(self, msg):
        self.get_logger().info(f"Received frame count: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    camera_subscriber_node = CameraSubscriberNode()
    rclpy.spin(camera_subscriber_node)  # Keep the node running
    camera_subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

In this example:

* The **camera_subscriber_node** subscribes to the `camera_frames` topic.
* Every time a message is received (the frame count), the subscriber node logs the received value.

---

### **ROS 2 Services (Request-Response Model)**

In ROS 2, services are used for **synchronous communication**. A client sends a request to a server, and the server processes the request and sends back a response.

#### **Service Server Example (Reset Position)**

Let’s create a **service server** that resets the robot’s position when it receives a request.

**reset_position_server.py**:

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class ResetPositionServer(Node):
    def __init__(self):
        super().__init__('reset_position_server')
        # Create a service that will reset the robot's position
        self.srv = self.create_service(Trigger, 'reset_position', self.reset_position_callback)

    def reset_position_callback(self, request, response):
        self.get_logger().info('Resetting robot position to (0, 0)')
        response.success = True
        response.message = "Position reset successful"
        return response

def main(args=None):
    rclpy.init(args=args)
    reset_position_server = ResetPositionServer()
    rclpy.spin(reset_position_server)  # Keep the server running
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

In this example:

* The **reset_position_server** creates a service called `reset_position`, which responds to requests by resetting the robot's position to `(0, 0)`.
* When a client calls this service, it responds with a success message.

#### **Service Client Example (Request Reset)**

Let’s create a **service client** that sends a request to the `reset_position` service.

**reset_position_client.py**:

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class ResetPositionClient(Node):
    def __init__(self):
        super().__init__('reset_position_client')
        self.cli = self.create_client(Trigger, 'reset_position')  # Call the reset_position service
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.request = Trigger.Request()

    def send_request(self):
        self.future = self.cli.call_async(self.request)  # Send the service request
        rclpy.spin_until_future_complete(self, self.future)  # Wait for the response
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    reset_position_client = ResetPositionClient()
    response = reset_position_client.send_request()
    print(f"Response: {response.message}")
    reset_position_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

In this example:

* The **reset_position_client** calls the `reset_position` service and waits for the response.
* After receiving the response, it prints out the success message ("Position reset successful").

---

### **Summary of ROS 2 Code Examples**

In these examples, we demonstrated:

1. **Creating Nodes**: Nodes are the basic building blocks of a ROS 2 system. We created a simple node that logs messages periodically.
2. **Publisher-Subscriber Model (Topics)**: We created a publisher node that sends data on a topic and a subscriber node that listens to that topic and prints the data.
3. **Request-Response Model (Services)**: We created a service server that responds to requests by resetting the robot’s position and a client that calls the service to reset the position.

These examples give you a foundation for working with **communication** in ROS 2, including the core patterns for inter-node communication: **topics** for continuous data streaming and **services** for synchronous requests.

---

