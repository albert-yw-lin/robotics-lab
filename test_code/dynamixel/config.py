### DO NOT MODIFY THIS SECTION
MY_DXL = 'X_SERIES'
PROTOCOL_VERSION            = 2.0
DXL_ID                      = [0, 1, 2, 3, 4, 5]
ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_MAX_POSITION_LIMIT     = 48
ADDR_MIN_POSITION_LIMIT     = 52
ADDR_PROFILE_ACCELERATION   = 108
ADDR_PROFILE_VELOCITY       = 112
ADDR_MOVING_THRESHOLD       = 24
LEN_GOAL_POSITION           = 4         # Data Byte Length
# DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
# DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
ADDR_PRESENT_POSITION       = 132
LEN_PRESENT_POSITION        = 4         # Data Byte Length
BAUDRATE                    = 57600
TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque

### can modify if necessary (CAREFULLY)
DEVICENAME                  = '/dev/ttyUSB0'
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold
POS_LIMIT = [[0,4095],
             [0,4095],
             [0,4095],
             [0,4095],
             [0,4095],
             [0,4095]]
PROFILE_ACCELERATION = 25
PROFILE_VELOCITY = 50
MOVING_THRESHOLD = 20