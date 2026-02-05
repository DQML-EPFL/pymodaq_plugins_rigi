import pyautogui
from pyautogui import Point
import time
import keyboard


class Click_and_Write_Master:



    def __init__(self, wait_time = 0.1):
        self.sequence : list[Action] = []
        self.click_precision = 3
        self.wait_time = wait_time

    def get_current_value(self):
        return -1
    
    def open_communication(self):
        return True

    def close_communication(self):
        pass


    # ------ Moving and defining ------

    def execute(self):
        for action in self.sequence:
            action.action()
            time.sleep(self.wait_time)

    def define_sequence(self):
        print(" ---------------- Define Sequence ----------------")
        print(" - Press 'Ctrl' to add points.")
        print(" - Press 'Shift' to input a text to write.")
        print(" - Press 'Esc' to stop the sequence.")
        print(" -------------------------------------------------")

        self.sequence = []
        record = True
        while record:
            action = None
            if keyboard.is_pressed('ctrl'):
                position = pyautogui.position()
                if self.check_position(position):
                    print("Added Click Action at : ", position)
                    action = Click( position = position )

            elif keyboard.is_pressed('Shift'):
                print(" Recording text, press 'Enter' to confirm.")
                text = input("Enter Text Here : ")
                print(" Added write action with text : ", text)
            
                action = Write( text = text )
            
            elif keyboard.is_pressed('esc'):
                print(" -- 'esc' pressed. Exiting loop.")
                record = False

            if action: self.sequence.append(action)
        
        
        print(" -------------------------------------------------")
        return self.sequence

    def check_position(self, pos):
        for action in self.sequence:
            if type(action) is Click:
                if self.round(action.position) == self.round(pos):
                    return False
        
        return True

    def round(self, point):
        return Point(point.x//self.click_precision * self.click_precision, 
                     point.y//self.click_precision * self.click_precision)

    def show_sequence(self):
        for action in self.sequence:
            print(action)







class Action:

    def action(self): 
        raise NotImplementedError("Action must be defined for class")

    def __str__(self):
        raise NotImplementedError("Print must be defined for class")

class Click(Action):
    def __init__(self, position : Point):
        self.position = position

    def action(self):
        pyautogui.click(x=self.position[0], 
                        y=self.position[1])

    def __str__(self):
        return f"Click at ({self.position.x},{self.position.y})" 




class Write(Action):

    def __init__(self, text):
        self.text = text
    
    def action(self):
        keyboard.write(self.text)
    
    def __str__(self):
        return f"Write down : {self.text}"






def main():
    master = Click_and_Write_Master()
    master.define_sequence()

    master.show_sequence()

    master.execute()


if __name__=="__main__":
    main()
    

