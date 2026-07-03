#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Joy
from erp42_serial2.msg import ERP_CMD
'''
buttons[4] = LB 버튼 → 전진 모드
buttons[5] = RB 버튼 → 후진 모드
axes[1]    = 전후 입력 → 속도/브레이크
axes[3]    = 좌우 입력 → 조향
'''
rospy.init_node('joy_con_erp42')

def callback(msg):
    joymsg = ERP_CMD()
    if msg.buttons[4]==1 and msg.buttons[5]==0: #LB버튼을 누르면 전진(계속누르고 있어여함.)
       joymsg.cmd_gear=0 #전진
       if msg.axes[1]>0:
         joymsg.cmd_speed = int(msg.axes[1]*5) #스피드(최대 속도 5로 테스트시 안정)
       elif msg.axes[1]<0:
          joymsg.cmd_brake = int(msg.axes[1]*(-100)) #브레이크 (0~100까지만 하지만 뒤로 하면 마이너스여서 통신 프로토콜에 맞춰 재매핑)
       joymsg.cmd_steer = int(msg.axes[3]*(-2000)) #스티어링  (실제 돌려보면서 재매핑)
          
    elif msg.buttons[4]==0 and msg.buttons[5]==1: #RB버튼을 누르면 후진.(계속누르고 있어여함.)
       joymsg.cmd_gear=2
       if msg.axes[1]>0:
         joymsg.cmd_speed = int(msg.axes[1]*50)
       elif msg.axes[1]<0:
          joymsg.cmd_brake = int(msg.axes[1]*(-100))
       joymsg.cmd_steer = int(msg.axes[3]*(-2000)) 
                 
    else :
        joymsg.cmd_gear = 1; joymsg.cmd_speed = 0; joymsg.cmd_steer = 0; #아무것도 안잡히면 기어 중립, 스티어링 중간, 스피드 0
     
    print("gear : %d / speed : %d / steer : %d / brake : %d" %(joymsg.cmd_gear, joymsg.cmd_speed, joymsg.cmd_steer, joymsg.cmd_brake))
    pub.publish(joymsg)
    
sub = rospy.Subscriber('joy', Joy, callback) #JOY노드에서 값이 들어오면
pub = rospy.Publisher('erp42_cmd', ERP_CMD, queue_size=100) #erp42_cmd에 pub

rospy.spin()
