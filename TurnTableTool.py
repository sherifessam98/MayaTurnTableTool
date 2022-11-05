from PySide2 import QtGui
from PySide2.QtWidgets import QWidget, QHBoxLayout, QSlider, QLabel, QLineEdit
from PySide2.QtCore import Qt


class Slider(QSlider):
    def __init__(self, minimum, maximum):
        """
        Slider Cnstructor to create the Horizontal
        and vertical sliders
        """
        super(Slider, self).__init__()
        self.slider = QSlider()
        self.label = QLabel("0")
        self.label.setFont(QtGui.QFont("Sanserif", 15))
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)


class Window(QWidget):
    def __init__(self):
        """
        Window UI Consructor. 
        """
        super(Window, self).__init__()
        self.setWindowTitle("Turntable")
        self.top = 200
        self.left = 500
        self.width = 500
        self.height = 150
        self.setGeometry(self.left,
                         self.top, self.width, self.height)
        self.textEdit = QLineEdit()
        self.nameLabel = QLabel()
        self.textEdit.setObjectName("textEdit")
        self.textEdit.resize(10, 10)
        self.h_slider = Slider(1, 100)
        self.h_slider.resize(20, 10)
        self.v_slider = Slider(1, 100)
        self.nameLabel.setText('Angles')
        self.h_slider.label.setText('Horizontal')
        self.v_slider.label.setText('Vertical')
        self.last_h = 0
        self.last_v = 0
        self.get_orientation()
        hbox = QHBoxLayout()
        self.h_slider.valueChanged.connect(self.changed_value_h)
        self.v_slider.valueChanged.connect(self.changed_value_v)
        hbox.addWidget(self.nameLabel)
        hbox.addWidget(self.textEdit)
        hbox.addWidget(self.h_slider.label)
        hbox.addWidget(self.h_slider)
        hbox.addWidget(self.v_slider.label)
        hbox.addWidget(self.v_slider)
        self.setLayout(hbox)
        self.show()

    def get_orientation(self):
        """
         Specifies the orientation of the sliders and their positions.
         h_slider: responsible for horizontal slider.
         v_slider: responsible for vertical slider. 
        """
        self.v_slider.label.setAlignment(Qt.AlignRight)
        self.h_slider.label.setAlignment(Qt.AlignCenter)
        self.v_slider.setOrientation(Qt.Vertical)
        self.h_slider.setOrientation(Qt.Horizontal)

    def changed_value_h(self):
        """
        Displays the change in the horizontal slider's values in the adjacent 
        label's text.
        """
        self.h_slider.label.setText(str(self.h_slider.value()))

    def changed_value_v(self):
        """
        Displays the change in the vertical slider's values in the adjacent 
        label's text.
        """
        self.v_slider.label.setText(str(self.v_slider.value()))

    def GetActiveCamera(self):
        """
        Returns the active camera in the scene.
        """
        perspPanel = cmds.getPanel(withLabel='Persp View')
        ActiveCamera = cmds.modelPanel(perspPanel,
                                       query=True, camera=True)
        return ActiveCamera

    def create_camera(self):
        """
        Duplicates the active camera to be able to control it.
        """
        cmds.duplicate(self.GetActiveCamera(), name='CAM2')
        try:
            cmds.delete("|CMForegroundPlane")
        except:
            pass
        try:
            cmds.delete("|CMBackgroundPlane")
        except:
            pass
        i = 0
        while cmds.objExists("shot_" + str(i)):
            try:
                cmds.delete("|" + "shot_" + str(i) + "_ImagePlane")
            except:
                pass
            i = i + 1

        cmds.camera('CAM2', edit=True,
                    startupCamera=False,
                    displayResolution=True)
        cmds.select('CAM2')

    def change_camera_h(self):
        """
        Moves the created camera horizontally.
        """
        cameras = cmds.ls(type='camera', l=True) or []
        p = cmds.camera(cameras[0], q=True, p=True)
        val = self.h_slider.value()
        distance = val - self.last_h
        cmds.move(p[0], p[1], p[2] + distance,
                  cameras[0], absolute=True)
        self.last_h = val

    def change_camera_v(self):
        """
        Moves the created camera vertically.
        """
        cameras = cmds.ls(type='camera', l=True) or []
        p = cmds.camera(cameras[0], q=True, p=True)
        val = self.v_slider.value()
        distance = val - self.last_v
        cmds.move(p[0], p[1] + distance, p[2], cameras[0],
                  absolute=True)
        self.last_v = val


def startup_camera():
    """
    Checks if a camera is already created and connects
    sliders' values with camera's movement
    """
    nonStartup = [c for c in cmds.ls(cameras=True) 
                  if not cmds.camera(c, q=True, startupCamera=True)]

    if not nonStartup:
        hello.create_camera()

    hello.h_slider.valueChanged.connect(hello.change_camera_h)
    hello.v_slider.valueChanged.connect(hello.change_camera_v)
    

hello = Window()
hello.show()
startup_camera()
