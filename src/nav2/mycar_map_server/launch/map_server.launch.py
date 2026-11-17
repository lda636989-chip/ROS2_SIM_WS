from launch import LaunchDescription
from launch_ros.actions import Node

# 封装终端指令相关
# from launch.actions import ExecuteProcess
# from launch.substitutions import FindExecutable

# 参数声明与获取
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

# 文件包含相关
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource

# 分组相关
# from launch_ros.actions import PushRosNamespace
# from launch.actions import GroupAction

# 事件相关
# from launch.event_handlers import OnProcessStart, OnProcessExit
# from launch.actions import RegisterEventHandler, LogInfo

# 获取功能包下share目录路径
from ament_index_python.packages import get_package_share_directory
import os
def generate_launch_description():
    use_sim_time = DeclareLaunchArgument("use_sim_time", default_value="true")
    map_server_node=Node(package="nav2_map_server",
                       executable="map_server",
                       name="map_server",
                       parameters=[{"yaml_filename":"map/my_map.yaml","use_sim_time":LaunchConfiguration('use_sim_time')}]
                       )
    life_manage=Node(package="nav2_lifecycle_manager",
                         executable="lifecycle_manager",
                         name="lifecycle_manager",
                         parameters=[{"use_sim_time": LaunchConfiguration('use_sim_time')},
                                     {"autostart": True},
                                     {"node_names": ["map_server"]}])
    return LaunchDescription([use_sim_time,map_server_node,life_manage])