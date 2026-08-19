import math
import os
import socket

import numpy as np
import pandas as pd

from common import *


# NameNode功能
# 1. 保存文件的块存放位置信息
# 2. ls ： 获取文件/目录信息
# 3. get_fat_item： 获取文件的FAT表项
# 4. new_fat_item： 根据文件大小创建FAT表项
# 5. rm_fat_item： 删除一个FAT表项
# 6. mkdir/mv: 创建目录、移动或重命名NameNode元数据
# 7. heartbeat/report_blocks: 检测DataNode状态并辅助副本修复
# 8. format: 删除所有FAT表项

class NameNode:
    def run(self):  # 启动NameNode
        # 创建一个监听的socket
        listen_fd = socket.socket()
        try:
            # 监听端口
            listen_fd.bind(("0.0.0.0", NAME_NODE_PORT))
            listen_fd.listen(5)
            print("Name node start")
            while True:
                # 等待连接，连接后返回通信用的套接字
                sock_fd, addr = listen_fd.accept()
                print("connected by {}".format(addr))
                
                try:
                    # 获取请求方发送的指令
                    request = str(sock_fd.recv(128), encoding='utf-8')
                    request = request.split()  # 指令之间使用空白符分割
                    print("Request: {}".format(request))
                    
                    cmd = request[0]  # 指令第一个为指令类型
                    
                    if cmd == "ls":  # 若指令类型为ls, 则返回DFS上对于文件、文件夹的内容
                        dfs_path = request[1]  # 指令第二个参数为DFS目标地址
                        response = self.ls(dfs_path)
                    elif cmd == "mkdir":  # 创建DFS目录，只修改NameNode元数据
                        dfs_path = request[1]
                        response = self.mkdir(dfs_path)
                    elif cmd == "mv":  # 移动或重命名DFS路径，只修改NameNode元数据
                        src_path = request[1]
                        dst_path = request[2]
                        response = self.mv(src_path, dst_path)
                    elif cmd == "get_fat_item":  # 指令类型为获取FAT表项
                        dfs_path = request[1]  # 指令第二个参数为DFS目标地址
                        response = self.get_fat_item(dfs_path)
                    elif cmd == "new_fat_item":  # 指令类型为新建FAT表项
                        dfs_path = request[1]  # 指令第二个参数为DFS目标地址
                        file_size = int(request[2])
                        response = self.new_fat_item(dfs_path, file_size)
                    elif cmd == "rm_fat_item":  # 指令类型为删除FAT表项
                        dfs_path = request[1]  # 指令第二个参数为DFS目标地址
                        response = self.rm_fat_item(dfs_path)
                    elif cmd == "format":
                        response = self.format()
                    elif cmd == "heartbeat":
                        host_name = request[1]
                        response = self.heartbeat(host_name)
                    elif cmd == "report_blocks":
                        host_name = request[1]
                        response = self.report_blocks(host_name)
                    else:  # 其他位置指令
                        response = "Undefined command: " + " ".join(request)
                    
                    print("Response: {}".format(response))
                    sock_fd.send(bytes(response, encoding='utf-8'))
                except KeyboardInterrupt:  # 如果运行时按Ctrl+C则退出程序
                    break
                except Exception as e:  # 如果出错则打印错误信息
                    print(e)
                finally:
                    sock_fd.close()  # 释放连接
        except KeyboardInterrupt:  # 如果运行时按Ctrl+C则退出程序
            pass
        except Exception as e:  # 如果出错则打印错误信息
            print(e)
        finally:
            listen_fd.close()  # 释放连接
    
    def ls(self, dfs_path):
        local_path = os.path.join(NAME_NODE_DIR, dfs_path)
        # 如果不存在，返回错误信息
        if not os.path.exists(local_path):
            return "No such file or directory: {}".format(dfs_path)
        
        if os.path.isdir(local_path):
            # 如果目标地址是一个文件夹，则显示该文件夹下内容
            dirs = os.listdir(local_path)
            response = " ".join(dirs)
        else:
            # 如果目标是文件则显示文件的FAT表信息
            with open(local_path) as f:
                response = f.read()
        
        return response
    
    def get_fat_item(self, dfs_path):
        # 获取FAT表内容
        local_path = os.path.join(NAME_NODE_DIR, dfs_path)
        response = pd.read_csv(local_path)
        return response.to_csv(index=False)

    def mkdir(self, dfs_path):
        local_path = os.path.join(NAME_NODE_DIR, dfs_path)
        # TODO: 创建NameNode目录；注意处理目录已存在、父目录不存在等情况
        return "TODO: mkdir {}".format(local_path)

    def mv(self, src_path, dst_path):
        src_local_path = os.path.join(NAME_NODE_DIR, src_path)
        dst_local_path = os.path.join(NAME_NODE_DIR, dst_path)
        # TODO: 移动或重命名NameNode中的目录/FAT表文件
        # 可接受方案：只移动NameNode元数据，不重命名DataNode中的块文件。
        return "TODO: mv {} {}".format(src_local_path, dst_local_path)
    
    def new_fat_item(self, dfs_path, file_size):
        nb_blks = int(math.ceil(file_size / DFS_BLK_SIZE))
        print(file_size, nb_blks)
        
        # TODO: 多副本实现时，每个blk_no应选择DFS_REPLICATION个不同host，
        # 并在FAT表中写入多行，例如同一个blk_no对应3个host_name。
        data_pd = pd.DataFrame(columns=['blk_no', 'host_name', 'blk_size'])

        for i in range(nb_blks):
            blk_no = i
            host_name = np.random.choice(HOST_LIST, size=DFS_REPLICATION, replace=False)[0]
            blk_size = min(DFS_BLK_SIZE, file_size - i * DFS_BLK_SIZE)
            data_pd.loc[i] = [blk_no, host_name, blk_size]
        
        # 获取本地路径
        local_path = os.path.join(NAME_NODE_DIR, dfs_path)
        # 若目录不存在则创建新目录
        os.system("mkdir -p {}".format(os.path.dirname(local_path)))
        # 保存FAT表为CSV文件
        data_pd.to_csv(local_path, index=False)
        # 同时返回CSV内容到请求节点
        return data_pd.to_csv(index=False)
    
    def rm_fat_item(self, dfs_path):
        local_path = NAME_NODE_DIR + dfs_path
        response = pd.read_csv(local_path)
        os.remove(local_path)
        return response.to_csv(index=False)
    
    def format(self):
        format_command = "rm -rf {}/*".format(NAME_NODE_DIR)
        os.system(format_command)
        return "Format namenode successfully~"

    def heartbeat(self, host_name):
        # TODO: 记录host_name最近一次心跳时间，供monitor_datanodes判断节点是否失联
        return "alive {}".format(host_name)

    def report_blocks(self, host_name):
        # TODO: 接收或拉取DataNode的块列表，用于节点失联后的副本修复
        return "TODO: report_blocks {}".format(host_name)

    def monitor_datanodes(self):
        # TODO: 周期性检查每个DataNode最后心跳时间。
        # 若当前时间 - 最后心跳时间 > HEARTBEAT_TIMEOUT，则调用handle_dead_datanode。
        pass

    def handle_dead_datanode(self, host_name):
        # TODO: 找出FAT表中所有host_name上的副本，并对受影响的block触发repair_replication。
        pass

    def repair_replication(self, dfs_path_or_blk):
        # TODO: 自动补副本推荐流程：
        # 1. 从FAT中找到该block仍存活的副本；
        # 2. 读取存活副本数据；
        # 3. 选择不含该block且仍存活的新DataNode；
        # 4. 将数据发送到新DataNode；
        # 5. 更新FAT表，使副本数恢复到DFS_REPLICATION。
        pass


# 创建NameNode并启动
name_node = NameNode()
name_node.run()

