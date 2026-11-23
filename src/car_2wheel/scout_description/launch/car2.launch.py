from launch import LaunchDescription
from launch_ros.actions import Node

# 封装终端指令相关
# from launch.actions import ExecuteProcess
# from launch.substitutions import FindExecutable

# 参数声明与获取
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

# 文件包含相关
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

# 分组相关
# from launc
# h_ros.actions import PushRosNamespace
# from launch.actions import GroupAction

# 事件相关
# from launch.event_handlers import OnProcessStart, OnProcessExit
# from launch.actions import RegisterEventHandler, LogInfo

# 获取功能包下share目录路径
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
import os
def generate_launch_description():
    # p_value = ParameterValue(Command(["xacro ",get_package_share_directory("cpp06_urdf") + "/urdf/urdf/demo01_helloworld.urdf"]))
    # ros2 launch cpp06_urdf display.launch.py model:=$(ros2 pkg prefix --share cpp06_urdf)/urdf/urdf/xxxx.urdf
    model = DeclareLaunchArgument(name="model",default_value=get_package_share_directory("scout_description") + "/urdf/scout_v2.xacro")
    p_value = ParameterValue(Command(["xacro ",LaunchConfiguration("model")]))
    robot_state_pub = Node(package="robot_state_publisher",
                           executable="robot_state_publisher",
                           parameters=[{"robot_description": p_value}])
    joint_state_pub = Node(package="joint_state_publisher",
                           executable="joint_state_publisher")
         
  
    return LaunchDescription([model,robot_state_pub,joint_state_pub
                            #   amcl_node,manager_localization_node,map_server_launch
                              ])