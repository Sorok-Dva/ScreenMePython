from PyQt5.QtWidgets import QMainWindow, QColorDialog, QGraphicsView, QGraphicsScene, QPushButton, QGraphicsTextItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItem
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QPen, QPolygonF
from PyQt5.QtCore import Qt, QRectF, QPointF
import os

class Editor(QMainWindow):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.config = self.config_manager.load_config()
        self.initUI()
        self.history = []

    def initUI(self):
        self.setWindowTitle('Image Editor')
        self.setGeometry(100, 100, 800, 600)

        # Create a scene and view
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # Add overlay buttons
        self.add_overlay_buttons()

        self.current_color = QColor(Qt.black)

        # Enable key events
        self.setFocusPolicy(Qt.StrongFocus)

    def add_overlay_buttons(self):
        self.btn_add_text = QPushButton('Add Text', self)
        self.btn_add_text.move(10, 10)
        self.btn_add_text.clicked.connect(self.add_text)

        self.btn_add_rectangle = QPushButton('Add Rectangle', self)
        self.btn_add_rectangle.move(10, 40)
        self.btn_add_rectangle.clicked.connect(self.add_rectangle)

        self.btn_add_ellipse = QPushButton('Add Ellipse', self)
        self.btn_add_ellipse.move(10, 70)
        self.btn_add_ellipse.clicked.connect(self.add_ellipse)

        self.btn_add_arrow = QPushButton('Add Arrow', self)
        self.btn_add_arrow.move(10, 100)
        self.btn_add_arrow.clicked.connect(self.add_arrow)

        self.btn_change_color = QPushButton('Change Color', self)
        self.btn_change_color.move(10, 130)
        self.btn_change_color.clicked.connect(self.change_color)

        self.btn_save_image = QPushButton('Save Image', self)
        self.btn_save_image.move(10, 160)
        self.btn_save_image.clicked.connect(self.save_image)

    def save_image(self):
        # Save the scene to an image
        image = self.scene.itemsBoundingRect()
        image_pixmap = QPixmap(int(image.width()), int(image.height()))
        painter = QPainter(image_pixmap)
        self.scene.render(painter)
        save_path = os.path.join(self.config['default_save_folder'], f"edited_screenshot.{self.config['file_extension']}")
        image_pixmap.save(save_path)
        painter.end()

    def add_text(self):
        text_item = DraggableTextItem("Editable Text")
        text_item.setDefaultTextColor(self.current_color)
        text_item.setFont(QFont('Arial', 16))
        self.scene.addItem(text_item)
        text_item.setPos(100, 100)
        self.history.append(('add', text_item))

    def add_rectangle(self):
        rect_item = ResizableRectItem(QRectF(0, 0, 100, 50))
        rect_item.setPen(QPen(self.current_color))
        self.scene.addItem(rect_item)
        rect_item.setPos(100, 100)
        self.history.append(('add', rect_item))

    def add_ellipse(self):
        ellipse_item = ResizableEllipseItem(QRectF(0, 0, 100, 50))
        ellipse_item.setPen(QPen(self.current_color))
        self.scene.addItem(ellipse_item)
        ellipse_item.setPos(100, 100)
        self.history.append(('add', ellipse_item))

    def add_arrow(self):
        arrow_item = DraggableArrowItem(QLineF(0, 0, 100, 0))
        arrow_item.setPen(QPen(self.current_color, 2))
        self.scene.addItem(arrow_item)
        arrow_item.setPos(100, 100)
        self.history.append(('add', arrow_item))

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_color = color

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for item in self.scene.selectedItems():
                self.scene.removeItem(item)
                self.history.append(('remove', item))
        elif event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.undo()

    def undo(self):
        if not self.history:
            return
        action, item = self.history.pop()
        if action == 'add':
            self.scene.removeItem(item)
        elif action == 'remove':
            self.scene.addItem(item)

class DraggableTextItem(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)

    def wheelEvent(self, event):
        # Adjust font size
        font = self.font()
        font_size = font.pointSize()
        if event.angleDelta().y() > 0:
            font_size += 1
        else:
            font_size -= 1
        font.setPointSize(font_size)
        self.setFont(font)

    def mousePressEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        super().mousePressEvent(event)

