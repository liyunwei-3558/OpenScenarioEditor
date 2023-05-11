'''
Author: Yunwei Li 1084087910@qq.com
Date: 2023-04-01 16:05:16
LastEditors: Yunwei Li 1084087910@qq.com
LastEditTime: 2023-05-11 19:38:39
FilePath: /scripts/XOSC_converter.py
Description: 

Copyright (c) 2023 by Tsinghua University, All Rights Reserved. 
'''

import xml.etree.ElementTree as ET
# from utils import  *
import argparse
from xpinyin import Pinyin

def reverse_all_y_coordinates(rt):
    # ls = rt.getElementsByTagName('Position')
    # print(ls)
    for position in rt.iter(tag='Position'):
        for ele in position:
            # print(ele.attrib['y'])
            newstr = str(float(ele.attrib['y']) * (-1))
            # print(newstr, 'done')
            ele.set('y', newstr)
            
def modify_x_coordinates(rt):
    for position in rt.iter(tag='Position'):
        for ele in position:
            # print(ele.attrib['y'])
            newstr = str(float(ele.attrib['x'])+2)
            # print(newstr, 'done')
            ele.set('x', newstr)
    
def replace_Ego(fpath):
    data = None

    with open(fpath, "r", encoding='UTF-8') as f:
        data = f.read()
        data = data.replace('Ego', 'ego_vehicle')
        # # process Chinese characters
        p = Pinyin()
        for i in range(len(data)):
            c = data[i]
            if ('\u4e00' <= c <= '\u9fa5'):
                result = p.get_pinyin(c)
                data = data[:i] + result + data[i + 1:]
        
        
        # for l in f.readlines:
        #     l.replace('Ego', 'ego_vehicle')
        # f.write('rep.xml')
        f.close()
    
    with open('rep.xml','w', encoding='UTF-8') as f:
        f.write(data)

def parse_my_xml(filename):
    return ET.parse(filename).getroot()


def get_traffic_event(state, dis):
    tl = ET.parse('./myXML/traffic_light.xml').getroot()
    # ste = tl.find('.//')
    for ste_i in tl.iterfind('TrafficSignalStateAction'):
        ste_i.set('state', state)
        break
    
    for pos in tl.iterfind('WorldPosition'):
        pos.set('y', dis)
    
    return tl

argparser = argparse.ArgumentParser()
argparser.add_argument('-n',
                       '--name',
                       default='./51/try2.xosc',
                       help='Name of the OpenScenario File')

argparser.add_argument('-c',
                       '--controller',
                       default='autoware',
                       help='choose the controller of ego vehicle')
argparser.add_argument('-tl',
                       '--trafficlight',
                       default='Green',
                       help='choose the traffic light state')

argparser.add_argument('-d',
                       '--trigger_distance',
                       default='-3',
                       help='set the trigger distance of traffic light')

args = argparser.parse_args()

replace_Ego(args.name)

xml_path = 'rep.xml'
tree = ET.parse(xml_path)
root = tree.getroot()

# change the version
for child in root.findall('./FileHeader'):
    child.attrib['author'] = 'Yunwei_Li'
    child.attrib['description'] = 'description'
    child.attrib['revMajor'] = '1'
    child.attrib['revMinor'] = '0'

roadnetwork = root.find('./RoadNetwork/LogicFile')
roadnetwork.attrib['filepath'] = 'Town05'
SceneGraphFile_ = ET.Element('SceneGraphFile', {'filepath': ""})
root.find('./RoadNetwork').append(SceneGraphFile_)

entities = root.find('.//Entities')
entities.remove(entities.find("./ScenarioObject[@name='ego_vehicle']"))

# POVs
bps = ['vehicle.audi.a2']
motor_bps = ['vehicle.vespa.zx125','vehicle.kawasaki.ninja']
# bike_bps=['vehicle.diamondback.century']
people_bps = ['walker.pedestrian.000']


for pov in entities:
    try:
        for ve in pov.find('./Vehicle/..'):
            model_name = 'default_vehicle'
            ve_cate = ve.get('vehicleCategory')
            if ve_cate=='car':
                if ve.get('name')[0] =='M':
                    model_name = motor_bps[1]
                else :
                    model_name = bps[0]
            elif ve_cate == 'bicycle':
                # ve.set('name', motor_bps[0])
                model_name = motor_bps[0]
                
            ve.set('name', model_name)

            ppt = ve.find('./Properties')
            type_ = ET.Element('Property', {'name': 'type', 'value': 'simulation'})
            ppt.append(type_)
            ppt.find('./Property[@name="model"]').set('value', model_name)
    except:
        pass
    try:
        ped_cnt = 0
        for ped in pov.find('./Pedestrian/..'):
            print(ped)
            ped_cnt += 1
            ped.set('name', people_bps[0]+str(ped_cnt))
            ppt = ped.find('./Properties')
            type_ = ET.Element('Property', {'name': 'type', 'value': 'simulation'})
            ppt.append(type_)
            ppt.find('./Property[@name="model"]').set('value', people_bps[0]+str(ped_cnt))
    except:
        # print("kkkkkk")
        pass

# change the information of Ego car
# by directly replacing the information with specific file
# for ego in root.findall('./ScenarioObject[@name='Ego']')

eego = ET.parse('./myXML/Entity_EgoVehicle.xml').getroot()
entities.append(eego)

# Storyboards
# entityRef
er = root.find('./Storyboard/Init/Actions/Private[@entityRef="Ego"]')
if er:
    er.set('entityRef','ego_vehicle')

er = root.find('./Storyboard/Init/Actions/Private[@entityRef="ego_vehicle"]')
controller = None
if args.controller == 'autoware':
    controller = ET.parse('./myXML/Assign_autoware_controller.xml').getroot()
elif args.controller == 'carla_ad':
    controller = ET.parse('./myXML/Assign_carla_ad_controller.xml').getroot()
else :
    print("Unknown controller!")
er.append(controller)

ego_speed = er.find('./PrivateAction/LongitudinalAction/SpeedAction/SpeedActionTarget/AbsoluteTargetSpeed')
ego_speed.set('value', str(float(ego_speed.get('value'))*3.6))
# reverse_all_y_coordinates(tree)
# reverse_all_y_coordinates(tree)
# modify_x_coordinates(tree)

# add traffic lights' control
tl_event = get_traffic_event(args.trafficlight, args.trigger_distance)
maneuver = root.find('./Storyboard/Story/Act//Maneuver/Event/..')
maneuver[0].append(tl_event)


tree.write('./output.xosc')
