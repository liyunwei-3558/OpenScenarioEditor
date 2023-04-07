<!--
 * @Author: Yunwei Li 1084087910@qq.com
 * @Date: 2023-04-07 19:50:11
 * @LastEditors: Yunwei Li 1084087910@qq.com
 * @LastEditTime: 2023-04-07 20:00:43
 * @FilePath: /scripts/README.md
 * @Description: 
 * 
 * Copyright (c) 2023 by Tsinghua University, All Rights Reserved. 
-->
# OPENSCENARIO Editor
A simple example of converting a OpenSCENARIO file created by 51simone into the form that CARLA simulator can successfully parse, which contains some useful ways to edit the OpenSCENARIO file.

## How to use

```bash
python XOSC_converter.py -n <OPENSCENARIO FILE> -c <Controller>
```

for example:
```bash
python XOSC_converter.py -n ./scenarios/FLV_LT.xosc -c autoware
```