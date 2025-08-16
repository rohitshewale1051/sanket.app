import sys
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QLabel)
from PyQt5.QtCore import QTimer,QTime,Qt
class stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.time=QTime(0,0,0,0)
        self.time_label=QLabel("00:00:00:00",self)
        self.start_button=QPushButton("Start",self)
        self.stop_button=QPushButton("stop",self)
        self.reset_button=QPushButton("reset",self)
        self.timer=QTimer(self)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("STopwatch")

        vbox=QVBoxLayout()
        vbox.addWidget(self.time_label)
        
        
        self.setLayout(vbox)

        self.time_label.setAlignment(Qt.AlignCenter)

        hbox=QHBoxLayout()

        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.reset_button)

        vbox.addLayout(hbox)

        self.setStyleSheet("""
             Qpushbutton,QLabel{
                 padding:20px;
                 font-weight:bold;
                 font-family:callbri:
            }
             Qpushbutton{
                 font-size:50px;
            }
            QLabel{
                font-size:120px;
                background-color:hs1(200,100%,85%);
                border-radius:       
            }
        """)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)
        self.timer.timeout.connect(self.update_display)


    def start(self):
        self.timer.start(10)

    def stop(self):
        self.timer.stop(10)

    def reset(self):
        self.time=QTime(0,0,0,0)
        self.time_label.selectedText(self.format_time(self.time))

    def format_time(self,time):
        hours=time.hour()
        minutes=time.minute()
        seconds=time.second()
        milliseconds=time.msec()//10
        return f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds:02}"

    def update_display(self):
        self.time=self.time.addMSecs(10)
        self.time_label.setText(self.format_time(self.time))
if __name__ == "__main__":
     app=QApplication(sys.argv)
     stopwatch=stopwatch()
     stopwatch.show()
     sys.exit(app.exec_())
