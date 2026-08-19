DFS_REPLICATION = 1  # 本地调试可设为1；多机实验请设为3
DFS_BLK_SIZE = 4096  # 数据块大小

# NameNode和DataNode数据存放位置
NAME_NODE_DIR = "./dfs/name/"
DATA_NODE_DIR = "./dfs/data/"

NAME_NODE_PORT = 21009  # NameNode监听端口
DATA_NODE_PORT = 11009  # DataNode程序监听端口

# 建议使用学号后四位作为端口号，避免端口冲突
HEARTBEAT_INTERVAL = 2  # NameNode/DataNode心跳间隔，单位：秒
HEARTBEAT_TIMEOUT = 6   # 超过该时间未收到心跳则判定DataNode失联

# 集群中的主机列表
HOST_LIST = ['localhost']
# 集群一4节点示例：HOST_LIST = ['thumm01', 'thumm03', 'thumm04', 'thumm07']
# 集群二4节点示例：HOST_LIST = ['thumm01', 'thumm02', 'thumm03', 'thumm04']
# 多机实验中建议设置：DFS_REPLICATION = 3
NAME_NODE_HOST = 'localhost'

BUF_SIZE = DFS_BLK_SIZE * 2
