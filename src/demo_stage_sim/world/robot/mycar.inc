include "robot/car_base.inc"
include "robot/laser.inc"
include "robot/camera.inc"

define mycar car_base(
        my_camera(pose [0.15 0.0 0.0 0.0])
        my_laser()
)