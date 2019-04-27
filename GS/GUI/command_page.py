try:
    from global_include import *
except ModuleNotFoundError:
    from GUI.global_include import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import itertools
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class MyVideoCapture:

    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        self.video_source = video_source
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.window.mainloop()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

class command_page(tk.Frame):

    def __init__(self, desired_state, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Command Page", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=4, sticky=tk.W, padx=15)

        controller.init_buttons(self)

        self.mav_cmd = [0, 0, 0, 0, 0, 0, 0, 0]

        self.offboard_cycle = itertools.cycle(["Offboard Enabled", "Offboard Disabled"])
        self.arm_cycle = itertools.cycle(["Pixhawk Armed", "Pixhawk Disarmed"])
        self.current_x_values = []
        self.current_y_values = []
        self.current_z_values = []
        self.desired_x_values = []
        self.desired_y_values = []
        self.desired_z_values = []
        self.set_mavlink_commands()
        self.get_current_state()
        self.set_desired_state(desired_state)
        self.graph_state()
        self.plot_video()
        """
        movement_label = tk.Label(self, text="Movement Commands")
        movement_label.grid(row=2, column=2, columnspan=3, sticky='nesw')

        left_btn = tk.Button(self, text="Left",
                            command=lambda: self.movement(cmd, "left"))
        left_btn.grid(row=4, column=2, sticky="nesw")

        right_btn = tk.Button(self, text="Right",
                            command=lambda: self.movement(cmd, "right"))app.frames['command_page']
        right_btn.grid(row=4, column=4, sticky='nesw')

        forward_btn = tk.Button(self, text="Forward",
                            command=lambda: self.movement(cmd, "forward"))
        forward_btn.grid(row=3, column=3, sticky='nesw')

        backward_btn = tk.Button(self, text="Backward",
                            command=lambda: self.movement(cmd, "backward"))
        backward_btn.grid(row=4, column=3, sticky='nesw')
        """
    def plot_video(self):

        #self.vid = cv2.VideoCapture(video_source)
        self.vid = MyVideoCapture()
        self.panel = None
        ret, frame = self.vid.get_frame()

        while not ret:
            ret, frame = self.vid.get_frame()
        image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(frame))

        self.panel = tk.Label(self, image=image)
        self.panel.image = image
        self.panel.grid(row=20, column=201, rowspan=100, padx=15)



        #self.canvas = tk.Canvas(self, width = self.vid.width, height = self.vid.height)#, bg='white')#width = self.vid.width, height = self.vid.height)
        #self.canvas.grid(row=6, column=15, rowspan=100, padx=15)#, columnspan=100, rowspan=100)
        #self.canvas.get_tk_widget().grid(row=601, column=5, columnspan=100, rowspan=100)

    def graph_state(self):

        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(111)#, projection='3d')

        #self.a.plot(float(self.x_current.get()), float(self.y_current.get()), 'bo',
        #        float(self.x_desired.get()), float(self.y_desired.get()), 'ro')
        self.current_x_values.append(float(self.x_current.get()))
        self.current_y_values.append(float(self.y_current.get()))
        self.current_z_values.append(float(self.z_current.get()))
        self.desired_x_values.append(float(self.x_desired.get()))
        self.desired_y_values.append(float(self.y_desired.get()))
        self.desired_z_values.append(float(self.z_desired.get()))
        """
        self.a.plot3D(
            self.current_x_values,
            self.current_y_values,
            self.current_z_values,
            'gray'
        )
        """
        #self.a.axes(projection='3d')
        """
        self.a.plot(
            self.current_x_values,
            self.current_y_values,
            color='blue',
            linestyle='--',
            marker="o"
        )
        self.a.plot(
            self.desired_x_values,
            self.desired_y_values,
            color='green',
            linestyle='--',
            marker="o"
        )
        """
        self.a.set_xlim(-10, 10)
        self.a.set_ylim(-10, 10)
        self.a.set_xlabel("X [m]")
        self.a.set_ylabel("Y [m]")
        self.a.set_xticks(np.arange(-10, 11, 2))
        self.a.set_yticks(np.arange(-10, 11, 2))
        self.a.grid()

        #self.plot_data()

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=20, column=0, rowspan=100, columnspan=200, pady=10)#, columnspan=100, rowspan=100)

    def set_desired_state(self, desired_state):

        curr_label = ttk.Label(self, text="Set Desired State")
        curr_label.grid(row=5, column=0, columnspan=3, sticky=tk.W)

        set_des_but = tk.Button(self, text="Set State",
                            command=lambda: self.sumbit_desired(desired_state))
        set_des_but.grid(row=8, column=1, columnspan=2, sticky='nesw')

        x_des_label = tk.Label(self, text="X [m]")
        x_des_label.grid(row=6, column=0, columnspan=1)

        self.x_desired = tk.StringVar()
        self.x_desired.set("%.2f" % float(self.x_current.get()))
        x_desired = tk.Entry(self, textvariable=self.x_desired, width=8)
        x_desired.grid(row=6, column=1, columnspan=1)

        y_des_label = tk.Label(self, text="Y [m]")
        y_des_label.grid(row=7, column=0, columnspan=1)

        self.y_desired = tk.StringVar()
        self.y_desired.set("%.2f" % float(self.y_current.get()))
        y_desired = tk.Entry(self, textvariable=self.y_desired, width=8)
        y_desired.grid(row=7, column=1, columnspan=1)

        x_des_label = tk.Label(self, text="Z [m]")
        x_des_label.grid(row=6, column=2, columnspan=1)

        self.z_desired = tk.StringVar()
        self.z_desired.set("%.2f" % float(self.z_current.get()))
        z_desired = tk.Entry(self, textvariable=self.z_desired, width=8)
        z_desired.grid(row=6, column=3, columnspan=1)

        x_des_label = tk.Label(self, text="YAW [rad]")
        x_des_label.grid(row=7, column=2, columnspan=1)

        self.yaw_desired = tk.StringVar()
        self.yaw_desired.set(0.0)
        yaw_desired = tk.Entry(self, textvariable=self.yaw_desired, width=8)
        yaw_desired.grid(row=7, column=3, columnspan=1)

    def get_current_state(self):

        curr_label = ttk.Label(self, text="Current State")
        curr_label.grid(row=9, column=0, columnspan=3, sticky=tk.W)

        x_curr_label = tk.Label(self, text="X [m]")
        x_curr_label.grid(row=10, column=0, columnspan=1)

        self.x_current = tk.StringVar()
        self.x_current.set('0.0')
        x_curr_value = tk.Label(self, textvariable=self.x_current)
        x_curr_value.grid(row=10, column=1, columnspan=1)

        y_curr_label = tk.Label(self, text="Y [m]")
        y_curr_label.grid(row=11, column=0, columnspan=1)

        self.y_current = tk.StringVar()
        self.y_current.set('0.0')
        y_curr_value = tk.Label(self, textvariable=self.y_current)
        y_curr_value.grid(row=11, column=1, columnspan=1)

        x_curr_label = tk.Label(self, text="Z [m]")
        x_curr_label.grid(row=12, column=0, columnspan=1)

        self.z_current = tk.StringVar()
        self.z_current.set('0.0')
        z_curr_value = tk.Label(self, textvariable=self.z_current)
        z_curr_value.grid(row=12, column=1, columnspan=1)

        roll_curr_label = tk.Label(self, text="ROLL [rad]")
        roll_curr_label.grid(row=10, column=2, columnspan=1)

        self.roll_current = tk.StringVar()
        self.roll_current.set('0.0')
        roll_curr_value = tk.Label(self, textvariable=self.roll_current)
        roll_curr_value.grid(row=10, column=3, columnspan=1)

        pitch_curr_label = tk.Label(self, text="PITCH [rad]")
        pitch_curr_label.grid(row=11, column=2, columnspan=1)

        self.pitch_current = tk.StringVar()
        self.pitch_current.set('0.0')
        pitch_curr_value = tk.Label(self, textvariable=self.pitch_current)
        pitch_curr_value.grid(row=11, column=3, columnspan=1)

        yaw_curr_label = tk.Label(self, text="YAW [rad]")
        yaw_curr_label.grid(row=12, column=2, columnspan=1)

        self.yaw_current = tk.StringVar()
        self.yaw_current.set('0.0')
        yaw_curr_value = tk.Label(self, textvariable=self.yaw_current)
        yaw_curr_value.grid(row=12, column=3, columnspan=1)

    def set_mavlink_commands(self):

        cmd_label = ttk.Label(self, text="Mavlink Commands")
        cmd_label.grid(row=2, column=0, columnspan=3, sticky=tk.W)

        self.offboard = tk.Button(
            self,
            text="Offboard Disabled",
            command=lambda: self.toggle_offboard(),
            bg = "red"
        )
        self.offboard.grid(row=3, column=0, columnspan=2, sticky='nesw')

        self.arm = tk.Button(
            self,
            text="Pixhawk Disarmed",
            command=lambda: self.toggle_arm(),
            bg = "red"
        )
        self.arm.grid(row=3, column=2, columnspan=2, sticky='nesw')

        self.takeoff = tk.Button(
            self,
            text="Takeoff",
            #command=lambda: self.toggle_pressed(),
            bg = "red",
            width = 15
        )
        self.takeoff.grid(row=3, column=4, columnspan=2, sticky='nesw')

        self.land = tk.Button(
            self,
            text="Land",
            #command=lambda: self.toggle_pressed(),
            bg = "red"
        )
        self.land.grid(row=4, column=1, columnspan=2, sticky='nesw')

        self.go_home = tk.Button(
            self,
            text="Go Home",
            #command=lambda: self.toggle_pressed(),
            bg = "red"
        )
        self.go_home.grid(row=4, column=3, columnspan=2, sticky='nesw')

    def sumbit_desired(self, desired_state):

        desired_state[0] = float(self.x_desired.get())
        desired_state[1] = float(self.y_desired.get())
        desired_state[2] = float(self.z_desired.get())
        desired_state[3] = float(self.yaw_desired.get())

    def toggle_offboard(self):

        state = next(self.offboard_cycle)
        self.offboard['text'] = str(state)

        if (self.offboard['text'] == "Offboard Disabled"):
            #cmd.value = 1
            self.offboard.configure(bg="red")
            self.mav_cmd = [92, 0, 0, 0, 0, 0, 0, 0]
            print("OFFBOARD DISABLED")
        elif (self.offboard['text'] == "Offboard Enabled"):
            #cmd.value = 2
            self.offboard.configure(bg="green")
            self.mav_cmd = [92, 1, 0, 0, 0, 0, 0, 0]
            print("OFFBOARD ENABLED")

    def toggle_arm(self):

        state = next(self.arm_cycle)
        self.arm['text'] = str(state)

        if (self.arm['text'] == "Pixhawk Disarmed"):
            #cmd.value = 1
            self.arm.configure(bg="red")
            self.mav_cmd = [400, 0, 0, 0, 0, 0, 0, 0]
            print("PIXHAWK DISARMED")
        elif (self.arm['text'] == "Pixhawk Armed"):
            #cmd.value = 2
            self.arm.configure(bg="green")
            self.mav_cmd = [400, 1, 0, 0, 0, 0, 0, 0]
            print("PIXHAWK ARMED")

    """
    def movement(self, direction):

        if (direction == "left"):
            #cmd.value = 3
            print("MOVE LEFT")
        elif (direction == "right"):
            #cmd.value = 4
            print("MOVE RIGHT")
        elif (direction == "forward"):
            #cmd.value = 5
            print("MOVE FORWARD")
        elif (direction == "backward"):
            #cmd.value = 6
            print("MOVE BACKWARD")
    """
