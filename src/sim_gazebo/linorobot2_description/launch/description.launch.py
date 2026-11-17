# Copyright (c) 2021 Juan Miguel Jimeno
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# import os
# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution, EnvironmentVariable
# from launch.conditions import IfCondition
# from launch_ros.actions import Node
# from launch_ros.substitutions import FindPackageShare


# def generate_launch_description():
#     robot_base = os.getenv('LINOROBOT2_BASE')
    
#     urdf_path = PathJoinSubstitution(
#         [FindPackageShare("linorobot2_description"), "urdf/robots", f"{robot_base}.urdf.xacro"]
#     )

#     rviz_config_path = PathJoinSubstitution(
#         [FindPackageShare('linorobot2_description'), 'rviz', 'description.rviz']
#     )

#     return LaunchDescription([
#         DeclareLaunchArgument(
#             name='urdf', 
#             default_value=urdf_path,
#             description='URDF path'
#         ),
        
#         DeclareLaunchArgument(
#             name='publish_joints', 
#             default_value='true',
#             description='Launch joint_states_publisher'
#         ),

#         DeclareLaunchArgument(
#             name='rviz', 
#             default_value='false',
#             description='Run rviz'
#         ),

#         DeclareLaunchArgument(
#             name='use_sim_time', 
#             default_value='false',
#             description='Use simulation time'
#         ),

#         Node(
#             package='joint_state_publisher',
#             executable='joint_state_publisher',
#             name='joint_state_publisher',
#             condition=IfCondition(LaunchConfiguration("publish_joints")),
#             parameters=[
#                 {'use_sim_time': LaunchConfiguration('use_sim_time')}
#             ]
#         ),

#         Node(
#             package='robot_state_publisher',
#             executable='robot_state_publisher',
#             name='robot_state_publisher',
#             output='screen',
#             parameters=[
#                 {
#                     'use_sim_time': LaunchConfiguration('use_sim_time'),
#                     'robot_description': Command(['xacro ', LaunchConfiguration('urdf')])
#                 }
#             ]
#         ),

#         Node(
#             package='rviz2',
#             executable='rviz2',
#             name='rviz2',
#             arguments=['-d', rviz_config_path],
#             condition=IfCondition(LaunchConfiguration("rviz")),
#             parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
#         )
#     ])

from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command,LaunchConfiguration
from launch.actions import DeclareLaunchArgument

#示例： ros2 launch cpp06_urdf display.launch.py model:=`ros2 pkg prefix --share cpp06_urdf`/urdf/urdf/demo01_helloworld.urdf
def generate_launch_description():

    MYCAR_MODEL = os.environ['MYCAR_MODEL']

    mycar_description = get_package_share_directory("linorobot2_description")
    default_model_path = os.path.join(mycar_description,"urdf/robots",MYCAR_MODEL + ".urdf.xacro")
    model = DeclareLaunchArgument(name="model", default_value=default_model_path)

    # 加载机器人模型
    # 启动 robot_state_publisher 节点并以参数方式加载 urdf 文件
    robot_description = ParameterValue(Command(["xacro ",LaunchConfiguration("model")]))
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )
    rviz2 = Node(package="rviz2",executable="rviz2",
                 arguments=["-d",get_package_share_directory("linorobot2_description") + "/rviz/sim.rviz"])
    return LaunchDescription([
        model,
        robot_state_publisher,
        rviz2
    ])