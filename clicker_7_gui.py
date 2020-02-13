import tkinter
#the gui part for the clicker

class ClickerGui:
    def __init__(self, window_size='normal', settings_dict=None, default_settings_file_path=None, list_box_msg=None, user_settings_file_path=None):
        #some data
        if list_box_msg:
            self.list_box_msg = list_box_msg
        else:
            self.list_box_msg = "--->Bill is awesome<---"

        self.settings_dict = settings_dict
        self.default_settings_file_path = default_settings_file_path
        self.user_settings_file_path = user_settings_file_path
        self.default_settings_dict = {}
        self.window_size = window_size.lower()
        #self.model = 1
        self.decide_model()
        #print("at the beginning: ", self.model)

        #the frame to update the live message
        self.right_top_frame = None
        self.base_window = tkinter.Tk()
        self.base_window.title("Clicker V_0.002 (Bill)")
        #self.window_height, self.window_width = self.get_window_size(self.window_size)
        #self.base_window.geometry("{0}x{1}".format(self.window_width, self.window_height))
        self.base_frame = tkinter.Frame(self.base_window)
        self.live_message_box = None


    def present(self, model=1):
        if model == 1:
            self.model_one()
        elif model == 2:
            self.model_two()


    def decide_model(self):
        if self.window_size == "tiny_vertical":
            self.model = 2
        elif self.window_size == "tiny_horizontal":
            self.model = 3
        else:
            self.model = 1

    def model_two(self):
        print("this is model two")
        self.base_frame.pack(fill='both', expand=True)
        self.base_window.geometry("100x300")

        title_label = tkinter.Label(self.base_frame, text="this is model two")
        title_label.pack()

        left_frame = tkinter.Frame(self.base_frame)
        left_frame.pack(fill='both', expand=True)
        #size_spin_box = tkinter.Spinbox(left_frame, values=("normal", "tiny_horizontal", "tiny_vertical"))

        size_sb_default_value = tkinter.StringVar()
        size_spin_box = tkinter.Spinbox(left_frame, values=("normal", "tiny_vertical", "tiny_horizontal"), textvariable=size_sb_default_value,
                                        command=lambda: self.change_window_size(size_spin_box.get()))
        #set the default value for the spinbox
        window_size_string = ""
        if self.window_size.lower() == "tiny_h":
            window_size_string = "tiny_horizontal"
        elif self.window_size.lower() == "tiny_v":
            window_size_string = "tiny_vertical"
        else:
            window_size_string = "normal"
        size_sb_default_value.set(window_size_string)
        #size_spin_box.grid(row=2,column=0)
        size_spin_box.pack(fill='both', expand=True)



    def model_one(self):
        self.base_frame.pack(fill='both', expand=True)

        #the settings information part of the gui
        settings_frame = tkinter.Frame(self.base_frame)
        settings_frame.pack(side='left', fill='both', expand=True)

        #self.list_box = tkinter.Listbox(self.settings_frame,  yscrollcommand= self.scroll_bar.set)
        scroll_bar = tkinter.Scrollbar(settings_frame)
        list_box = tkinter.Listbox(settings_frame, width=32, height=5, yscrollcommand=scroll_bar.set)
        default_button = tkinter.Button(settings_frame, text="Default Settings", command=self.load_default_settings, bg='red', fg='yellow')

        if self.settings_dict:
            the_message = ""
            line = 2
            list_box.insert(1, self.list_box_msg)
            for key in self.settings_dict:
                the_message = str(line-1) + ": " + key + "_:_ " + str(self.settings_dict[key])
                list_box.insert(line, the_message)
                line = line + 1
        elif self.default_settings_file_path:
            pass

        else:
            list_box.insert(1, self.list_box_msg)
            for i in range(2, 50):
                list_box.insert(i, "this is line: {0} ".format(i))


        default_button.pack(side='bottom', fill='x')
        list_box.pack(side=tkinter.LEFT, fill='both', expand=True, padx=1, pady=1)

        scroll_bar.config(command=list_box.yview)
        scroll_bar.pack(side='right', fill='y')


        #the right side
        right_frame = tkinter.Frame(self.base_frame)
        right_frame.pack(side="right", expand='yes', fill='both')

        #the right top side
        self.right_top_frame = tkinter.Frame(right_frame)
        self.right_top_frame.pack(side="top", expand='yes', fill='both')

        self.live_message_label = tkinter.Label(self.right_top_frame, text="Live Info", bg='gray')
        self.live_message_label.pack(side='top', fill='x', expand=True, padx=2)
        self.live_message(message="-->\nClicker V0.002 is now ready!\n-->\nEmergency Pause: Press other keys 4 times")


        #right middle part
        right_middle_frame = tkinter.Frame(right_frame)
        right_middle_frame.pack(expand=True, fill="both")

        option_label = tkinter.Label(right_middle_frame, text='Other Options', bg='gray')
        option_label.pack(side='top', fill="x", expand=True, pady=2, padx=1)

        option_radio = tkinter.StringVar()
        option_radio.set('no_limit')
        operation_limit_radio = tkinter.Radiobutton(right_middle_frame, text='Cycles Limit', variable=option_radio, value="max_cycles",
                                                    command=lambda: self.radio_options(option_radio))
        operation_limit_radio.pack(anchor='w')

        time_limit_radio = tkinter.Radiobutton(right_middle_frame, text="Time Limit", variable=option_radio, value="time_limit",
                                               command=lambda: self.radio_options(option_radio))
        time_limit_radio.pack(anchor='w')

        no_limit_radio = tkinter.Radiobutton(right_middle_frame, text="No Limit", variable=option_radio, value="no_limit",
                                             command=lambda: self.radio_options(option_radio))
        no_limit_radio.pack(anchor='w')

        #print("the option radio value: ", option_radio.get())






        #right bot part

        right_bot_frame = tkinter.Frame(right_frame)
        right_bot_frame.pack(side='bottom', expand=True, fill="both")






        size_label = tkinter.Label(right_bot_frame, text="Window Size Options", bg="gray")
        size_label.pack(side='top', fill='x', expand=True, pady=2, padx=1)
        #spin_box = tkinter.Spinbox(self.base_frame,from_=0, to=10 )
        size_sb_default_value = tkinter.StringVar()
        size_spin_box = tkinter.Spinbox(right_bot_frame, values=("normal", "tiny_vertical", "tiny_horizontal"), textvariable=size_sb_default_value,
                                        command=lambda: self.change_window_size(size_spin_box.get()))
        #set the default value for the spinbox
        window_size_string = ""
        if self.window_size.lower() == "tiny_h":
            window_size_string = "tiny_horizontal"
        elif self.window_size.lower() == "tiny_v":
            window_size_string = "tiny_vertical"
        else:
            window_size_string = "normal"
        size_sb_default_value.set(window_size_string)
        #size_spin_box.grid(row=2,column=0)
        size_spin_box.pack(fill='both', expand=True)
        #print("the value inside the spinbox is now: ", size_spin_box.get())




        self.base_window.mainloop()



    def radio_options(self, options_variable):
        #print("the value of the options radio is now: ", options_variable.get() )
        message = "the value of the options radio is now:\n" + str(options_variable.get())
        self.live_message_box.destroy()
        self.live_message(message=message)





    def change_window_size(self, size_string):
        #size_string = self.model_one.size_spin_box.get()
        if self.window_size == size_string:
            return 0
        self.window_size = size_string
        self.decide_model()
        #print("spin box triggered", size_string)
        self.refresh_window(self.base_frame)


    def live_message(self, master=None, message="Clicker V0.002 is now ready!"):
        #can't set default argumet with something with self.  don't know why
        master = self.right_top_frame
        self.live_message_box = tkinter.Message(master=master, text=message, bg='red', width=90)
        self.live_message_box.pack(fill='both', expand=True, padx=2, pady=1)



    def load_default_settings(self):
        if self.default_settings_file_path:
            try:
                with open(self.default_settings_file_path, 'r') as f:
                    for line in f:
                        line_list = line.split()
                        if len(line_list[0]) == 0 or len(line_list[1]) == 0:
                            raise ValueError
                        self.default_settings_dict[line_list[0]] = line_list[1]

                print("restoring settings")
                self.settings_dict = self.default_settings_dict
                self.dict_to_file(the_dict=self.settings_dict, result_file_path=self.user_settings_file_path)
                print("the settings_dict is now: ", self.settings_dict)
                #find the child of the base_frame and then destroy them
                self.refresh_window(self.base_frame)
            #redo this part later
            except Exception as e:
                self.error_window("something is wrong with the default settings file (path): {0}".format(str(e)))

        else:
            self.error_window("Default settings file not FOUND!")

    @staticmethod
    def dict_to_file(the_dict, result_file_path):
        empty_it = True
        with open(result_file_path, 'w') as f:
            if empty_it:
                empty_it = False
                f.write("")
            for key in the_dict:
                data = key + " " + str(the_dict[key]) + '\n'
                #print("wrote to file: ", result_file_path, "data: ", data)
                f.write(data)


    def refresh_window(self, refresh_part):
        for child in refresh_part.winfo_children():
            child.destroy()
        print("self.model is now: ", self.model)
        self.present(model=self.model)

    def error_window(self, message):
        #create the error window
        pass

    def get_window_size(self, size_string):
        if size_string == "tiny_v":
            return (200, 100)
        elif size_string == "tiny_h":
            return (100, 200)
        else:
            return (200, 200)

    def close_window(self):
        self.base_window.destroy()

    def get_widget_value(self, widget):
        try:
            return widget.get()
        except Exception as e:
            self.error_window("failed to get value from the widget: " + str(e))
if __name__ == "__main__":
    a_window = ClickerGui("normal")
    a_window.present()