class ResizeHandle(QGraphicsRectItem):
    def __init__(self, parent, position):
        super().__init__(-5, -5, 10, 10, parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setBrush(QColor(Qt.black))
        self.setParentItem(parent)
        self.position = position

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.parentItem():
            self.parentItem().prepareGeometryChange()
            new_pos = value.toPointF()
            self.parentItem().resize(new_pos, self.position)
        return super().itemChange(change, value)

class ResizableRectItem(QGraphicsRectItem):
    def __init__(self, rect):
        super().__init__(rect)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.handles = [ResizeHandle(self, pos) for pos in ['topLeft', 'topRight', 'bottomLeft', 'bottomRight']]
        self.updateHandlesPos()

    def resize(self, new_pos, handle):
        rect = self.rect()
        if handle == 'topLeft':
            rect.setTopLeft(new_pos)
        elif handle == 'topRight':
            rect.setTopRight(new_pos)
        elif handle == 'bottomLeft':
            rect.setBottomLeft(new_pos)
        elif handle == 'bottomRight':
            rect.setBottomRight(new_pos)
        self.setRect(rect)
        self.updateHandlesPos()

    def updateHandlesPos(self):
        rect = self.rect()
        self.handles[0].setPos(rect.topLeft())
        self.handles[1].setPos(rect.topRight())
        self.handles[2].setPos(rect.bottomLeft())
        self.handles[3].setPos(rect.bottomRight())

    def wheelEvent(self, event):
        # Adjust border size
        pen = self.pen()
        width = pen.width()
        if event.angleDelta().y() > 0:
            width += 1
        else:
            width -= 1
        pen.setWidth(width)
        self.setPen(pen)

    def mousePressEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        super().mousePressEvent(event)

class ResizableEllipseItem(QGraphicsEllipseItem):
    def __init__(self, rect):
        super().__init__(rect)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.handles = [ResizeHandle(self, pos) for pos in ['topLeft', 'topRight', 'bottomLeft', 'bottomRight']]
        self.updateHandlesPos()

    def resize(self, new_pos, handle):
        rect = self.rect()
        if handle == 'topLeft':
            rect.setTopLeft(new_pos)
        elif handle == 'topRight':
            rect.setTopRight(new_pos)
        elif handle == 'bottomLeft':
            rect.setBottomLeft(new_pos)
        elif handle == 'bottomRight':
            rect.setBottomRight(new_pos)
        self.setRect(rect)
        self.updateHandlesPos()

    def updateHandlesPos(self):
        rect = self.rect()
        self.handles[0].setPos(rect.topLeft())
        self.handles[1].setPos(rect.topRight())
        self.handles[2].setPos(rect.bottomLeft())
        self.handles[3].setPos(rect.bottomRight())

    def wheelEvent(self, event):
        # Adjust border size
        pen = self.pen()
        width = pen.width()
        if event.angleDelta().y() > 0:
            width += 1
        else:
            width -= 1
        pen.setWidth(width)
        self.setPen(pen)

    def mousePressEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        super().mousePressEvent(event)

class DraggableArrowItem(QGraphicsLineItem):
    def __init__(self, line):
        super().__init__(line)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.arrow_head = QPolygonF()
        self.start_pos = self.line().p1()  # Initialisation de start_pos
        self.end_pos = self.line().p2()  # Initialisation de end_pos
        self.updateArrow()
        self.handle_start = ResizeHandle(self, 'start')
        self.handle_start.setPos(self.start_pos)
        self.handle_end = ResizeHandle(self, 'end')
        self.handle_end.setPos(self.end_pos)

    def resize(self, new_pos, handle):
        if handle == 'start':
            self.setStartPos(new_pos)
        elif handle == 'end':
            self.setEndPos(new_pos)
        self.updateHandlesPos()

    def updateHandlesPos(self):
        self.handle_start.setPos(self.start_pos)
        self.handle_end.setPos(self.end_pos)

    def wheelEvent(self, event):
        # Adjust border size
        pen = self.pen()
        width = pen.width()
        if event.angleDelta().y() > 0:
            width += 1
        else:
            width -= 1
        pen.setWidth(width)
        self.setPen(pen)

    def mousePressEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.setEndPos(event.pos())
        super().mouseMoveEvent(event)

    def setStartPos(self, pos):
        self.start_pos = pos
        self.updateArrow()

    def setEndPos(self, pos):
        self.end_pos = pos
        self.updateArrow()

    def setLength(self, length):
        line = self.line()
        angle = line.angle() * 3.14 / 180
        new_end = QPointF(self.start_pos.x() + length * cos(angle), self.start_pos.y() + length * sin(angle))
        line.setP2(new_end)
        self.setLine(line)

    def updateArrow(self):
        line = QLineF(self.start_pos, self.end_pos)
        self.setLine(line)

        # Calculate the arrow head
        arrow_size = 10
        angle = line.angle() * 3.14 / 180
        p1 = self.end_pos
        p2 = QPointF(p1.x() + arrow_size * -cos(angle + 3.14 / 6), p1.y() + arrow_size * -sin(angle + 3.14 / 6))
        p3 = QPointF(p1.x() + arrow_size * -cos(angle - 3.14 / 6), p1.y() + arrow_size * -sin(angle - 3.14 / 6))

        self.arrow_head.clear()
        self.arrow_head << p1 << p2 << p3 << p1

        self.update()

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        painter.setBrush(self.pen().color())
        painter.drawPolygon(self.arrow_head)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    config_manager = ConfigManager("resources/config.json")
    editor = Editor(config_manager)
    editor.show()
    sys.exit(app.exec_())
