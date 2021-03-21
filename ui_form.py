/********************************************************************************
** Form generated from reading UI file 'form.ui'
**
** Created by: Qt User Interface Compiler version 5.9.7
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_FORM_H
#define UI_FORM_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QVBoxLayout *verticalLayout;
    QFrame *bar_frame;
    QHBoxLayout *horizontalLayout;
    QFrame *menuopen_frame;
    QGridLayout *gridLayout;
    QPushButton *pushButton;
    QFrame *top_frame;
    QVBoxLayout *verticalLayout_2;
    QFrame *title_frame;
    QHBoxLayout *horizontalLayout_2;
    QLabel *title_label;
    QPushButton *minimise_button;
    QPushButton *maximise_button;
    QPushButton *close_button;
    QFrame *subtitle_frame;
    QFrame *center_frame;
    QHBoxLayout *horizontalLayout_3;
    QFrame *frame;
    QFrame *frame_2;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(1147, 835);
        QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MainWindow->sizePolicy().hasHeightForWidth());
        MainWindow->setSizePolicy(sizePolicy);
        QPalette palette;
        QBrush brush(QColor(210, 210, 210, 255));
        brush.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::WindowText, brush);
        QBrush brush1(QColor(40, 44, 52, 255));
        brush1.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Button, brush1);
        QBrush brush2(QColor(255, 255, 255, 255));
        brush2.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Light, brush2);
        QBrush brush3(QColor(227, 227, 227, 255));
        brush3.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Midlight, brush3);
        QBrush brush4(QColor(160, 160, 160, 255));
        brush4.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Dark, brush4);
        palette.setBrush(QPalette::Active, QPalette::Mid, brush4);
        palette.setBrush(QPalette::Active, QPalette::Text, brush);
        palette.setBrush(QPalette::Active, QPalette::BrightText, brush2);
        palette.setBrush(QPalette::Active, QPalette::ButtonText, brush);
        palette.setBrush(QPalette::Active, QPalette::Base, brush1);
        palette.setBrush(QPalette::Active, QPalette::Window, brush1);
        QBrush brush5(QColor(105, 105, 105, 255));
        brush5.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Shadow, brush5);
        QBrush brush6(QColor(245, 245, 245, 255));
        brush6.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::AlternateBase, brush6);
        QBrush brush7(QColor(255, 255, 220, 255));
        brush7.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::ToolTipBase, brush7);
        QBrush brush8(QColor(0, 0, 0, 255));
        brush8.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::ToolTipText, brush8);
        QBrush brush9(QColor(210, 210, 210, 128));
        brush9.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::PlaceholderText, brush9);
        palette.setBrush(QPalette::Inactive, QPalette::WindowText, brush);
        palette.setBrush(QPalette::Inactive, QPalette::Button, brush1);
        palette.setBrush(QPalette::Inactive, QPalette::Light, brush2);
        palette.setBrush(QPalette::Inactive, QPalette::Midlight, brush3);
        palette.setBrush(QPalette::Inactive, QPalette::Dark, brush4);
        palette.setBrush(QPalette::Inactive, QPalette::Mid, brush4);
        palette.setBrush(QPalette::Inactive, QPalette::Text, brush);
        palette.setBrush(QPalette::Inactive, QPalette::BrightText, brush2);
        palette.setBrush(QPalette::Inactive, QPalette::ButtonText, brush);
        palette.setBrush(QPalette::Inactive, QPalette::Base, brush1);
        palette.setBrush(QPalette::Inactive, QPalette::Window, brush1);
        palette.setBrush(QPalette::Inactive, QPalette::Shadow, brush5);
        palette.setBrush(QPalette::Inactive, QPalette::AlternateBase, brush6);
        palette.setBrush(QPalette::Inactive, QPalette::ToolTipBase, brush7);
        palette.setBrush(QPalette::Inactive, QPalette::ToolTipText, brush8);
        palette.setBrush(QPalette::Inactive, QPalette::PlaceholderText, brush9);
        palette.setBrush(QPalette::Disabled, QPalette::WindowText, brush);
        palette.setBrush(QPalette::Disabled, QPalette::Button, brush1);
        palette.setBrush(QPalette::Disabled, QPalette::Light, brush2);
        palette.setBrush(QPalette::Disabled, QPalette::Midlight, brush3);
        palette.setBrush(QPalette::Disabled, QPalette::Dark, brush4);
        palette.setBrush(QPalette::Disabled, QPalette::Mid, brush4);
        palette.setBrush(QPalette::Disabled, QPalette::Text, brush);
        palette.setBrush(QPalette::Disabled, QPalette::BrightText, brush2);
        palette.setBrush(QPalette::Disabled, QPalette::ButtonText, brush);
        palette.setBrush(QPalette::Disabled, QPalette::Base, brush1);
        palette.setBrush(QPalette::Disabled, QPalette::Window, brush1);
        palette.setBrush(QPalette::Disabled, QPalette::Shadow, brush8);
        palette.setBrush(QPalette::Disabled, QPalette::AlternateBase, brush6);
        palette.setBrush(QPalette::Disabled, QPalette::ToolTipBase, brush7);
        palette.setBrush(QPalette::Disabled, QPalette::ToolTipText, brush8);
        palette.setBrush(QPalette::Disabled, QPalette::PlaceholderText, brush9);
        MainWindow->setPalette(palette);
        MainWindow->setStyleSheet(QStringLiteral(""));
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QStringLiteral("centralwidget"));
        sizePolicy.setHeightForWidth(centralwidget->sizePolicy().hasHeightForWidth());
        centralwidget->setSizePolicy(sizePolicy);
        centralwidget->setStyleSheet(QLatin1String("color: rgb(210, 210, 210);\n"
"border: 0;"));
        verticalLayout = new QVBoxLayout(centralwidget);
        verticalLayout->setSpacing(0);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        bar_frame = new QFrame(centralwidget);
        bar_frame->setObjectName(QStringLiteral("bar_frame"));
        QSizePolicy sizePolicy1(QSizePolicy::Expanding, QSizePolicy::Maximum);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(bar_frame->sizePolicy().hasHeightForWidth());
        bar_frame->setSizePolicy(sizePolicy1);
        bar_frame->setMinimumSize(QSize(0, 65));
        bar_frame->setMaximumSize(QSize(16777215, 65));
        bar_frame->setFrameShape(QFrame::NoFrame);
        bar_frame->setFrameShadow(QFrame::Plain);
        bar_frame->setLineWidth(0);
        horizontalLayout = new QHBoxLayout(bar_frame);
        horizontalLayout->setSpacing(0);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        horizontalLayout->setContentsMargins(0, 0, 0, 0);
        menuopen_frame = new QFrame(bar_frame);
        menuopen_frame->setObjectName(QStringLiteral("menuopen_frame"));
        menuopen_frame->setMinimumSize(QSize(70, 0));
        menuopen_frame->setMaximumSize(QSize(70, 16777215));
        menuopen_frame->setStyleSheet(QLatin1String("background-color: #1C1D23;\n"
""));
        menuopen_frame->setFrameShape(QFrame::NoFrame);
        menuopen_frame->setFrameShadow(QFrame::Plain);
        menuopen_frame->setLineWidth(0);
        gridLayout = new QGridLayout(menuopen_frame);
        gridLayout->setSpacing(0);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        gridLayout->setContentsMargins(0, 0, 0, 0);
        pushButton = new QPushButton(menuopen_frame);
        pushButton->setObjectName(QStringLiteral("pushButton"));
        sizePolicy.setHeightForWidth(pushButton->sizePolicy().hasHeightForWidth());
        pushButton->setSizePolicy(sizePolicy);
        pushButton->setStyleSheet(QLatin1String("QPushButton {\n"
"	background-image:url(:/icon_24x24/icons/24x24/cil-menu.png);\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}"));

        gridLayout->addWidget(pushButton, 0, 0, 1, 1);


        horizontalLayout->addWidget(menuopen_frame);

        top_frame = new QFrame(bar_frame);
        top_frame->setObjectName(QStringLiteral("top_frame"));
        top_frame->setStyleSheet(QStringLiteral("background-color: rgb(37, 39, 44)"));
        top_frame->setFrameShape(QFrame::StyledPanel);
        top_frame->setFrameShadow(QFrame::Raised);
        verticalLayout_2 = new QVBoxLayout(top_frame);
        verticalLayout_2->setSpacing(0);
        verticalLayout_2->setObjectName(QStringLiteral("verticalLayout_2"));
        verticalLayout_2->setContentsMargins(0, 0, 0, 0);
        title_frame = new QFrame(top_frame);
        title_frame->setObjectName(QStringLiteral("title_frame"));
        QSizePolicy sizePolicy2(QSizePolicy::Expanding, QSizePolicy::Preferred);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(0);
        sizePolicy2.setHeightForWidth(title_frame->sizePolicy().hasHeightForWidth());
        title_frame->setSizePolicy(sizePolicy2);
        title_frame->setMinimumSize(QSize(0, 42));
        title_frame->setStyleSheet(QLatin1String("QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}"));
        title_frame->setFrameShape(QFrame::StyledPanel);
        title_frame->setFrameShadow(QFrame::Raised);
        horizontalLayout_2 = new QHBoxLayout(title_frame);
        horizontalLayout_2->setSpacing(0);
        horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
        horizontalLayout_2->setContentsMargins(15, 0, 0, 0);
        title_label = new QLabel(title_frame);
        title_label->setObjectName(QStringLiteral("title_label"));
        sizePolicy.setHeightForWidth(title_label->sizePolicy().hasHeightForWidth());
        title_label->setSizePolicy(sizePolicy);
        QFont font;
        font.setFamily(QStringLiteral("Segoe UI"));
        font.setPointSize(10);
        font.setBold(true);
        font.setWeight(75);
        title_label->setFont(font);

        horizontalLayout_2->addWidget(title_label);

        minimise_button = new QPushButton(title_frame);
        minimise_button->setObjectName(QStringLiteral("minimise_button"));
        QSizePolicy sizePolicy3(QSizePolicy::Fixed, QSizePolicy::Expanding);
        sizePolicy3.setHorizontalStretch(0);
        sizePolicy3.setVerticalStretch(0);
        sizePolicy3.setHeightForWidth(minimise_button->sizePolicy().hasHeightForWidth());
        minimise_button->setSizePolicy(sizePolicy3);
        minimise_button->setMinimumSize(QSize(40, 0));
        minimise_button->setMaximumSize(QSize(40, 16777215));
        minimise_button->setStyleSheet(QLatin1String("background-image:url(:/icon_24x24/icons/24x24/cil-window-minimize.png);\n"
""));

        horizontalLayout_2->addWidget(minimise_button);

        maximise_button = new QPushButton(title_frame);
        maximise_button->setObjectName(QStringLiteral("maximise_button"));
        sizePolicy3.setHeightForWidth(maximise_button->sizePolicy().hasHeightForWidth());
        maximise_button->setSizePolicy(sizePolicy3);
        maximise_button->setMinimumSize(QSize(40, 0));
        maximise_button->setMaximumSize(QSize(40, 16777215));
        maximise_button->setStyleSheet(QStringLiteral("background-image:url(:/icon_24x24/icons/24x24/cil-window-maximize.png);"));

        horizontalLayout_2->addWidget(maximise_button);

        close_button = new QPushButton(title_frame);
        close_button->setObjectName(QStringLiteral("close_button"));
        sizePolicy3.setHeightForWidth(close_button->sizePolicy().hasHeightForWidth());
        close_button->setSizePolicy(sizePolicy3);
        close_button->setMinimumSize(QSize(40, 0));
        close_button->setMaximumSize(QSize(40, 16777215));
        close_button->setStyleSheet(QStringLiteral("background-image:url(:/icon_24x24/icons/24x24/cil-x.png);"));

        horizontalLayout_2->addWidget(close_button);


        verticalLayout_2->addWidget(title_frame);

        subtitle_frame = new QFrame(top_frame);
        subtitle_frame->setObjectName(QStringLiteral("subtitle_frame"));
        subtitle_frame->setMinimumSize(QSize(0, 23));
        subtitle_frame->setStyleSheet(QLatin1String("background-color: rgb(39,44,54);\n"
"border: 0;"));
        subtitle_frame->setFrameShape(QFrame::StyledPanel);
        subtitle_frame->setFrameShadow(QFrame::Plain);
        subtitle_frame->setLineWidth(0);

        verticalLayout_2->addWidget(subtitle_frame);


        horizontalLayout->addWidget(top_frame);


        verticalLayout->addWidget(bar_frame);

        center_frame = new QFrame(centralwidget);
        center_frame->setObjectName(QStringLiteral("center_frame"));
        center_frame->setFrameShape(QFrame::NoFrame);
        center_frame->setFrameShadow(QFrame::Plain);
        center_frame->setLineWidth(0);
        horizontalLayout_3 = new QHBoxLayout(center_frame);
        horizontalLayout_3->setSpacing(0);
        horizontalLayout_3->setObjectName(QStringLiteral("horizontalLayout_3"));
        horizontalLayout_3->setContentsMargins(0, 0, 0, 0);
        frame = new QFrame(center_frame);
        frame->setObjectName(QStringLiteral("frame"));
        frame->setMinimumSize(QSize(70, 0));
        frame->setStyleSheet(QStringLiteral("background-color: rgb(27, 29, 35);"));
        frame->setFrameShape(QFrame::StyledPanel);
        frame->setFrameShadow(QFrame::Raised);

        horizontalLayout_3->addWidget(frame);

        frame_2 = new QFrame(center_frame);
        frame_2->setObjectName(QStringLiteral("frame_2"));
        sizePolicy2.setHeightForWidth(frame_2->sizePolicy().hasHeightForWidth());
        frame_2->setSizePolicy(sizePolicy2);
        frame_2->setStyleSheet(QLatin1String("background-color: rgb(40, 44, 52);\n"
"border: 0;"));
        frame_2->setFrameShape(QFrame::StyledPanel);
        frame_2->setFrameShadow(QFrame::Sunken);
        frame_2->setLineWidth(0);

        horizontalLayout_3->addWidget(frame_2);


        verticalLayout->addWidget(center_frame);

        MainWindow->setCentralWidget(centralwidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", Q_NULLPTR));
        pushButton->setText(QString());
        title_label->setText(QApplication::translate("MainWindow", "Chess GUI", Q_NULLPTR));
        minimise_button->setText(QString());
        maximise_button->setText(QString());
        close_button->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_FORM_H
