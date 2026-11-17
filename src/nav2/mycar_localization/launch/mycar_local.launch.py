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
# from launch_ros.actions import PushRosNamespace
# from launch.actions import GroupAction

# 事件相关
# from launch.event_handlers import OnProcessStart, OnProcessExit
# from launch.actions import RegisterEventHandler, LogInfo

# 获取功能包下share目录路径
from ament_index_python.packages import get_package_share_directory
import os
def generate_launch_description():
    use_sim_time=DeclareLaunchArgument("use_sim_time",default_value="true")
    map_file=os.path.join(get_package_share_directory("demo_stage_sim"),"launch","sim.launch.py")
    amcl_yaml = os.path.join(get_package_share_directory("mycar_localization"),
             'params', 'amcl.yaml')
    world_launch=IncludeLaunchDescription(
        launch_description_source=PythonLaunchDescriptionSource(
            launch_file_path=map_file
        ))
    map_server_launch=IncludeLaunchDescription(
        launch_description_source=PythonLaunchDescriptionSource(
            launch_file_path=os.path.join(get_package_share_directory("mycar_map_server"),"launch","map_server.launch.py"))
        )
    
    amcl_node = Node(
             package='nav2_amcl',
             executable='amcl',
             name='amcl',
             parameters=[amcl_yaml,
                         {'use_sim_time': LaunchConfiguration('use_sim_time')}]
         )
    life_manage=Node(package="nav2_lifecycle_manager",
                             executable="lifecycle_manager",
                             name="lifecycle_manager_amcl",
                             parameters=[{"use_sim_time": LaunchConfiguration('use_sim_time')},
                                         {"autostart": True},
                                         {"node_names": ["amcl"]}])
    return LaunchDescription([use_sim_time,world_launch,map_server_launch,amcl_node,life_manage])