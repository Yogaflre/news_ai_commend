# 加载数据的类
class LoadFile(object):
    # 加载一个文件，按照行循环输出
    def loadFile(self, fileName):
        file = open(fileName, 'r')
        for line in file:
            yield line.strip('\r\n')  # 返回执行结果并不中断程序
        file.close()
