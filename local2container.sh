#!/usr/bin/env bash
###
 # @Author: Yunwei Li 1084087910@qq.com
 # @Date: 2023-05-11 19:41:37
 # @LastEditors: Yunwei Li 1084087910@qq.com
 # @LastEditTime: 2023-05-11 19:45:05
 # @FilePath: /scripts/local2container.sh
 # @Description: 
 # 
 # Copyright (c) 2023 by Tsinghua University, All Rights Reserved. 
### 
docker cp output.xosc CIIP_container:/home/autoware/XOSCfiles/$1.xosc
