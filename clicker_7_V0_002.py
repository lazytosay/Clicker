#date: 7/31/2018
import time
import threading
import os
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import sys
#the gui part
import clicker_7_gui

#some global variable
version = "V_0.002"
settings_file_path = "clicker_settings.txt"
default_settings_file_path = "default_clicker_settings.txt"
error_report_path = "error_report.txt"
settings_dict = {}
num_settings = 9
EMERGENCY_STOP = True
EMERGENCY_STOP_COUNT = 0
EMERGENCY_STOP_PRESS_COUNT = 3


class MouseClicker:
    global settings_dict
    def __init__(self, mouse_controller, button=Button.left):
        self.operation_delay = float(settings_dict['delay_between_operations'])
        #print("the delay between operation is: ", float(settings_dict['delay_between_operations']))
        self.button = button
        self.mouse_controller = mouse_controller
        self.clicking = False
        self.program_running = True
        self.cycle_delay = float(settings_dict["delay_between_operations"])
        self.working_hours = int(settings_dict["working_hours"])
        self.working_minutes = int(settings_dict["working_minutes"])
        self.miss_pressed_count = 0
        self.max_cycles = int(settings_dict["max_cycles"])
        #can't save this value...
        #self.start_pause_key = settings_dict["start_pause_key"]
        #self.quit_program_key = settings_dict["quit_program_key"]
        self.start_pause_key = KeyCode(char=str(settings_dict["start_pause_key"]))
        self.quit_program_key = KeyCode(char=str(settings_dict["quit_program_key"]))


    def start_clicking(self):
        self.clicking = True

    def stop_clicking(self):
        self.clicking = False

    def switch_status(self):
        if self.clicking == False:
            self.start_clicking()
        elif self.clicking == True:
            self.stop_clicking()
        else:
            return "unknown self.running status"

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run_program(self):
        while self.program_running:
            while self.clicking:
                self.mouse_controller.click(self.button)
                #since there is only one operation/action, so we don't need it so far
                #time.sleep(self.operation_delay)
                time.sleep(self.cycle_delay)

    def update_operation_delay(self):
        self.operation_delay = settings_dict["delay_between_operations"]

    def update_cycle_delay(self):
        self.cycle_delay = settings_dict["delay_between_cycles"]



#check keyboard
def key_pressed(key):
    global key_board
    global mouse_manager
    global clicker_gui
    global EMERGENCY_STOP_COUNT
    if key == mouse_manager.start_pause_key:
        mouse_manager.switch_status()
        print("current status: ", mouse_manager.clicking)
        EMERGENCY_STOP_COUNT = 0
    elif key == mouse_manager.quit_program_key:
        print("bye bye")
        #the keyboard and mouse_manager will be terminated because daemon=True
        clicker_gui.close_window()
        settings_dict = clicker_gui.settings_dict
        dict_to_file(settings_dict, settings_file_path)
        #mouse_manager.exit()
        #key_board.stop()
        EMERGENCY_STOP_COUNT = 0
    elif EMERGENCY_STOP:
        if EMERGENCY_STOP_COUNT >= EMERGENCY_STOP_PRESS_COUNT:
            mouse_manager.stop_clicking()
        EMERGENCY_STOP_COUNT = EMERGENCY_STOP_COUNT + 1

    message_show = "-->Pressed<--\n" + str(key) + "\n" + "-->Clicking<--\n" + str(mouse_manager.clicking) + "\n-->Emergency Stop: " + str(EMERGENCY_STOP)
    clicker_gui.live_message_box.destroy()
    clicker_gui.live_message(message=message_show)

#try to load the setting_file.txt first, if failed, use the default settings
#and create the file
def main():
    global settings_file_path
    global settings_dict

    #making sure there is a default settings file, since I need to to restore to the default settings
    load_default_settings()
    dict_to_file(settings_dict, default_settings_file_path)

    try:
        settings_dict = file_to_dict(settings_file_path)
        print("the settings_dict", settings_dict)
        if len(settings_dict) < num_settings:
            raise Exception

    except Exception as e:
        print("main: something is wrong: ", e)
        error_handler("main: " + str(e))
        #load_default_settings()
        #create/save to the settings file
        #dict_to_file(settings_dict, default_settings_file_path)
        dict_to_file(settings_dict, settings_file_path)






    global mouse_controller
    global mouse_manager
    global key_board
    mouse_controller = Controller()
    mouse_manager = MouseClicker(mouse_controller)
    key_board = Listener(on_press=key_pressed)
    #so when the window closes, the thread will eventually ends
    key_board.daemon = True

    print("Clicker is now ready")
    a_thread = threading.Thread(target=mouse_manager.run_program, daemon=True)
    a_thread.start()

    key_board.start()

    #the gui part
    global clicker_gui
    clicker_gui = clicker_7_gui.ClickerGui(window_size=settings_dict['size'],settings_dict=settings_dict,
                                            default_settings_file_path=default_settings_file_path,
                                           user_settings_file_path=settings_file_path)
    clicker_gui.present()

    #if the window is closed, the program will then proceed, (the mainloop is now terminated)
    #save the changes to settings file

    settings_dict = clicker_gui.settings_dict
    dict_to_file(settings_dict, settings_file_path)
    mouse_manager.stop_clicking()
    #mouse_manager.exit()
    #key_board.stop()

def load_default_settings():
    global settings_dict
    settings_dict['start_pause_key'] = 's'
    settings_dict['quit_program_key'] = 'e'
    settings_dict['emergency_stop'] = True
    settings_dict['max_cycles'] = 500
    settings_dict['working_minutes'] = 0
    settings_dict['working_hours'] = 0
    settings_dict['delay_between_cycles'] = 0.13
    settings_dict['delay_between_operations'] = 0.1
    settings_dict['size'] = 'normal'


def dict_to_file(a_dictionary, file_path):
    if len(a_dictionary) == 0:
        raise ValueError

    with open(file_path, 'w') as f:
        for key in a_dictionary:
            data = key + " " + str(a_dictionary[key]) + '\n'
            f.write(data)


def file_to_dict(file_path):
    #if file doesn't exist or something is wrong with the values, raise exception
    #so the main function will load the default settings instead
    result_dict = {}
    try:
        #FIXME: how to check empty files
        with open(file_path, 'r') as f:
            for line in f:
                #print("the line", line)
                line_list = line.split()
                #print("the line_list", line_list)
                #FIXME:should I turn them into int??
                if len(line_list[0]) == 0 or len(line_list[1]) == 0:
                    error_handler("the line list: "+str(line_list))
                    raise ValueError
                result_dict[line_list[0]] = line_list[1]
                #print(result_dict)
            print("hi i'm here")
    except Exception as e:
        print("something is wrong: ", e)
        error_handler("file_to_dict: " + str(e))
        raise e
    return result_dict

def error_handler(exception):
    error_message = "==========>\n" + time_stamp() + "\n" + str(exception) + "\n"
    append_to_file(error_report_path, error_message)

def empty_file(file_path):
    with open(file_path, 'w') as f:
        f.write("")
    f.close()

def back_up_file(file_path):
    added_name = "_"+time_stamp()+".bak"
    os.rename(file_path, file_path+added_name)

def append_to_file(file_path, message):
    with open(file_path, 'a') as f:
        f.write("\n" + message + "\n")


def time_stamp():
    time_data = time.strftime("%m_%d_%Y", time.localtime())
    return time_data

#test run
'''
empty_file("hi.txt")
back_up_file("hi.txt")
'''
#file_to_dict("hi.txt")
#append_to_file('hi.txt', 'hello world')
main()








