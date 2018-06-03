import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QTextEdit, QLabel
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPalette, QFont, QPixmap
from news_ai_commend.news_spider import spider_main
from news_ai_commend.news_recommend import commend_main, testSpark2


class Index(QWidget):

    def __init__(self):
        super().__init__()
        self.text_spider = QTextEdit(self)
        self.text_commend_user = QTextEdit(self)
        self.text_commend_als = QTextEdit(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('教育新闻智能推荐系统')
        self.resize(1000, 700)
        self.setStyleSheet("background-color:white;")

        # 设置颜色属性
        # pe = QPalette()
        # pe.setColor(QPalette.WindowText, Qt.gray)

        # 设置logo
        label_img = QLabel(self)
        school_png = QPixmap('/Users/yogafire/Documents/Projects-Pycharm/news_ai_commend/news_view/school.jpg')
        label_img.setPixmap(school_png)
        label_img.setAlignment(Qt.AlignCenter)
        label_img.setGeometry(0, 30, 1000, 50)

        # 设置标题
        label = QLabel("教育新闻智能推荐系统", self)
        label.setFont(QFont("Roman times", 30, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        # 屏幕从(x,y)开始，显示一个(x,y)的label
        label.setGeometry(0, 120, 1000, 30)
        # 设置label颜色
        # label.setPalette(pe)

        # 爬取按钮
        btn_spider = QPushButton('新闻数据采集', self)
        btn_spider.setGeometry(100, 200, 200, 50)
        btn_spider.clicked.connect(self.craw)
        btn_spider.setStyleSheet("background-color:lightblue;")
        # 爬取数据框
        self.text_spider.setGeometry(60, 300, 280, 350)

        # 推荐按钮1
        btn_commend_user = QPushButton('新闻推荐之UserCF', self)
        btn_commend_user.setGeometry(400, 200, 200, 50)
        btn_commend_user.clicked.connect(self.commend_user)
        btn_commend_user.setStyleSheet("background-color:lightblue;")
        # 推荐1数据框
        self.text_commend_user.setGeometry(360, 300, 280, 350)

        # 推荐按钮2
        btn_commend_als = QPushButton('新闻推荐之ALS', self)
        btn_commend_als.setGeometry(700, 200, 200, 50)
        btn_commend_als.clicked.connect(self.commend_als)
        btn_commend_als.setStyleSheet("background-color:lightblue;")
        # 推荐2数据框
        self.text_commend_als.setGeometry(660, 300, 280, 350)

    @pyqtSlot()
    def craw(self):
        pageNum = self.text_spider.toPlainText()
        self.text_spider.setText("")
        spiderMain = spider_main.SpiderMain()
        num = 1
        for new_data in spiderMain.craw("http://www.jyb.cn/sy/zhxw/", int(pageNum)):
            self.text_spider.append(str(num) + "、" + "".join(new_data))
            self.text_spider.append("")
            num = num + 1

    @pyqtSlot()
    def commend_user(self):
        userNum = self.text_commend_user.toPlainText()
        self.text_commend_user.setText("")
        commendMain = commend_main.CommendMain()
        commendMain.training(
            "/Users/yogafire/Documents/Projects-Pycharm/news_ai_commend/news_recommend/data/ratings2.dat")
        commend_list = commendMain.commend(userNum)
        num = 1
        for commends in commend_list:
            str1 = str(num) + "、" + commends[0] + "：" + commends[1]
            str2 = "感兴趣的程度为：" + str(commends[2])
            self.text_commend_user.append(str1)
            self.text_commend_user.append(str2)
            self.text_commend_user.append("")
            num = num + 1

    @pyqtSlot()
    def commend_als(self):
        userNum = self.text_commend_als.toPlainText()
        self.text_commend_als.setText("")
        testSparkMain2 = testSpark2.testSparkMain2()
        commend_list, rmse = testSparkMain2.test(userNum)
        num = 1
        for commends in commend_list:
            str1 = str(num) + "、" + commends[0] + "：" + commends[1]
            str2 = "感兴趣的程度为：" + str(commends[2])
            self.text_commend_als.append(str1)
            self.text_commend_als.append(str2)
            self.text_commend_als.append("")
            num = num + 1
        self.text_commend_als.append("均方根误差(RMSE)为：" + str(rmse))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    index = Index()
    index.show()
    sys.exit(app.exec_())
