# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'saver_loader.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Saver_Loader(object):
    def setupUi(self, Saver_Loader):
        if not Saver_Loader.objectName():
            Saver_Loader.setObjectName(u"Saver_Loader")
        Saver_Loader.resize(525, 469)
        self.verticalLayout = QVBoxLayout(Saver_Loader)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Saver_Loader)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 50)
        self.job_grp = QGroupBox(self.frame)
        self.job_grp.setObjectName(u"job_grp")
        self.verticalLayout_8 = QVBoxLayout(self.job_grp)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 10)
        self.show_lbl = QLabel(self.job_grp)
        self.show_lbl.setObjectName(u"show_lbl")

        self.horizontalLayout_5.addWidget(self.show_lbl)

        self.cbb_show = QComboBox(self.job_grp)
        self.cbb_show.setObjectName(u"cbb_show")

        self.horizontalLayout_5.addWidget(self.cbb_show)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, -1, -1, 10)
        self.seq_lbl = QLabel(self.job_grp)
        self.seq_lbl.setObjectName(u"seq_lbl")

        self.horizontalLayout_10.addWidget(self.seq_lbl)

        self.cbb_sequence = QComboBox(self.job_grp)
        self.cbb_sequence.setObjectName(u"cbb_sequence")

        self.horizontalLayout_10.addWidget(self.cbb_sequence)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 10)
        self.label_2 = QLabel(self.job_grp)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_6.addWidget(self.label_2)

        self.cbb_shot = QComboBox(self.job_grp)
        self.cbb_shot.setObjectName(u"cbb_shot")

        self.horizontalLayout_6.addWidget(self.cbb_shot)


        self.verticalLayout_7.addLayout(self.horizontalLayout_6)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)


        self.horizontalLayout.addWidget(self.job_grp)

        self.task_grp = QGroupBox(self.frame)
        self.task_grp.setObjectName(u"task_grp")
        self.verticalLayout_10 = QVBoxLayout(self.task_grp)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 10)
        self.dep_lbl = QLabel(self.task_grp)
        self.dep_lbl.setObjectName(u"dep_lbl")

        self.horizontalLayout_7.addWidget(self.dep_lbl)

        self.cbb_department = QComboBox(self.task_grp)
        self.cbb_department.setObjectName(u"cbb_department")

        self.horizontalLayout_7.addWidget(self.cbb_department)


        self.verticalLayout_9.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, -1, -1, 10)
        self.task_lbl = QLabel(self.task_grp)
        self.task_lbl.setObjectName(u"task_lbl")

        self.horizontalLayout_9.addWidget(self.task_lbl)

        self.cbb_task = QComboBox(self.task_grp)
        self.cbb_task.setObjectName(u"cbb_task")

        self.horizontalLayout_9.addWidget(self.cbb_task)


        self.verticalLayout_9.addLayout(self.horizontalLayout_9)

        self.bnt_refresh = QPushButton(self.task_grp)
        self.bnt_refresh.setObjectName(u"bnt_refresh")

        self.verticalLayout_9.addWidget(self.bnt_refresh)


        self.verticalLayout_10.addLayout(self.verticalLayout_9)


        self.horizontalLayout.addWidget(self.task_grp)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.version_grp = QGroupBox(self.frame)
        self.version_grp.setObjectName(u"version_grp")
        self.verticalLayout_6 = QVBoxLayout(self.version_grp)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.label = QLabel(self.version_grp)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label, 0, Qt.AlignTop)

        self.list_scripts_versions = QListView(self.version_grp)
        self.list_scripts_versions.setObjectName(u"list_scripts_versions")

        self.horizontalLayout_2.addWidget(self.list_scripts_versions)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.btn_save = QPushButton(self.version_grp)
        self.btn_save.setObjectName(u"btn_save")

        self.verticalLayout_5.addWidget(self.btn_save)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 10)
        self.lbl_path = QLabel(self.version_grp)
        self.lbl_path.setObjectName(u"lbl_path")

        self.horizontalLayout_4.addWidget(self.lbl_path)

        self.lbl_path_info = QLabel(self.version_grp)
        self.lbl_path_info.setObjectName(u"lbl_path_info")

        self.horizontalLayout_4.addWidget(self.lbl_path_info)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 10)
        self.lbl_user = QLabel(self.version_grp)
        self.lbl_user.setObjectName(u"lbl_user")

        self.horizontalLayout_3.addWidget(self.lbl_user)

        self.lbl_user_info = QLabel(self.version_grp)
        self.lbl_user_info.setObjectName(u"lbl_user_info")

        self.horizontalLayout_3.addWidget(self.lbl_user_info)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.btn_open = QPushButton(self.version_grp)
        self.btn_open.setObjectName(u"btn_open")

        self.verticalLayout_5.addWidget(self.btn_open)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)


        self.verticalLayout_4.addWidget(self.version_grp)


        self.verticalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Saver_Loader)

        QMetaObject.connectSlotsByName(Saver_Loader)
    # setupUi

    def retranslateUi(self, Saver_Loader):
        Saver_Loader.setWindowTitle(QCoreApplication.translate("Saver_Loader", u"Form", None))
        self.job_grp.setTitle(QCoreApplication.translate("Saver_Loader", u"Job", None))
        self.show_lbl.setText(QCoreApplication.translate("Saver_Loader", u"Show:", None))
        self.seq_lbl.setText(QCoreApplication.translate("Saver_Loader", u"Secquence:", None))
        self.label_2.setText(QCoreApplication.translate("Saver_Loader", u"Shot:", None))
        self.task_grp.setTitle(QCoreApplication.translate("Saver_Loader", u"Task", None))
        self.dep_lbl.setText(QCoreApplication.translate("Saver_Loader", u"Department:", None))
        self.task_lbl.setText(QCoreApplication.translate("Saver_Loader", u"Task:", None))
        self.bnt_refresh.setText(QCoreApplication.translate("Saver_Loader", u"Refresh", None))
        self.version_grp.setTitle(QCoreApplication.translate("Saver_Loader", u"Version Info", None))
        self.label.setText(QCoreApplication.translate("Saver_Loader", u"Verssions:", None))
        self.btn_save.setText(QCoreApplication.translate("Saver_Loader", u"Save", None))
        self.lbl_path.setText(QCoreApplication.translate("Saver_Loader", u"Path:", None))
        self.lbl_path_info.setText("")
        self.lbl_user.setText(QCoreApplication.translate("Saver_Loader", u"User:", None))
        self.lbl_user_info.setText("")
        self.btn_open.setText(QCoreApplication.translate("Saver_Loader", u"Open", None))
    # retranslateUi

