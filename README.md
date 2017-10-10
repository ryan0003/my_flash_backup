# my_flash_backup
# 使用方法：
 配置conf.yaml文件
  为了方便切换数据库，使用了conf.yaml文件，这里说下其中几个重要的参数：
   server_conf:里面的“con1”、“con2”是对应于下面的if_sit和if_pro的。就是有多少个conN就有多少个if_xxx(其中名# 字也是可以自定义的)。if_xxx就是数据库的资料了（用户名、密码什么的）
    log_file和log_pos两个值：这两个值的意思就是从哪个binlog文件的哪个点开始读取二进制语句。就是说比如现在你要操作数据库了，可以使用show master status获取当前的binlog文件和点，填入配置文件启动脚本；又或者你发现问题了，可以找到出问题前的某个时间点，找到当时的binlog文件的点，填入配置文件。
    is_set:这个参数为1就是使用当前的if_xxx。
    server_id： 不要个数据库的server_id一样就可以了
    log_dir： 现在还没加上，暂时没有意义
    log_level： 可以留着不写就""这样，也可以使用all和info，输出自己体验一下（这个还没想好要怎么弄。。。）


