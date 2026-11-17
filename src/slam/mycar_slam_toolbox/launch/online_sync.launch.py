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
    yaml_path=os.path.join(get_package_share_directory("mycar_slam_toolbox"),"params","online_sync.yaml")
    slam_node=Node(package="slam_toolbox",
                   executable="sync_slam_toolbox_node",
                   name="my_slam_toolbox",
                   parameters=[yaml_path, {
                       "use_sim_time": LaunchConfiguration("use_sim_time")
                   }]
                   )
    life_manage=Node(package="nav2_lifecycle_manager",
                     executable="lifecycle_manager",
                     name="lifecycle_manager_slam",
                     parameters=[{"use_sim_time": LaunchConfiguration('use_sim_time')},
                                 {"autostart": True},
                                 {"bond_timeout": 0.0},
                                 {"node_names": ["my_slam_toolbox"]}])
    return LaunchDescription([use_sim_time,slam_node,life_manage])
