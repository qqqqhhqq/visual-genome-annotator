import json
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

import libs.labelFile
from libs.shape import Shape
from libs.combobox import ComboBox
from libs.ustr import ustr
from libs.utils import *
from libs.constants import *
from libs.canvas import Canvas
from libs.labelDialog import LabelDialog
from libs.hashableQListWidgetItem import HashableQListWidgetItem
from libs.labelFile import LabelFile, LabelFileError
from libs.relationship import Relationship

__appname__ = 'application'


class MainWindow(QMainWindow):
    FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = list(range(3))

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        screen_size = QDesktopWidget().screenGeometry()
        self.setObjectName("MainWindow")
        self.setGeometry(0, 0, screen_size.width(), screen_size.height())
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(2000, 0, 261, 1151))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.objects_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.objects_label.setObjectName("objects_label")
        self.verticalLayout.addWidget(self.objects_label)
        self.objs_list_widget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.objs_list_widget.setObjectName("objs_list_widget")
        self.verticalLayout.addWidget(self.objs_list_widget)
        self.relations_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.relations_label.setObjectName("relations_label")
        self.verticalLayout.addWidget(self.relations_label)
        self.rels_list_widget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.rels_list_widget.setObjectName("rels_list_widget")
        self.verticalLayout.addWidget(self.rels_list_widget)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 281, 341))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(7)
        self.gridLayout.setObjectName("gridLayout")
        self.prev_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.prev_button.setObjectName("prev_button")
        self.gridLayout.addWidget(self.prev_button, 1, 1, 1, 1)
        self.open_dir = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.open_dir.setObjectName("open_dir")
        self.gridLayout.addWidget(self.open_dir, 0, 1, 1, 1)
        self.next_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.next_button.setObjectName("next_button")
        self.gridLayout.addWidget(self.next_button, 1, 2, 1, 1)
        self.open_anno_dir = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.open_anno_dir.setObjectName("open_anno_dir")
        self.gridLayout.addWidget(self.open_anno_dir, 0, 2, 1, 1)
        self.anno_res = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.anno_res.setObjectName("anno_res")
        self.gridLayout.addWidget(self.anno_res, 2, 2, 1, 1)
        self.anno_obj = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.anno_obj.setObjectName("anno_obj")
        self.anno_attr = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.anno_res.setObjectName("anno_attr")
        self.gridLayout.addWidget(self.anno_attr, 3, 1, 1, 1)
        self.anno_obj.setEnabled(False)
        self.anno_res.setEnabled(False)
        self.anno_attr.setEnabled(False)
        self.gridLayout.addWidget(self.anno_obj, 2, 1, 1, 1)
        # self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        # self.graphicsView.setGeometry(QtCore.QRect(295, 1, 1701, 1151))
        # self.graphicsView.setObjectName("graphicsView")
        self.save_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.save_button.setObjectName("save_button")
        self.save_button.setEnabled(False)
        self.gridLayout.addWidget(self.save_button, 4, 2, 1, 1)
        self.del_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.del_button.setObjectName("del_button")
        self.gridLayout.addWidget(self.del_button, 4, 1, 1, 1)

        self.canvas = Canvas(parent=self)
        self.scroll = QScrollArea(self.centralwidget)
        self.scroll.setWidget(self.canvas)
        self.scroll.setWidgetResizable(True)
        self.scroll_bars = {
            Qt.Vertical: self.scroll.verticalScrollBar(),
            Qt.Horizontal: self.scroll.horizontalScrollBar()
        }
        self.scroll.setGeometry(QtCore.QRect(300, 26, 1690, 1153))
        self.canvas.set_drawing_shape_to_square(False)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 860, 291, 291))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.imgs_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.imgs_label.setObjectName("imgs_label")
        self.verticalLayout_2.addWidget(self.imgs_label)
        self.image_list_widget = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.image_list_widget.setObjectName("image_list_widget")
        self.verticalLayout_2.addWidget(self.image_list_widget)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2242, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        self.action = QtWidgets.QAction(self)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(self)
        self.action_2.setObjectName("action_2")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())

        self.label_coordinates = QLabel('')

        self.os_path = os.getcwd()

        self.file_path = None
        self.last_open_dir = None  # 上次打开的文件
        self.default_save_dir = None  # 默认的保存文件
        self.m_img_list = []
        self.img_count = 0
        self.cur_img_idx = None
        self.image_data = None
        self.dir_name = None

        self.last_anno_dir = None
        self.anno_save_dir = None
        self.img_meta_json_file = None
        self.objects_json_file = None
        self.rela_json_file = None

        self.image = None
        self._beginner = True

        self.dirty = False

        self.objects_labels_list = []
        self.relations_labels_list = []
        self.objects_labels_list, self.relations_labels_list = self.load_predefined_label()

        self.prev_label_text = ''
        self.prev_predicate_text = ''
        self.lastLabel = None
        self.lastPredicate = None
        self.items_to_shapes = {}
        self.item_to_relationship = {}
        self.shapes_to_items = {}
        self.relationship_to_item = {}

        self.label_file = None

        self.label_dialog = LabelDialog(parent=self, list_item=self.objects_labels_list)
        self.predicate_dialog = LabelDialog(parent=self, list_item=self.relations_labels_list)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.init_widget()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.objects_label.setText(_translate("MainWindow", "objects"))
        self.relations_label.setText(_translate("MainWindow", "relations"))
        self.prev_button.setText(_translate("MainWindow", "上一张"))
        self.open_dir.setText(_translate("MainWindow", "打开文件夹"))
        self.next_button.setText(_translate("MainWindow", "下一张"))
        self.open_anno_dir.setText(_translate("MainWindow", "选择标注文件夹"))
        self.anno_res.setText(_translate("MainWindow", "标注关系"))
        self.anno_obj.setText(_translate("MainWindow", "标注对象"))
        self.anno_attr.setText(_translate("MainWindow", "标注属性"))
        self.imgs_label.setText(_translate("MainWindow", "图片"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.action.setText(_translate("MainWindow", "打开图片文件夹"))
        self.action_2.setText(_translate("MainWindow", "选择保存路径"))
        self.save_button.setText(_translate("MainWindow", "保存"))
        self.del_button.setText(_translate("MainWindow", "清除"))

    def init_widget(self):
        self.open_dir.clicked.connect(self.open_dir_dialog)
        self.open_anno_dir.clicked.connect(self.open_anno_dir_dialog)
        self.next_button.clicked.connect(self.open_next_image)
        self.prev_button.clicked.connect(self.open_prev_image)
        self.anno_obj.clicked.connect(self.create_shape)
        self.canvas.newShape.connect(self.new_shape)
        self.anno_res.clicked.connect(self.create_relation)
        self.canvas.annotateRelation.connect(self.new_relation)

    def show_message(self, title, msg):
        reply = QMessageBox.information(None, title, msg, QMessageBox.Yes)

    def status(self, message, delay=5000):
        self.statusBar.showMessage(message, delay)

    def beginner(self):
        return self._beginner

    def load_predefined_label(self):
        objects_txt = os.path.join(self.os_path, OBJECTS_TXT)
        relations_txt = os.path.join(self.os_path, RELATIONS_TXT)

        if os.path.exists(objects_txt):
            with open(objects_txt, 'r') as otxt:
                obj_txt_lines = otxt.readlines()
                obj_txt_lines = [line.strip() for line in obj_txt_lines]
        else:
            with open(objects_txt, 'w') as otxt:
                otxt.write("\n".join(self.objects_labels_list))
                obj_txt_lines = []

        if os.path.exists(relations_txt):
            with open(relations_txt, 'r') as rtxt:
                rel_txt_lines = rtxt.readlines()
                rel_txt_lines = [line.strip() for line in rel_txt_lines]
        else:
            with open(relations_txt, 'w') as rtxt:
                rtxt.write("\n".join(self.relations_labels_list))
                rel_txt_lines = []
        return obj_txt_lines, rel_txt_lines

    def set_dirty(self):
        self.dirty = True
        self.save_button.setEnabled(True)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            print('ctrl press')
            self.canvas.set_drawing_shape_to_square(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            # Draw rectangle if Ctrl is pressed
            self.canvas.set_drawing_shape_to_square(True)

    def open_dir_dialog(self, dir_path=None, silent=False):
        default_open_dir_path = dir_path if dir_path else '.'
        if self.last_open_dir and os.path.exists(self.last_open_dir):
            default_open_dir_path = self.last_open_dir
        else:
            default_open_dir_path = os.path.dirname(self.file_path) if self.file_path else '.'
        if silent != True:
            target_dir_path = ustr(QFileDialog.getExistingDirectory(self,
                                                                    '%s - Open Directory' % __appname__,
                                                                    default_open_dir_path,
                                                                    QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks))
        else:
            target_dir_path = ustr(default_open_dir_path)
        self.last_open_dir = target_dir_path
        self.default_save_dir = target_dir_path
        self.import_dir_images(target_dir_path)
        self.img_meta_json_file = os.path.join(self.default_save_dir, 'image_data.json')
        self.objects_json_file = os.path.join(self.default_save_dir, 'objects.json')

    def import_dir_images(self, dir_path):
        self.last_open_dir = dir_path
        self.dir_name = dir_path
        self.file_path = None
        self.image_list_widget.clear()
        self.m_img_list = self.scan_all_images(dir_path)
        self.img_count = len(self.m_img_list)
        self.open_next_image()
        for imgPath in self.m_img_list:
            item = QListWidgetItem(imgPath)
            self.image_list_widget.addItem(item)

    def scan_all_images(self, folder_path):
        extensions = ['.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        images = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    relative_path = os.path.join(root, file)
                    path = ustr(os.path.abspath(relative_path))
                    images.append(path)
        natural_sort(images, key=lambda x: x.lower())
        return images

    def open_prev_image(self, _value=False):
        # Proceeding prev image without dialog if having any label
        if self.img_count <= 0:
            return

        if self.file_path is None:
            return

        if self.cur_img_idx - 1 >= 0:
            self.cur_img_idx -= 1
            filename = self.m_img_list[self.cur_img_idx]
            if filename:
                self.load_file(filename)

    def open_next_image(self):
        if self.default_save_dir is not None:
            if self.dirty is True:
                self.save_file()
        else:
            self.show_message(ERROR, "设置标注保存文件！")

        if self.img_count <= 0:
            return

        if not self.m_img_list:
            return

        # 如果是刚打开就返回第一张，否则就打开下一张
        filename = None
        if self.file_path is None:
            filename = self.m_img_list[0]
            self.cur_img_idx = 0
        else:
            if self.cur_img_idx + 1 < self.img_count:
                self.cur_img_idx += 1
                filename = self.m_img_list[self.cur_img_idx]

        if filename:
            self.load_file(filename)

    def set_clean(self):
        self.dirty = False
        self.save_button.setEnabled(False)

    def _save_file(self, annotation_file_path):
        if annotation_file_path and self.save_labels(annotation_file_path):
            self.set_clean()
            self.status('Saved to  %s' % annotation_file_path)
            self.statusBar.show()

    def save_file(self):
        if self.default_save_dir is not None and len(ustr(self.default_save_dir)):
            if self.file_path:
                image_file_name = os.path.basename(self.file_path)
                saved_file_name = os.path.splitext(image_file_name)[0]
                saved_path = os.path.join(ustr(self.default_save_dir), saved_file_name)
                self._save_file(saved_path)

    # 12/19 - 23pm
    def save_labels(self, annotation_file_path):
        annotation_file_path = ustr(annotation_file_path)
        if self.label_file is None:
            self.label_file = LabelFile()

        def format_shape(s):
           return dict(label=s.label,
                  line_color=s.line_color.getRgb(),
                  fill_color=s.fill_color.getRgb(),
                  points=[(p.x(), p.y()) for p in s.points],
                  object_id=s.shape_id,
                  difficult=s.difficult)

        def format_relation(r):
            return dict(
                predicate=r.predicate,
                rel_id=r.rel_id,
                subject=format_shape(r.sub),
                object=format_shape(r.obj)
            )

        shapes = []
        for shape in self.canvas.shapes:
            if isinstance(shape , Shape):
                shapes.append(format_shape(shape))

        relationships = []
        for r in self.canvas.relationships:
            if isinstance(r, Relationship):
                relationships.append(format_relation(r))

        try:
            self.label_file.save_image_mate_format(self.img_meta_json_file, self.file_path, self.cur_img_idx)
            self.label_file.save_object_anno_format(self.objects_json_file, self.file_path, self.cur_img_idx, shapes)
            self.label_file.save_relationship_anno_format(self.rela_json_file, self.file_path, self.cur_img_idx,
                                                          relationships)
            print('Image:{0} -> Annotation:{1}'.format(self.file_path, annotation_file_path))
            return True
        except LabelFileError as e:
            self.show_message(ERROR, "Error saving label data")
            return False
        # try:
        #     self.label_file.save_object_anno_format()

    def load_file(self, file_path=None):
        self.reset_state()
        self.canvas.setEnabled(False)
        if file_path is None:
            return
        file_path = ustr(file_path)
        unicode_file_path = ustr(file_path)
        unicode_file_path = os.path.abspath(unicode_file_path)
        if unicode_file_path and self.image_list_widget.count() > 0:
            if unicode_file_path in self.m_img_list:
                index = self.m_img_list.index(unicode_file_path)
                file_widget_item = self.image_list_widget.item(index)
                file_widget_item.setSelected(True)
            else:
                self.image_list_widget.clear()
                self.m_img_list.clear()

        if unicode_file_path and os.path.exists(unicode_file_path):
            self.image_data = read(unicode_file_path, None)

        if isinstance(self.image_data, QImage):
            image = self.image_data
        else:
            image = QImage.fromData(self.image_data)

        if image.isNull():
            self.show_message(ERROR, u"<p>Make sure <i>%s</i> is a valid image file." % unicode_file_path)
            self.status("Error reading %s" % unicode_file_path)
            return False
        self.status("Loaded %s" % os.path.basename(unicode_file_path))
        self.image = image
        self.file_path = unicode_file_path
        self.canvas.load_pixmap(QPixmap.fromImage(image))

        self.canvas.setEnabled(True)
        self.anno_obj.setEnabled(True)
        self.anno_res.setEnabled(True)

    def open_anno_dir_dialog(self, dir_path=None, silent=False):
        default_anno_dir = dir_path
        if self.last_anno_dir and os.path.exists(self.last_anno_dir):
            default_anno_dir = self.last_anno_dir
        else:
            default_anno_dir = None

        if silent != True:
            target_anno_dir = ustr(QFileDialog.getExistingDirectory(self,
                                                                    '%s - Open Directory' % __appname__,
                                                                    default_anno_dir,
                                                                    QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks))
        else:
            target_anno_dir = ustr(default_anno_dir)

        if target_anno_dir:
            self.last_anno_dir = target_anno_dir
            self.anno_save_dir = target_anno_dir
            self.load_anno_file(target_anno_dir)
            self.img_meta_json_file = os.path.join(self.anno_save_dir, 'image_data.json')
            self.objects_json_file = os.path.join(self.anno_save_dir, 'objects.json')
            self.rela_json_file = os.path.join(self.anno_save_dir, 'relationships.json')
            self.attr_json_file = os.path.join(self.anno_save_dir, 'attributes.json')

        else:
            self.show_message(ERROR, "标注文件夹路径为空")

    def load_anno_file(self, anno_dir):
        pass

    def load_bounding_box_from_annotation_json(self, json_file):
        if json_file is None:
            return

        if os.path.isfile(json_file) is False:
            return

        if not json_file.lower().endwith('.json'):
            return

    def new_shape(self):
        self.label_dialog = LabelDialog(parent=self, list_item=self.objects_labels_list)
        text = self.label_dialog.pop_up(text=self.prev_label_text)
        self.lastLabel = text

        if text is not None:
            generate_color = generate_color_by_text(text)
            shape = self.canvas.set_last_label(text, generate_color, generate_color)
            self.add_label(shape)
            if self.beginner():  # Switch to edit mode.
                self.canvas.set_editing(True)

            self.set_dirty()
            if text not in self.objects_labels_list:
                self.objects_labels_list.append(text)
        else:
            # self.canvas.undoLastLine()
            self.canvas.reset_all_lines()

        self.anno_obj.setEnabled(True)

    def new_relation(self, relationship):
        self.predicate_dialog = LabelDialog(parent=self, list_item=self.relations_labels_list)
        text = self.predicate_dialog.pop_up(text=self.prev_predicate_text)
        self.lastPredicate = text

        if text is not None:
            relationship.predicate = text
            self.add_predicate(relationship)
            if self.beginner():  # Switch to edit mode.
                self.canvas.set_relating(True)

            self.set_dirty()
            if text not in self.relations_labels_list:
                self.relations_labels_list.append(text)

        else:
            self.canvas.prev_shape = None

    def add_predicate(self, relationship):
        predicate_label = relationship.show_rel()
        if predicate_label:
            item = HashableQListWidgetItem(predicate_label)
            item.setBackground(generate_color_by_text(relationship.predicate))
            self.item_to_relationship[item] = relationship
            self.relationship_to_item[relationship] = item
            self.rels_list_widget.addItem(item)

    def add_label(self, shape):
        shape.paint_label = True
        item = HashableQListWidgetItem(shape.label)
        # item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked)
        item.setBackground(generate_color_by_text(shape.label))
        self.items_to_shapes[item] = shape
        self.shapes_to_items[shape] = item
        self.objs_list_widget.addItem(item)

    def create_shape(self):
        assert self.beginner()
        self.canvas.set_relating(False)
        self.canvas.set_editing(False)
        self.anno_obj.setEnabled(False)
        self.anno_res.setEnabled(True)

    def create_relation(self):
        assert self.beginner()
        self.canvas.set_relating(True)
        self.anno_res.setEnabled(False)
        self.anno_obj.setEnabled(True)

    def paint_canvas(self):
        assert not self.image.isNull(), "cannot paint null image"
        # self.canvas.scale = 0.01 * self.zoom_widget.value()
        # self.canvas.overlay_color = self.light_widget.color()
        self.canvas.label_font_size = int(0.02 * max(self.image.width(), self.image.height()))
        self.canvas.adjustSize()
        self.canvas.update()

    def load_labels(self, shapes):
        s = []
        for label, points, line_color, fill_color, difficult in shapes:
            shape = Shape(label=label)
            for x, y in points:

                # Ensure the labels are within the bounds of the image. If not, fix them.
                x, y, snapped = self.canvas.snap_point_to_canvas(x, y)
                if snapped:
                    self.set_dirty()

                shape.add_point(QPointF(x, y))
            shape.difficult = difficult
            shape.close()
            s.append(shape)

            if line_color:
                shape.line_color = QColor(*line_color)
            else:
                shape.line_color = generate_color_by_text(label)

            if fill_color:
                shape.fill_color = QColor(*fill_color)
            else:
                shape.fill_color = generate_color_by_text(label)

            self.add_label(shape)
        self.update_combo_box()
        self.canvas.load_shapes(s)

    def update_combo_box(self):
        # Get the unique labels and add them to the Combobox.
        items_text_list = [str(self.objs_list_widget.item(i).text()) for i in range(self.objs_list_widget.count())]

        unique_text_list = list(set(items_text_list))
        # Add a null row for showing all the labels
        unique_text_list.append("")
        unique_text_list.sort()

    def reset_state(self):
        self.items_to_shapes.clear()
        self.shapes_to_items.clear()
        self.item_to_relationship.clear()
        self.relationship_to_item.clear()
        self.objs_list_widget.clear()
        self.rels_list_widget.clear()
        self.file_path = None
        self.image_data = None
        self.canvas.reset_state()
        self.label_coordinates.clear()

    def closeEvent(self, e):
        objects_txt = os.path.join(self.os_path, OBJECTS_TXT)
        relations_txt = os.path.join(self.os_path, RELATIONS_TXT)

        with open(objects_txt, 'w') as objtxt:
            for label in self.objects_labels_list:
                objtxt.write(str(label) + '\n')

        with open(relations_txt, 'w') as reltxt:
            for label in self.relations_labels_list:
                reltxt.write(str(label) + '\n')


def read(filename, default=None):
    try:
        reader = QImageReader(filename)
        reader.setAutoTransform(True)
        return reader.read()
    except:
        return default


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
