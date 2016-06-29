# DNS

目的是学习理解dns协议

# 使用

以MacOS为例, 先开启Server

    sudo python main.py

运行nslookup命令

    ~ nslookup

修改dns目标地址

    > lserver 127.0.0.1
    Default server: 127.0.0.1
    Address: 127.0.0.1#53

查询域名

    > ly95.me


得到下面结果为正确:

    Server:		127.0.0.1
    Address:	127.0.0.1#53

    Non-authoritative answer:
    Name:	ly95.me
    Address: 127.0.0.1

# 版权

Licensed under the Apache License, Version 2.0