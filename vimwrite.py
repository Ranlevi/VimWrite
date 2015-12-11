import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

#modal editor. start in normal mode, press i to insert mode.
#vim commands to implement:
# movement: hjkl, gg, G, A, ctrl+F, ctrl+B
# commands: :w, :wq, :q, open in menu, new file in menu
# operators: dd, ciw
# select: yank, delete,  
# normal: u, paste 


class Main(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)

        self.insert_mode = False
        self.normal_mode = True
        self.visual_mode = False

        #self.operator_recived = False
        self.pressed_keys = []
        self.copied_text = None
         
        self.initUI()

    def initMenubar(self):

        menubar = self.menuBar()
        self.file_menu = menubar.addMenu("File")

    def initStatusBar(self):

        self.mode_label = QtGui.QLabel()
        self.mode_label.setText("Mode: Normal")
        self.statusBar().addWidget(self.mode_label)

    def open_file(self):

        cursor = self.text.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        cursor.removeSelectedText()

        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Select a Text File to open')

        with open(file_name) as f:
            text = f.read()
            cursor.insertText(text)

        self.text.setTextCursor(cursor)

    def new_file(self):
        
        cursor = self.text.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        cursor.removeSelectedText()

        self.text.setTextCursor(cursor)
            
    def keyPressEvent(self, event):

        key = event.text()
        print (key)
        print (event.key())
        print (event.nativeModifiers())

        #cursor = self.text.textCursor()
        if self.normal_mode:

            if key=='i' or key=='ן':

                #if self.operator_recived: #Motion expected
                #    pass

                #else:

                self.insert_mode = True
                self.normal_mode = False

                self.text.setReadOnly(False)
                self.mode_label.setText("Mode: Insert")

            elif key=="h":
                self.text.moveCursor(QtGui.QTextCursor.Left)
                self.text.setTextInteractionFlags(Qt.TextSelectableByKeyboard)

            elif key=="l":
                self.text.moveCursor(QtGui.QTextCursor.Right)
                self.text.setTextInteractionFlags(Qt.TextSelectableByKeyboard)

            elif key=="j":
                self.text.moveCursor(QtGui.QTextCursor.Up)
                self.text.setTextInteractionFlags(Qt.TextSelectableByKeyboard)

            elif key=="k":
                self.text.moveCursor(QtGui.QTextCursor.Up)
                self.text.setTextInteractionFlags(Qt.TextSelectableByKeyboard)

            elif key=="x":

                cursor = self.text.textCursor()
                cursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor, 1)
                self.copied_text = cursor.selectedText()
                cursor.deleteChar()
                self.text.setTextCursor(cursor)

            elif key=="p":

                cursor = self.text.textCursor()
                cursor.insertText(self.copied_text)
                self.text.setTextCursor(cursor)

            elif key==":":
                
                command, cmd_entered = QtGui.QInputDialog.getText(self, 'Command Dialog', 'Enter Command')
                   
                if cmd_entered:
                    if command=="w" or command=="'":
                        f = open('test.txt','w')
                        f.write(self.text.document().toPlainText())
                        f.close()
                        self.mode_label.setText("Mode: Normal. File Saved.")

                    if command=="q":
                       self.close()

            elif key=="g":
                
                if self.pressed_keys == ["g"]:
                    self.text.moveCursor(QtGui.QTextCursor.Start)
                    self.text.setTextInteractionFlags(Qt.TextSelectableByKeyboard)

                    self.pressed_keys = []
                else:
                    self.pressed_keys.append("g")

            elif key=="G":
                self.text.moveCursor(QtGui.QTextCursor.End)
                self.text.setTextInteractionFlags(Qt.TextSelectableByKeyboard)

            elif event.key()==Qt.Key_F and event.nativeModifiers()==4: #ctrl F
                cursor = self.text.textCursor()
                cursor.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveAnchor, 30)
                self.text.setTextCursor(cursor)

            elif event.key()==Qt.Key_B and event.nativeModifiers()==4: #ctrl B
                cursor = self.text.textCursor()
                cursor.movePosition(QtGui.QTextCursor.Up, QtGui.QTextCursor.MoveAnchor, 30)
                self.text.setTextCursor(cursor)




           # elif key=="c":
           #     self.operator_recived = True
           #     self.mode_label.setText("Mode: Normal. Motion Exected.")

        elif self.insert_mode:

            if event.key() == Qt.Key_Escape:

                self.insert_mode = False
                self.normal_mode = True
                self.text.setReadOnly(True)
                self.mode_label.setText("Mode: Normal")

        #self.text.setTextCursor(cursor) 

        #self.text.setTextInteractionFlags(Qt.TextEditable)

    #def delete_mode(self):
    #    if self.mode == "Normal":
    #        
    #        if self.in_delete_mode:
    #            cursor = self.text.textCursor()
    #            cursor.select(QtGui.QTextCursor.LineUnderCursor)
    #            self.copied_text = cursor.selectedText()
    #            cursor.removeSelectedText()
    #            self.text.setTextCursor(cursor) 
    #            
    #        else:
    #            self.in_delete_mode = True

    def initUI(self):

        self.text = QtGui.QTextEdit(self)
        self.text.setReadOnly(True)

        self.setCentralWidget(self.text)

        self.initMenubar()
        self.initStatusBar()

        open_file_action = QtGui.QAction('&Open File...',self)
        open_file_action.triggered.connect(self.open_file)
        self.file_menu.addAction(open_file_action)

        new_file_action = QtGui.QAction('&New File',self)
        new_file_action.triggered.connect(self.new_file)
        self.file_menu.addAction(new_file_action)


        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,1030,800)

        self.setWindowTitle("VimWriter")

def main():

    app = QtGui.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


    
