# 实验一 Linux基础实验

<img src="./assets/sudo.png" alt="sudo" style="zoom:60%;" />

## 一、实验目标

* 实验主体满分 **5 分**，外加 **2 分 Bonus**。本实验旨在为后续 MapReduce / Spark 实验打下基础，包括以下 4 项核心能力：

  - 掌握 SSH 远程登录与免密登录配置（1 分）
  - 掌握 Linux 文件/目录操作以及文本处理命令的组合使用（0.5 分）
  - 理解阻塞/非阻塞执行，并掌握进程与系统资源的基本管理（1.5 分）
  - 掌握 shell 脚本基础语法，能够编写脚本来组织、运行并验证相关任务（2 分）

* Bonus：在多节点上完成"切分→分发→远程执行→回收→汇总"的完整流水线（2 分）。

## 二、实验任务与要求

下面是本次实验四个核心任务，详细要求与评分点见第三节。请同学们按顺序完成。

* **核心任务一：SSH 远程登录与免密配置**

  - 使用 `ssh` 登录课程服务器；
  - 使用 `ssh-keygen` / `ssh-copy-id` 配置本机到服务器的免密登录。

* **核心任务二：文件/目录与文本处理常用命令**

  - 掌握 `pwd / mkdir / cd / ls / cp / mv / rm / vim`；
  - 掌握 `cat / head / tail / scp / awk / grep / 重定向`；
  - 掌握 `sort / uniq / wc / cut / tr / xargs`，能够使用**一行管道**完成 word count。

* **核心任务三：阻塞/非阻塞、进程与资源管理**

  - 用稳定的工作负载对比阻塞 vs 非阻塞脚本的 real / user / sys 时间；
  - 掌握 `ps / top / kill / nohup / jobs / fg / bg / free / df / du / lsof`，能够定位并清理"端口被占用"等常见问题。

* **核心任务四：shell 脚本基础**

  - 掌握变量、数组、`for / if / while`、函数与退出码 `$?`；
  - 编写 `start_all.sh / stop_all.sh`，使用 `ssh` 在多个节点上批量启动、检验并停止一个示例进程。

* **Bonus：多节点协同处理流水线**

  - 配置集群中**多主机**的免密登录；
  - 按"切片→分发→远程执行→回收→汇总"5 步实现多节点词频统计，对比单节点与多节点处理时间，并分析加速比与瓶颈。

* 服务器介绍

  - 课程共有两个服务器集群，可由本地ssh连接（需连接网络tsinghua或使用VPN），登录thumm01后，使用命令`ssh thumm0x`可以跳转至其他主机。服务器资源有限，请勿用于课程无关任务。

  - 集群一：ip地址： 10.103.9.11 ，可用机器：01，02，03，04。登录集群一01的命令： ssh [xxx@10.103.9.11](mailto:xxx@10.103.9.11) （也就是和以下实验指导书的内容完全相同）

  - 集群二：ip地址： 10.103.10.156 ，可用机器：01-04。 登录集群二01的命令： ssh [xxx@10.103.10.156](mailto:xxx@10.103.10.156) -p 8001 (由于进入该集群的端口并非默认端口，所以在 ssh 指令后面一定要用 -p 要加上端口号！) 


* 本地SSH客户端的选择
  
  - 本课程使用Secure Shell(SSH)协议连接远程服务器。MacOS, Linux用户可以使用Terminal, Windows用户可以下载[MobaXterm](https://mobaxterm.mobatek.net/)、[XShell](https://www.netsarang.com/en/free-for-home-school/)等软件。考虑到后续实验，我们推荐在[VSCode](https://code.visualstudio.com/docs/remote/ssh)、[PyCharm](https://www.jetbrains.com/help/pycharm/remote-development-starting-page.html)等IDE中部署远程连接，方便代码编写与调试。

* 报告提交要求

  * 将命令、关键代码（文本）、结果截图放入报告，实验报告需为pdf 格式，连同代码文件一同打包成压缩文件（命名为`学号_姓名_实验一.*`，例如：`2021200000_张三_实验一.zip`），最后提交到网络学堂。压缩文件中文件目录应为：

    ```shell
    .
    └── 学号_姓名_实验一.pdf # 实验报告
    └── code # 代码文件夹
        └── code_file1
        └── code_file2
        └── ...
    ```


  * 迟交作业一周以内，以50% 比例计分；一周以上不再计分。一经发现抄袭情况（包括往届），零分处理。

## 三、Linux常用命令

### 任务1. 使用ssh远程登录服务器 （0.5 分）

课程服务器的地址是**10.103.9.11**，使用`ssh student_id@10.103.9.11`命令即可登录服务器，其中student_id替换为学号，密码也是学号。

```shell
$ ssh 2019211199@10.103.9.11
2019211199@10.103.9.11's password:
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.12.9-041209-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

2019211199@thumm01:~$
```

### 任务2. 配置免密登录 （0.5 分）

服务器每次登录都需要输入密码, 对此我们可以配置免密登录，原理是将本地主机的公钥保存在服务器，每次登录时主机和服务器通过公钥验证身份，因此不再需要输入密码。

#### 生成公钥和私钥

使用ssh-keygen在个人机器上生成公钥和私钥，存放的位置一般不需要改。

```shell
szxie at ubuntu:~$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/dsjxtjc/2019211199/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/dsjxtjc/2019211199/.ssh/id_rsa.
Your public key has been saved in /home/dsjxtjc/2019211199/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:pDlFzmQA+bFtVlcSwH3hqMT9Du/qjs7rMu7eXb9yZls 2019211199@thumm01
The key's randomart image is:
+---[RSA 2048]----+
|    .o..+..oooo. |
|    . .* .o.o+.  |
|     . +=.o.o..  |
|      o=+. . .   |
|      +oS . . .  |
|       .     +   |
|              + E|
|        oo o + =.|
|       ++=B+=.*o+|
+----[SHA256]-----+
```

#### 将公钥内容复制到服务器

使用ssh-copy-id命令将本地的公钥（localhost:\~/.ssh/id_rsa.pub）添加到远程服务器的认证列表（server:\~/.ssh/authorized_keys）。

```shell
szxie at ubuntu$ ssh-copy-id -i ~/.ssh/id_rsa.pub 2019211199@thumm01
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/dsjxtjc/2019211199/.ssh/id_rsa.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
2019211199@thumm01's password:

Number of key(s) added:        1

Now try logging into the machine, with:   "ssh '2019211199@thumm01'"
and check to make sure that only the key(s) you wanted were added.
```

Windows用户可能找不到`ssh-copy-id`命令，此时需要手动拷贝本地公钥文件到服务器中

* 在执行`ssh-keygen`命令后得到公钥存放地址，比如给出的示例为`Enter file in which to save the key (/home/dsjxtjc/2019211199/.ssh/id_rsa):`
* 登录服务器后，执行命令`mkdir ~/.ssh`，新建.ssh文件夹
* 使用scp命令将本地公钥发送至服务器，`scp <key_path> student_id@10.103.9.11:~/.ssh/authorized_keys`

如果server:~/.ssh/authorized_keys文件已经存在，也可以手动把本地公钥内容粘贴到服务器该文件内

### 任务3. 文件/目录与文本处理常用命令 （0.5 分）

> 本任务覆盖 `pwd / mkdir / cd`、`cp / vim / ls / mv / rm`、`cat / head / tail / scp / awk / grep / 重定向`、`sort / uniq / wc / cut / tr / xargs` 共 3 组命令。本任务下方有 3 个子小节，请通读示例并把要求的截图都放入报告。**不要求一一截图**——只需要在每个子小节末尾给出 1 张能体现该小节命令组合使用的截图即可。

#### 3.1 目录与文件基本操作（`pwd / mkdir / cd / ls / cp / vim / mv / rm`）

查看当前目录

```shell
2019211199@thumm01:~$ pwd
/home/dsjxtjc/2019211199
```

创建新目录

```shell
2019211199@thumm01:~$ mkdir dir_name
2019211199@thumm01:~$ ls
dir_name
```

进入新目录

```shell
2019211199@thumm01:~$ cd dir_name
2019211199@thumm01:~/dir_name$ pwd
/home/dsjxtjc/2019211199/dir_name
```

退出回到上级目录

```shell
2019211199@thumm01:~/dir_name$ cd ..
2019211199@thumm01:~$ pwd
/home/dsjxtjc/2019211199
```

#### 3.2 文件读写与查看（`vim / cat / cp / mv / rm / ls -l`）

使用vim创建一个文件file.txt，**在命令模式下输入i 切换到插入模式**，输入内容‘hello world’，**按ESC返回命令模式**，输入:wq保存并退出。

```shell
2019211199@thumm01:~$ vim file.txt
2019211199@thumm01:~$ ls
dir_name  file.txt
```

查看文件内容

```shell
2019211199@thumm01:~$ cat file.txt
helloworld
```

拷贝文件file.txt, 生成新的文件new_file.txt

```shell
2019211199@thumm01:~$ cp file.txt new_file.txt
2019211199@thumm01:~$ ls
dir_name  file.txt  new_file.txt
```

给新文件重命名

```shell
2019211199@thumm01:~$ mv new_file.txt new_file_renamed.txt
2019211199@thumm01:~$ ls
dir_name  file.txt  new_file_renamed.txt
```

删除file.txt

```shell
2019211199@thumm01:~$ rm file.txt
2019211199@thumm01:~$ ls
dir_name  new_file_renamed.txt
```

查看文件详细信息

```shell
2019211199@thumm01:~$ ls -l
total 8
drwxr-xr-x 2 2019211199 dsjxtjc 4096 Sep 20 16:02 dir_name
-rw-r--r-- 1 2019211199 dsjxtjc   11 Sep 20 16:12 new_file_renamed.txt
```

#### 3.3 文本处理与组合管道（`head / tail / scp / awk / grep / sort / uniq / wc / cut / tr / xargs`）

拷贝数据集wc_dataset.txt（约13MB）到用户目录下

```shell
2019211199@thumm01:~$ cp /home/dsjxtjc/wc_dataset.txt ./
2019211199@thumm01:~$ ls
dir_name  new_file_renamed.txt	wc_dataset.txt
```

wc_dataset是一个包含2683500个单词的大数据集，每个单词占据一行。使用指令对该数据集进行操作。

#### head、tail命令

head/tail用于查看文件头部/尾部的内容，默认最多显示十行

```shell
2019211199@thumm01:~$ head wc_dataset.txt
chapter
i
down
the
rabbit
hole
alice
was
beginning
to
2019211199@thumm01:~$
```

也可以通过添加参数-n来设定显示的行数

```shell
2019211199@thumm01:~$ head -n 5 wc_dataset.txt
chapter
i
down
the
rabbit
2019211199@thumm01:~$
```

head和tail可以结合，可以查看文件中任意几行的内容。例如我们要查看wc_dataset.txt中6-10行，可以这样做

```shell
2019211199@thumm01:~$ head -n 10 wc_dataset.txt | tail -n 5
hole
alice
was
beginning
to
2019211199@thumm01:~$
```

#### 重定向符'>'的使用

重定向符可以将指令执行的结果重新定向，可以将原本在控制台输出的内容输出到文件。

将wc_dataset.txt中1-5行内容保存为文件wc_1-5.txt, 将6-10行保存为wc_6-10.txt。

```shell
2019211199@thumm01:~$ head -n 5 wc_dataset.txt > wc_1-5.txt
2019211199@thumm01:~$ head -n 10 wc_dataset.txt | tail -n 5 > wc_6-10.txt
2019211199@thumm01:~$ ls
dir_name  new_file_renamed.txt	wc_1-5.txt  wc_6-10.txt  wc_dataset.txt
```

使用了重定向符，原先的结果输出不见了，同时可以看到多了wc_1-5.txt和wc_6-10.txt两个文件，指令的输出结果被保存在了文件中。

#### cat命令

查看两文件的内容

```shell
2019211199@thumm01:~$ cat wc_1-5.txt
chapter
i
down
the
rabbit
2019211199@thumm01:~$ cat wc_6-10.txt
hole
alice
was
beginning
to
```

`cat wc_1-5.txt wc_6-10.txt > wc_1-10.txt`相当于合并两文件内容并保存。

```shell
2019211199@thumm01:~$ cat wc_1-5.txt wc_6-10.txt > wc_1-10.txt
2019211199@thumm01:~$ cat wc_1-10.txt
chapter
i
down
the
rabbit
hole
alice
was
beginning
to
```

#### scp命令

scp命令用来在不同主机之间传输文件，它使用的是SSH协议。

这里需要开启两个终端来查看结果，分别连接上thumm01, thumm02。需要注意的是，thumm02节点未提供外网地址，需要先登录thumm01，使用命令`ssh thumm02`跳转。

在thumm01上

```shell
2019211199@thumm01:~$ ls
dir_name  new_file_renamed.txt	wc_1-10.txt  wc_1-5.txt  wc_6-10.txt  wc_dataset.txt
2019211199@thumm01:~$
```

在thumm02上

```shell
2019211199@thumm02:~$ ls
2019211199@thumm02:~$
```

将thumm01中的wc_1-10.txt传到thumm02，其中`~/`代表用户目录

在thumm01上

```shell
2019211199@thumm01:~$ scp wc_1-10.txt thumm02:~/
2019211199@thumm02's password:
wc_1-10.txt                      100%   54     0.1KB/s   00:00
```

在thumm02上多出wc_1-10.txt

```shell
2019211199@thumm02:~$ ls
wc_1-10.txt
```

#### awk命令

awk是一个强大的文本分析工具，我们仅介绍一些常用功能。

基本用法
```shell
awk [选项参数] 'script' var=value file(s)
或
awk [选项参数] -f scriptfile var=value file(s)
```

awk指令适合处理格式规整的数据，例如`/etc/passwd`文件，它保存着Linux系统中用户的用户名以及其他信息（不包含密码），我们可以通过它了解当前主机上的用户信息。下面以"统计服务器上学号以某个年份开头的账号"为例演示`awk`的用法。示例里用的是`^2026`，请把它换成你自己的入学年份前缀。

要处理数据，我们首先要分析一下数据的格式

```shell
2019211199@thumm01:~$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
......
2026214323:x:1372:502::/home/dsjxtjc/2026214323:/bin/bash
2026280795:x:1373:502::/home/dsjxtjc/2026280795:/bin/bash
```

我们可以看到，数据每一行代表一个用户，开头为用户的用户名，后面为用户信息（具体代表什么不用管），每个信息使用`:`隔开。对此，我们可以依据冒号进行分割，然后取每行第一个元素（用户名），使用正则表达式匹配下看用户名是否为2026开头，如果是则输出。

要实现这个功能，我们可以使用下面的指令

```shell
2019211199@thumm01:~$ awk -F: '$1~"^2026"{print $1}' /etc/passwd
2026210991
2026211018
......
2026214484
```

其中-F:参数表示使用`:`作为分隔符进行分割，\$1~"^2026"{print \$1}中\$1表示分割后第一个元素（用户名），"\^2026"是一个正则表达式，表示以2026开头，`~`表示匹配，所以\$1\~"^2026"表示分割后第一个元素满足2026开头，那么就执行后面的指令{print \$1}。

再用`wc -l`统计一下有多少个这样的学号。

```shell
2019211199@thumm01:~$ awk -F: '$1~"^2026"{print $1}' /etc/passwd | wc -l
xx
```

请把你自己实际得到的数字写进报告。注意这个数字只反映**当前这台服务器上还保留着的账号数量**：往届账号会被陆续清理，不同节点上的账号也可能不完全一致，因此它并不等于本课程的选课人数。你可以换几个年份前缀（例如 `^2021`、`^2024`）对比一下，观察往届账号的留存情况。

####  grep命令

> grep命令用于查找文件里符合条件的字符串。如果发现某文件的内容符合所指定的范本样式，预设 grep 指令会把含有范本样式的那一列显示出来。若不指定任何文件名称，或是所给予的文件名为-，则 grep 指令会从标准输入设备读取数据。

接下来我们使用grep命令对wc_dataset.txt作分析

1. 显示以"dis"开头的单词（显示前10条）

```shell
2019211199@thumm01:~$ grep "^dis" wc_dataset.txt |head
disappointment
distance
disagree
distance
distance
distance
distant
dish
dishes
disgust
```

2. 反向过滤，添加参数-v。

查找wc_1-10.txt中以t字母开头的单词：

```shell
2019211199@thumm01:~$ grep "^t" wc_1-10.txt
the
to
```

接着添加参数-v，过滤掉以t开头的单词。

```shell
2019211199@thumm01:~$ grep -v "^t" wc_1-10.txt
chapter
i
down
rabbit
hole
alice
was
beginning
```

##### 组合管道：纯 shell 实现 word count（本任务的硬性提交点）

为了方便同学深入理解linux的管道命令，我们下面再补充几个常用文本处理命令：

* `sort`: 排序。`-n`按数值排序，`-r`逆序，`-k`按某一列排序。
* `uniq`: 对相邻重复行做去重；`uniq -c`统计相邻相同行的出现次数（因此通常先 `sort` 再 `uniq -c`）。
* `wc`: 统计行/词/字节数。`-l`只统计行数。
* `cut`: 按列截取文本。例如 `cut -d',' -f1` 按逗号分列后取第 1 列。
* `tr`: 字符替换/删除。例如 `tr 'A-Z' 'a-z'` 把大写转小写，`tr -s ' ' '\n'` 把多个空格压缩并转换为换行。
* `xargs`: 把上一步的输出转成下一条命令的参数。

请使用上述命令组合完成下面的任务，要求**只用一行管道**：

1. 对 `wc_dataset.txt` 统计 Top-10 高频词，每行格式为"次数 单词"，按次数从大到小排序；
2. **必须在报告中给出命令和前 10 行的结果截图**（这是本任务 0.5 分的核心提交点）。

参考管道：

```shell
2019211199@thumm01:~$ cat wc_dataset.txt | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn | head -n 10
```

进一步思考：如果数据集有 1GB，上面这条管道的瓶颈在哪一步？为什么一些先进的word count算法/工具（MapReduce、Spark）会引入"分而治之"？请在报告中用 1–2 句话给出你的判断。

### 任务4. 阻塞与非阻塞时间对比 （0.5 分）

在Linux shell脚本中，指令是顺序执行的，但实际上没有相互依赖（或者说数据关联）的指令可以并行地运行而对结果没有影响。为了让同一个脚本中没有相互依赖的指令并行地执行，我们需要指定这些指令为非阻塞。

让指令不阻塞的方法是在指令最后加上'&'。

接下来边写两个脚本，第一个脚本使用阻塞的方法执行，第二个脚本使用非阻塞的方法执行，对比两个脚本的运行时间。

> **提示**：上一版本使用 `awk '$1~"^chapter"{}'` 作为负载，单次耗时极短（百毫秒级），结果不稳定。本版改为更具计算量、更稳定的"排序 + 去重 + 再排序"管道，5 次串行约 5–10 秒，便于在 4 核机上观察 4× 左右的加速。

为了让计算量更接近"真实数据处理"，建议先把数据集放大若干倍：

```shell
2019211199@thumm01:~$ for i in $(seq 1 5); do cat wc_dataset.txt; done > wc_big.txt
2019211199@thumm01:~$ wc -l wc_big.txt
```

脚本一: shell_blocked.sh

```shell
#!/bin/bash
sort wc_big.txt | uniq -c | sort -rn > /dev/null
sort wc_big.txt | uniq -c | sort -rn > /dev/null
sort wc_big.txt | uniq -c | sort -rn > /dev/null
sort wc_big.txt | uniq -c | sort -rn > /dev/null
sort wc_big.txt | uniq -c | sort -rn > /dev/null
```

脚本二：shell_unblocked.sh

```shell
#!/bin/bash
sort wc_big.txt | uniq -c | sort -rn > /dev/null &
sort wc_big.txt | uniq -c | sort -rn > /dev/null &
sort wc_big.txt | uniq -c | sort -rn > /dev/null &
sort wc_big.txt | uniq -c | sort -rn > /dev/null &
sort wc_big.txt | uniq -c | sort -rn > /dev/null &
wait
```

运行这两个脚本，对比它们运行的时间

```shell
2019211199@thumm01:~$ vim shell_blocked.sh
2019211199@thumm01:~$ vim shell_unblocked.sh
2019211199@thumm01:~$ time bash ./shell_blocked.sh

real    0m8.6xxs
user    0m8.5xxs
sys     0m0.0xxs

2019211199@thumm01:~$ time bash ./shell_unblocked.sh

real    0m2.3xxs
user    0m8.7xxs
sys     0m0.0xxs
```

具体数值会因机器负载略有波动。可以看到 user time 基本不变（仍是 5 次任务的 CPU 总时长），但 real time 在非阻塞版本下降到约 1/4，因为 4 核机上 5 个任务被并行调度。请同学们在报告中给出自己的运行结果，并解释 user / real / sys 三者的差别。

（用户时间user time是指程序在多个核上运行时间的和，真实时间real time是现实中程序运行过去了多长时间，真实时间变短原因是每个操作不再阻塞，而是利用多个处理器核心并行计算。）

### 任务5. 进程与资源管理 （1 分）

后续实验中，大家会经常遇到"端口被占用"、"自己上次的进程没退干净"、"想知道哪台机器还剩多少内存/磁盘"等问题。本任务介绍最常用的几条命令，请同学亲手做一次定位与清理。

#### 5.1 查看与终止进程

`ps` 用来查看当前进程，`kill` 用来发送信号给进程：

```shell
2019211199@thumm01:~$ ps -ef | grep $USER | head      # 查看自己的进程
2019211199@thumm01:~$ ps aux --sort=-%cpu | head      # 按 CPU 占用排序
2019211199@thumm01:~$ kill <pid>                      # 礼貌地结束进程（SIGTERM）
2019211199@thumm01:~$ kill -9 <pid>                   # 强制结束（SIGKILL，慎用）
```

`top` / `htop` 提供交互式实时视图（按 `q` 退出）。

#### 5.2 后台运行与作业控制

```shell
2019211199@thumm01:~$ sleep 300 &                # & 让命令在后台运行
2019211199@thumm01:~$ jobs                       # 查看当前 shell 的后台作业
2019211199@thumm01:~$ fg %1                      # 把 1 号作业切回前台
2019211199@thumm01:~$ Ctrl-Z                     # 在前台作业里按下，挂起
2019211199@thumm01:~$ bg %1                      # 把挂起的作业放到后台继续

# 退出 ssh 后仍要继续执行的任务
2019211199@thumm01:~$ nohup python3 long_job.py > log.out 2>&1 &
```

#### 5.3 查看资源占用与端口占用

```shell
2019211199@thumm01:~$ free -h            # 查看内存
2019211199@thumm01:~$ df -h              # 查看各挂载点的磁盘剩余
2019211199@thumm01:~$ du -sh ./MyDFS     # 查看某个目录占用
2019211199@thumm01:~$ lsof -i:11009      # 查看占用某端口的进程（后续 lab2/4 常用）
```

#### 任务要求

1. 写一个会持续运行 60 秒以上的命令（例如 `sleep 120`），分别用 `&` 和 `nohup ... &` 启动；分别用 `ps` / `jobs` 查看，截图。
2. 使用 `kill` 终止其中一个进程（不要使用 `-9`），并用 `ps` 验证它确实退出。
3. 截图 `free -h`、`df -h` 和当前用户目录的 `du -sh`。在报告中简述：当后续实验出现"端口被占用"时，你打算如何定位并清理。

### 任务6. shell 脚本基础 （2 分）

后续实验需要在多个节点上启停 NameNode、DataNode、worker 等进程，手动逐机操作既繁琐又易错。本任务通过编写脚本掌握变量、流程控制、函数、退出码与远程执行，并把任务 4 / 任务 5 中已经会的命令组织成一组**可复用的脚本**。

#### 6.1 基本语法回顾

```shell
#!/bin/bash
set -e                                # 出错即退出，便于发现问题

NAME="thumm"                          # 变量赋值，等号两侧不能有空格
NODES=(01 02 03 04)                   # 数组

greet() {                             # 函数定义
    local who=$1                      # 函数第 1 个参数
    echo "Hello, ${who}!"
}

for n in "${NODES[@]}"; do            # for 循环遍历数组
    greet "${NAME}${n}"
done

if [ -f wc_dataset.txt ]; then        # 文件是否存在
    echo "dataset ready"
else
    echo "dataset missing" >&2
    exit 1
fi

ls /no/such/dir
echo "exit code = $?"                 # $? 是上一条命令的退出码
```

#### 6.2 任务要求：编写 `start_all.sh` 与 `stop_all.sh` （1.5 分）

请编写两个 shell 脚本，分别在 4 个节点（如集群一的 thumm01、02、03、04）上同时启动/停止一个示例进程（推荐用 `sleep 600` 模拟）：

`start_all.sh` 至少需要做到：

1. 把节点列表放在数组里，便于修改；
2. 使用 `for` 循环对每个节点执行 `ssh <node> "nohup sleep 600 > /tmp/demo.log 2>&1 &"`；
3. 每条 `ssh` 后检查 `$?`，失败时打印警告但继续后面的节点；
4. 全部启动完成后，再次 `ssh` 各节点用 `pgrep -af "sleep 600"` 验证进程已经存在，并把结果汇总打印。

`stop_all.sh` 应该使用 `pkill -f "sleep 600"` 或 `kill <pid>` 把刚才启动的进程清理掉，并打印每台机器的清理结果。

请在报告中给出脚本完整内容，以及一次完整的"启动—验证—停止"运行截图。

#### 6.3 进阶：把任务 3.3 的"一行管道"改写成脚本 （0.5 分）

把任务 3.3 中 Top-K 高频词的一行管道，改写为一个带参数的脚本 `topk.sh <input_file> <K>`：

1. 检查输入参数个数（`if [ $# -ne 2 ]; then ...; exit 1; fi`），错误时给出 usage；
2. 检查输入文件存在（`[ -f "$1" ]`）；
3. 输出 Top-K 行结果。

请在报告中给出脚本，并展示 `./topk.sh wc_dataset.txt 10` 的运行结果。该脚本会在 Bonus 的多节点流水线里被复用。

## 四、Bonus（2 分）：多节点协同处理流水线

> 本部分为 Bonus，最高 2 分。完成情况好可以直接弥补主体部分丢的分数；做不出来不影响主体的 5 分满分。

### B.1 集群主机之间免密登录配置 （0.5 分）

为了充分利用集群的运算性能，我们需要将资源分配至各个节点、协调各个节点的任务、整合多个结果等等。要在多主机上协同运行命令，首先要让 4 个节点之间能够互相免密登录。下面给出一个参考脚本的伪代码，请同学们自行实现：

```shell
2019211199@thumm01:~$ mkdir ssh-keys
2019211199@thumm01:~$ cd ssh-keys
```

创建一个登录脚本auto_autho.sh, 内容如下
```shell
2019211199@thumm01:~/ssh-keys$ vim auto_autho.sh
```

auto_autho.sh文件的内容:

 ``` shell
#!/bin/bash
Empty the authorized_keys file

For each node:
    Generate an SSH key pair for this node
    Append the public key to authorized_keys

For each node:
    Copy authorized_keys and the key files to the node's ~/.ssh/ directory

# 这个脚本做的思路是在thumm01上生成4个节点的公钥和私钥，然后把所有公钥加入到authorized_keys中，然后把各自的公钥私钥以及authorized_keys分发到各个节点。之后就可以通过ssh thumm0**X**从thumm01免密登录到**X**号节点了。


 ```



### B.2 多节点词频统计：切分→分发→执行→回收→汇总  （1.5 分）

请仿照 `wc_dataset.txt`，制作 10M~20M 左右的数据集（比如将 `wc_dataset.txt` 重复拼接十几次，不要太多会把硬盘占满）。在多主机运行一个简单的词频统计任务并汇总（即每个单词出现多少次，区分大小写），对比单机处理和多机处理的差异，可以包括任务执行结果、延迟等方面。

> **重要提醒**：每年都有大量同学把"多节点"做成了"在 thumm01 上跑完全部数据再 scp 几个文件到别的机器"。这并不是真正的多节点处理。请严格按照下面的拆解步骤来做。

#### 参考拆解步骤（强烈建议按此结构组织代码）

将多节点任务处理拆成 5 个阶段：**Split → Distribute → Execute → Collect → Reduce**。下面给出每一步可参考的命令，最终请把这 5 步串成一个 shell 脚本（例如 `multi_wc.sh`）。建议直接复用任务 6 写好的 `topk.sh` 作为远程节点的执行单元。

1. **Split（在 master 节点切片）**：将数据集切成与节点数等量的若干片：
    ```shell
    # 假设有 4 台机器，等分为 4 片：part_aa, part_ab, part_ac, part_ad
    split -n l/4 wc_big.txt part_
    ```
2. **Distribute（分发到各节点）**：
    ```shell
    NODES=(thumm01 thumm02 thumm03 thumm04)
    PARTS=(part_aa part_ab part_ac part_ad)
    for i in 0 1 2 3; do
        scp ${PARTS[$i]} ${NODES[$i]}:/tmp/
    done
    ```
3. **Execute（远程执行词频统计，并写入各自的本地结果文件）**：
    ```shell
    for i in 0 1 2 3; do
        ssh ${NODES[$i]} "cat /tmp/${PARTS[$i]} \
            | tr 'A-Z' 'a-z' \
            | tr -cs 'a-z' '\n' \
            | sort | uniq -c \
            > /tmp/${PARTS[$i]}.cnt" &
    done
    wait
    ```
4. **Collect（把各节点的局部结果拉回 master）**：
    ```shell
    for i in 0 1 2 3; do
        scp ${NODES[$i]}:/tmp/${PARTS[$i]}.cnt ./
    done
    ```
5. **Reduce（在 master 上做最终汇总）**：
    > 局部结果格式是"次数 单词"，相同单词可能在多个节点上各出现一次，需要把它们再合并：
    ```shell
    cat part_*.cnt \
        | awk '{cnt[$2]+=$1} END{for(w in cnt) print cnt[w], w}' \
        | sort -rn \
        | head -n 10 > final.txt
    ```

完成上述脚本后，请回答下面三个问题，写到报告里：

1. 用 `time` 分别对比"单机处理整份数据"和"4 节点 multi_wc.sh"的 real time，给出加速比；
2. 加速比是否接近 4×？如果不是，请说明你认为耗时主要花在了哪里（提示：scp 的网络/磁盘 IO 不可忽略）；
3. 如果数据集只有 1MB，多节点处理会不会反而更慢？如果会更慢，这是为什么？
