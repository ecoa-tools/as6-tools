# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

import subprocess
import os
import shutil

def create_window(master, master_name, master_icon, app_width, app_height):
    master.title(master_name)
    master.iconphoto(True, master_icon)
    master.resizable(False, False)
    app_width = app_width
    app_height = app_height
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    x = int((screen_width / 2) - (app_width / 2))
    y = int((screen_height / 2) - (app_height / 2))
    master.geometry("{}x{}+{}+{}".format(app_width, app_height, x, y))


class ECOA_Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.tool = None
        self.file_xml = None
        self.exe_checker = None
        self.file_conf = None
        self.dir_output = None
        self.var_force = None
        self.val_level = None
        self.verbose_level = None
        self.dir_templates = None
        self.verbose = None
        self.log_level = None
        self.userid = None
        self.debug = None
        self.coverage = None
        
        self.button_exe = None
        self.button_stop = None
        self.exe_process = None
        
        # ECOA images
        self.ecoa_icon = ImageTk.PhotoImage(Image.open('images/ECOA_Icon.png').resize((100,130)))
        self.workflow_img = ImageTk.PhotoImage(Image.open('images/Workflow.png').resize((400,360)))
        self.exvt_icon = ImageTk.PhotoImage(Image.open('images/EXVT_Icon.png').resize((100,70)))
        self.exvt_label = 'EXVT - ECOA CHECKER'
        self.edt_icon = ImageTk.PhotoImage(Image.open('images/EDT_Icon.png').resize((100,70)))
        self.edt_label = 'EDT - ECOA EDITOR'
        self.asctg_icon = ImageTk.PhotoImage(Image.open('images/ASCTG_Icon.png').resize((100,70)))
        self.asctg_label = 'ASCTG - ECOA TEST GENERATOR'
        self.mscigt_icon = ImageTk.PhotoImage(Image.open('images/MSCIGT_Icon.png').resize((100,70)))
        self.mscigt_label = 'MSCIGT - ECOA SKELETON GENERATOR'
        self.csmgvt_icon = ImageTk.PhotoImage(Image.open('images/CSMGVT_Icon.png').resize((100,70)))
        self.csmgvt_label = 'CSMGVT - ECOA CORK GENERATOR'
        self.ldp_icon = ImageTk.PhotoImage(Image.open('images/LDP_Icon.png').resize((100,70)))
        self.ldp_label = 'LDP - ECOA ENGINE'
        
        # Creation of the icon on the main window
        self.create_ecoa_icon(self)
        self.create_worflow_img()
        self.create_icon_button(self.exvt_icon, self.exvt_label, 0.1, self.exvt_window)
        self.create_icon_button(self.edt_icon, self.edt_label, 0.25, '')
        self.create_icon_button(self.asctg_icon, self.asctg_label, 0.40, self.asctg_window)
        self.create_icon_button(self.mscigt_icon, self.mscigt_label, 0.55, self.mscigt_window)
        self.create_icon_button(self.csmgvt_icon, self.csmgvt_label, 0.70, self.csmgvt_window)
        self.create_icon_button(self.ldp_icon, self.ldp_label, 0.85, self.ldp_window)
        
        self.pack(fill=BOTH, expand=1)
        self.create_exit_button()

    # Recurrent mecanism
    def create_ecoa_icon(self, master):
        label = Label(master, image=self.ecoa_icon)
        label.place(relx=0.98, rely=0.01, anchor='ne')
        
    def create_worflow_img(self):
        label = Label(self, image=self.workflow_img)
        label.place(relx=0.98, rely=0.6, anchor='e')
        
    def create_icon_button(self, img_icon, icon_label, y, command):
        button = Button(self, image=img_icon, command=command)
        button.place(relx=0.02, rely=y, anchor='w')
        label = Label(self, text=icon_label, justify='left')
        label.place(relx=0.15, rely=y, anchor='w')
        
    def create_exit_button(self):
        button_quit = Button(self, text='Exit Program', command=self.quit)
        button_quit.place(relx=0.5, rely=1.0, anchor='s')

    def run_tool(self):
        command = [self.tool, '-p', self.file_xml]
        if self.exe_checker:
            command.append('-k')
            command.append(self.exe_checker)
        elif self.tool != 'ecoa-exvt':
            command.append('-k')
            command.append('ecoa-exvt')
        if self.file_conf:
            command.append('-c')
            command.append(self.file_conf)
        if self.dir_output:
            command.append('-o')
            command.append(self.dir_output)
        if self.var_force == 1:
            command.append('-f')
        if self.val_level:
            command.append('-l')
            command.append(self.val_level)
        if self.verbose_level:
            command.append('-v')
            command.append(self.verbose_level)
        if self.dir_templates:
            command.append('-t')
            command.append(self.dir_templates)
        if self.verbose == 1:
            command.append('-v')
        if self.log_level:
            command.append('-l')
            command.append(self.log_level)
        if self.userid:
            command.append('-u')
            command.append(self.userid)
        if self.debug:
            command.append('-g')
        if self.coverage:
            command.append('-c')
        subprocess.run(command)

    def create_launch_button(self, master, compile_tool=False):
        button_launch = Button(master, text="Launch", command=self.run_tool)
        if compile_tool:
            button_launch.place(relx=0.35, rely=0.95, anchor='s')
        else:
            button_launch.place(relx=0.49, rely=0.95, anchor='s')

    def help_command(self):
        subprocess.run([self.tool, '-h'])

    def create_help_button(self, master):
        button_help = Button(master, text="Help?", command=self.help_command)
        button_help.place(relx=0.95, rely=0.95, anchor='se')

    def compile_command(self, ldp_tool):
        current_dir = os.getcwd()
        if ldp_tool:
            os.chdir(os.path.split(self.file_xml)[0])
            project_path = os.path.split(self.file_xml)[0]
            project_dir = os.path.basename(os.path.normpath(project_path))
            os.chdir(os.path.join('..', '..', 'centos'))
            subprocess.run(['make', 'distclean', 'all_ecoa', f'ECOA_PROJECT={project_dir}'])
        else:
            os.chdir(self.dir_output)
            if not os.path.isdir("build"):
                os.makedirs("build")
            os.chdir("build")
            subprocess.run(['cmake3', '..', '-D64BIT_SUPPORT=ON'])
            subprocess.run(['make'])
        os.chdir(current_dir)

    def create_compile_button(self, master, ldp_tool=False):
        button_compile = Button(master, text="Compile", command=lambda:
                                self.compile_command(ldp_tool))
        button_compile.place(relx=0.58, rely=0.95, anchor='se')

    def exe_command(self, master, ldp_tool):
        self.create_stop_button(master)
        current_dir = os.getcwd()
        if ldp_tool:
            os.chdir(os.path.split(self.file_xml)[0])
            project_path = os.path.split(self.file_xml)[0]
            project_dir = os.path.basename(os.path.normpath(project_path))
            os.chdir(os.path.join('..', '..', 'centos', 'app.rootfs', f'{project_dir}', '6-Output', 'bin'))
            self.exe_process = subprocess.Popen(['./platform'])
        else:
            os.chdir(os.path.join(self.dir_output, 'build'))
            self.exe_process = subprocess.Popen(['./csm'])
        os.chdir(current_dir)

    def stop_exe_process(self, master):
        if self.exe_process:
            self.exe_process.terminate()
            self.exe_process.kill()
            self.exe_process = None
            self.create_exe_button(master)

    def create_exe_button(self, master, ldp_tool=False):
        if self.button_stop:
            self.button_stop.destroy()
        self.button_exe = Button(master, text="Execute", command=lambda:
                                self.exe_command(master, ldp_tool))
        self.button_exe.place(relx=0.74, rely=0.95, anchor='se')

    def create_stop_button(self, master):
        if self.button_exe:
            self.button_exe.destroy()
        self.button_stop = Button(master, text="STOP", command=lambda: self.stop_exe_process(master))
        self.button_stop.place(relx=0.74, rely=0.95, anchor='se')

    # EXVT PART
    def callback_exvt(self, event):
        self.tool = 'ecoa-exvt'
        self.file_xml = self.file_xml_exvt
        self.exe_checker = None
        self.file_conf = None
        self.dir_output = None
        self.var_force = None
        self.val_level = self.combo.get()
        self.verbose_level = self.combo_verbose.get()
        self.dir_templates = None
        self.verbose = None
        self.log_level = None
        self.userid = None
        self.debug = None
        self.coverage = None

    def open_xml_exvt(self):
        self.file_xml_exvt = filedialog.askopenfilename(initialdir = ".",
                                                    title = "Select an ECOA xml project file",
                                                    filetypes = [("XML files","*.xml")]
                                                    )
        if self.file_xml_exvt:
            self.label_xml_exvt.configure(text="Input XML file opened :\n" 
            + os.path.split(self.file_xml_exvt)[1])
            self.label_xml_exvt.place(relx=0.5, rely=0.5, anchor='c', width=300, height=50)

    def exvt_window(self):
        self.file_xml_exvt = None
        

        new_exvt = Toplevel(self)
        create_window(new_exvt, self.exvt_label, self.exvt_icon, 500, 300)

        label = Label(new_exvt, image=self.exvt_icon)
        label.place(relx=0.02, rely=0.15, anchor='w')
        self.create_ecoa_icon(new_exvt)

        self.label_xml_exvt = Label(new_exvt, justify='center')
        
        combo_label = Label(new_exvt, text='Validation level :')
        combo_label.place(relx=0.02, rely=0.75, anchor='w')
        self.combo = ttk.Combobox(new_exvt, state="readonly", values=["0", "1", "2", "3", "4", "5"], width=2)
        self.combo.current(0)
        self.combo.place(relx=0.23, rely=0.75, anchor='w')
        
        combo_verbose_label = Label(new_exvt, text='Verbose level :')
        combo_verbose_label.place(relx=0.02, rely=0.65, anchor='w')
        self.combo_verbose = ttk.Combobox(new_exvt, state="readonly", values=["0", "1", "2", "3", "4"], width=2)
        self.combo_verbose.current(0)
        self.combo_verbose.place(relx=0.23, rely=0.65, anchor='w')

        button_xml_exvt = Button(new_exvt, text="Open an ECOA xml file", command=self.open_xml_exvt) 
        button_xml_exvt.place(relx=0.5, rely=0.4, anchor='c')

        self.create_launch_button(new_exvt)
        self.create_help_button(new_exvt)
        
        new_exvt.bind("<Button-1>", self.callback_exvt)

    # ASCTG PART
    def callback_asctg(self, event):
        self.tool = 'ecoa-asctg'
        self.file_xml = self.file_xml_asctg
        self.exe_checker = self.file_checker_asctg
        self.file_conf = self.file_conf_asctg
        self.dir_output = self.dir_output_asctg
        self.var_force = self.var_force_asctg.get()
        self.val_level = None
        self.verbose_level = self.combo_verbose.get()
        self.dir_templates = None
        self.verbose = None
        self.log_level = None
        self.userid = None
        self.debug = None
        self.coverage = None

    def open_xml_asctg(self):
        self.file_xml_asctg = filedialog.askopenfilename(initialdir = ".",
                                                    title = "Select an ECOA xml project file",
                                                    filetypes = [("XML files","*.project.xml")]
                                                    )
        if self.file_xml_asctg:
            self.label_xml_asctg.configure(text="Input XML file opened :\n" 
            + os.path.split(self.file_xml_asctg)[1])
            self.label_xml_asctg.place(relx=0.5, rely=0.17, anchor='c', width=300, height=50)

    def open_conf_asctg(self):
        self.file_conf_asctg = filedialog.askopenfilename(initialdir = ".",
                                                    title = "Select a configuration file",
                                                    filetypes = [("Configuration files","*.config.xml")]
                                                    )
        if self.file_conf_asctg:
            self.label_conf_asctg.configure(text="Input checker used :\n" 
            + os.path.split(self.file_conf_asctg)[1])
            self.label_conf_asctg.place(relx=0.5, rely=0.34, anchor='c', width=300, height=50)

    def open_checker_asctg(self):
        self.file_checker_asctg = filedialog.askopenfilename(initialdir = ".",
                                                    title = "Select a checker executable",
                                                    filetypes = [("Checker executable","*.*")]
                                                    )
        if self.file_checker_asctg:
            self.label_check_asctg.configure(text="Input checker used :\n" 
            + os.path.split(self.file_checker_asctg)[1])

    def open_output_asctg(self):
        self.dir_output_asctg = filedialog.askdirectory()
        if self.dir_output_asctg:
            self.label_output_asctg.configure(text="Output directory given :\n" 
            + os.path.basename(os.path.normpath(self.dir_output_asctg)))
            self.label_output_asctg.place(relx=0.5, rely=0.67, anchor='c', width=300, height=50)

    def asctg_window(self):
        self.file_xml_asctg = None
        self.file_conf_asctg = None
        self.file_checker_asctg = None
        self.dir_output_asctg = None
        self.var_force_asctg = IntVar()

        new_asctg = Toplevel(self)
        create_window(new_asctg, self.asctg_label, self.asctg_icon, 500, 450)

        label = Label(new_asctg, image=self.asctg_icon)
        label.place(relx=0.02, rely=0.12, anchor='w')
        self.create_ecoa_icon(new_asctg)

        self.label_xml_asctg = Label(new_asctg, justify='center')
        self.label_conf_asctg = Label(new_asctg, justify='center')
        self.label_check_asctg = Label(new_asctg, justify='center')
        self.label_output_asctg = Label(new_asctg, justify='center')
        
        if shutil.which('ecoa-exvt'):
            self.label_check_asctg.configure(text="Default input checker used :\n ecoa-exvt")
            self.label_check_asctg.place(relx=0.5, rely=0.51, anchor='c', width=200, height=50) 

        checkbox_force_asctg = Checkbutton(new_asctg, text="Force existing files overwrite", variable=self.var_force_asctg,
        onvalue=1, offvalue=0)
        checkbox_force_asctg.place(relx=0.02, rely=0.78, anchor='w')

        button_openfile_xml = Button(new_asctg, text="Open an ECOA xml file", command=self.open_xml_asctg)
        button_openfile_xml.place(relx=0.5, rely=0.1, anchor='c')
        button_openfile_conf = Button(new_asctg, text="Open a configuration file", command=self.open_conf_asctg)
        button_openfile_conf.place(relx=0.5, rely=0.27, anchor='c')
        button_openfile_check = Button(new_asctg, text="Open a checker executable file", command=self.open_checker_asctg)
        button_openfile_check.place(relx=0.5, rely=0.44, anchor='c')
        button_dir_output = Button(new_asctg, text="Choose an output directory", command=self.open_output_asctg)
        button_dir_output.place(relx=0.5, rely=0.60, anchor='c')
        
        combo_verbose_label = Label(new_asctg, text='Verbose level :')
        combo_verbose_label.place(relx=0.02, rely=0.73, anchor='w')
        self.combo_verbose = ttk.Combobox(new_asctg, state="readonly", values=["0", "1", "2", "3", "4"], width=2)
        self.combo_verbose.current(0)
        self.combo_verbose.place(relx=0.23, rely=0.73, anchor='w')

        self.create_launch_button(new_asctg)
        self.create_help_button(new_asctg)
        
        new_asctg.bind("<Button-1>", self.callback_asctg)
    
    # MSCIGT PART
    def callback_mscigt(self, event):
        self.tool = 'ecoa-mscigt'
        self.file_xml = self.file_xml_mscigt
        self.exe_checker = self.file_checker_mscigt
        self.file_conf = None
        self.dir_output = self.dir_output_mscigt
        self.var_force = self.var_force_mscigt.get()
        self.val_level = None
        self.verbose_level = None
        self.dir_templates = self.dir_templates_mscigt
        self.verbose = self.verbose_mscigt.get()
        self.log_level = self.combo_log.get()
        self.userid = None
        self.debug = None
        self.coverage = None

    def open_xml_mscigt(self):
        self.file_xml_mscigt = filedialog.askopenfilename(initialdir = ".",
                                                    title = "Select an ECOA xml project file",
                                                    filetypes = [("XML files","*.xml")]
                                                    )
        if self.file_xml_mscigt:
            self.label_xml_mscigt.configure(text="Input XML file opened :\n" 
            + os.path.split(self.file_xml_mscigt)[1])
            self.label_xml_mscigt.place(relx=0.5, rely=0.2, anchor='c', width=300, height=50)

    def open_checker_mscigt(self):
        self.file_checker_mscigt = filedialog.askopenfilename(initialdir = ".",
                                                    title = "Select a checker executable",
                                                    filetypes = [("Checker executable","*.*")]
                                                    )
        if self.file_checker_mscigt:
            self.label_check_mscigt.configure(text="Input checker used :\n" 
            + os.path.split(self.file_checker_mscigt)[1])
            self.label_check_mscigt.place(relx=0.5, rely=0.4, anchor='c', width=300, height=50)

    def open_output_mscigt(self):
        self.dir_output_mscigt = filedialog.askdirectory()
        if self.dir_output_mscigt:
            self.label_output_mscigt.configure(text="Output directory given :\n" 
            + os.path.basename(os.path.normpath(self.dir_output_mscigt)))
            self.label_output_mscigt.place(relx=0.5, rely=0.6, anchor='c', width=300, height=50)

    def open_templates_mscigt(self):
        self.dir_templates_mscigt = filedialog.askdirectory()
        if self.dir_templates_mscigt:
            self.label_templates_mscigt.configure(text="Templates directory given :\n"
            + os.path.basename(os.path.normpath(self.dir_templates_mscigt)))
            self.label_templates_mscigt.place(relx=0.5, rely=0.8, anchor='c', width=300, height=50)

    def mscigt_window(self):
        self.file_xml_mscigt = None
        self.file_checker_mscigt = None
        self.dir_output_mscigt = None
        self.dir_templates_mscigt = None
        self.var_force_mscigt = IntVar()
        self.verbose_mscigt = IntVar()

        new_mscigt = Toplevel(self)
        create_window(new_mscigt, self.mscigt_label, self.mscigt_icon, 500, 300)

        label = Label(new_mscigt, image=self.mscigt_icon)
        label.place(relx=0.02, rely=0.15, anchor='w')
        self.create_ecoa_icon(new_mscigt)

        self.label_xml_mscigt = Label(new_mscigt, justify='center')
        self.label_check_mscigt = Label(new_mscigt, justify='center')
        self.label_output_mscigt = Label(new_mscigt, justify='center')
        self.label_templates_mscigt = Label(new_mscigt, justify='center')

        if shutil.which('ecoa-exvt'):
            self.label_check_mscigt.configure(text="Default input checker used :\n ecoa-exvt")
            self.label_check_mscigt.place(relx=0.5, rely=0.4, anchor='c', width=200, height=50) 

        checkbox_force_mscigt = Checkbutton(new_mscigt, text="Force existing files overwrite", variable=self.var_force_mscigt,
        onvalue=1, offvalue=0)
        checkbox_force_mscigt.place(relx=0.02, rely=0.9, anchor='w')
        
        checkbox_verbose_mscigt = Checkbutton(new_mscigt, text="Verbose mode", variable=self.verbose_mscigt,
        onvalue=1, offvalue=0)
        checkbox_verbose_mscigt.place(relx=0.6, rely=0.9, anchor='w')

        button_openfile_xml = Button(new_mscigt, text="Open an ECOA xml file", command=self.open_xml_mscigt)
        button_openfile_xml.place(relx=0.5, rely=0.1, anchor='c')
        button_openfile_check = Button(new_mscigt, text="Open a checker executable file", command=self.open_checker_mscigt)
        button_openfile_check.place(relx=0.5, rely=0.3, anchor='c')
        button_dir_output = Button(new_mscigt, text="Choose an output directory", command=self.open_output_mscigt)
        button_dir_output.place(relx=0.5, rely=0.5, anchor='c')
        button_dir_templates = Button(new_mscigt, text="Choose a templates directory", command=self.open_templates_mscigt)
        button_dir_templates.place(relx=0.5, rely=0.7, anchor='c')

        combo_log_label = Label(new_mscigt, text='Log level :')
        combo_log_label.place(relx=0.02, rely=0.5, anchor='w')
        self.combo_log = ttk.Combobox(new_mscigt, state="readonly", values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], width=6)
        self.combo_log.current(1)
        self.combo_log.place(relx=0.15, rely=0.5, anchor='w')

        self.create_launch_button(new_mscigt)
        self.create_help_button(new_mscigt)

        new_mscigt.bind("<Button-1>", self.callback_mscigt)

    # CSMGVT PART
    def callback_csmgvt(self, event):
        self.tool = 'ecoa-csmgvt'
        self.file_xml = self.file_xml_csmgvt
        self.exe_checker = self.file_checker_csmgvt
        self.file_conf = None
        self.dir_output = self.dir_output_csmgvt
        self.var_force = self.var_force_csmgvt.get()
        self.val_level = None
        self.verbose_level = None
        self.dir_templates = None
        self.verbose = self.verbose_csmgvt.get()
        self.log_level = self.combo_log.get()
        self.userid = None
        self.debug = None
        self.coverage = None

    def open_xml_csmgvt(self):
        self.file_xml_csmgvt = filedialog.askopenfilename(initialdir = ".",
                                                    title = "Select an ECOA xml project file",
                                                    filetypes = [("XML files","*.xml")]
                                                    )
        if self.file_xml_csmgvt:
            self.label_xml_csmgvt.configure(text="Input XML file opened :\n" 
            + os.path.split(self.file_xml_csmgvt)[1])
            self.label_xml_csmgvt.place(relx=0.5, rely=0.2, anchor='c', width=300, height=50)

    def open_checker_csmgvt(self):
        self.file_checker_csmgvt = filedialog.askopenfilename(initialdir = ".",
                                                    title = "Select a checker executable",
                                                    filetypes = [("Checker executable","*.*")]
                                                    )
        if self.file_checker_csmgvt:
            self.label_check_csmgvt.configure(text="Input checker used :\n" 
            + os.path.split(self.file_checker_csmgvt)[1])
            self.label_check_csmgvt.place(relx=0.5, rely=0.45, anchor='c', width=300, height=50)

    def open_output_csmgvt(self):
        self.dir_output_csmgvt = filedialog.askdirectory()
        if self.dir_output_csmgvt:
            self.label_output_csmgvt.configure(text="Output directory given :\n" 
            + os.path.basename(os.path.normpath(self.dir_output_csmgvt)))
            self.label_output_csmgvt.place(relx=0.5, rely=0.7, anchor='c', width=300, height=50)

    def csmgvt_window(self):
        self.file_xml_csmgvt = None
        self.file_checker_csmgvt = None
        self.dir_output_csmgvt = None
        self.var_force_csmgvt = IntVar()
        self.verbose_csmgvt = IntVar()

        new_csmgvt = Toplevel(self)
        create_window(new_csmgvt, self.csmgvt_label, self.csmgvt_icon, 500, 300)

        label = Label(new_csmgvt, image=self.csmgvt_icon)
        label.place(relx=0.02, rely=0.15, anchor='w')
        self.create_ecoa_icon(new_csmgvt)

        self.label_xml_csmgvt = Label(new_csmgvt, justify='center')
        self.label_check_csmgvt = Label(new_csmgvt, justify='center')
        self.label_output_csmgvt = Label(new_csmgvt, justify='center')

        if shutil.which('ecoa-exvt'):
            self.label_check_csmgvt.configure(text="Default input checker used :\n ecoa-exvt")
            self.label_check_csmgvt.place(relx=0.5, rely=0.45, anchor='c', width=200, height=50) 

        checkbox_force_csmgvt = Checkbutton(new_csmgvt, text="Force existing files overwrite", variable=self.var_force_csmgvt,
        onvalue=1, offvalue=0)
        checkbox_force_csmgvt.place(relx=0.02, rely=0.78, anchor='w')
        
        checkbox_verbose_csmgvt = Checkbutton(new_csmgvt, text="Verbose mode", variable=self.verbose_csmgvt,
        onvalue=1, offvalue=0)
        checkbox_verbose_csmgvt.place(relx=0.6, rely=0.78, anchor='w')

        button_openfile_xml = Button(new_csmgvt, text="Open an ECOA xml file", command=self.open_xml_csmgvt)
        button_openfile_xml.place(relx=0.5, rely=0.1, anchor='c')
        button_openfile_check = Button(new_csmgvt, text="Open a checker executable file", command=self.open_checker_csmgvt)
        button_openfile_check.place(relx=0.5, rely=0.35, anchor='c')
        button_dir_output = Button(new_csmgvt, text="Choose an output directory", command=self.open_output_csmgvt)
        button_dir_output.place(relx=0.5, rely=0.6, anchor='c')
        
        combo_log_label = Label(new_csmgvt, text='Log level :')
        combo_log_label.place(relx=0.02, rely=0.5, anchor='w')
        self.combo_log = ttk.Combobox(new_csmgvt, state="readonly", values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], width=6)
        self.combo_log.current(1)
        self.combo_log.place(relx=0.15, rely=0.5, anchor='w')

        self.create_launch_button(new_csmgvt, True)
        self.create_help_button(new_csmgvt)
        self.create_compile_button(new_csmgvt)
        self.create_exe_button(new_csmgvt)
        
        new_csmgvt.bind("<Button-1>", self.callback_csmgvt)

    # LDP PART
    def callback_ldp(self, event):
        self.tool = 'ecoa-ldp'
        self.file_xml = self.file_xml_ldp
        self.exe_checker = self.file_checker_ldp
        self.file_conf = None
        self.dir_output = self.dir_output_ldp
        self.var_force = self.var_force_ldp.get()
        self.val_level = None
        self.verbose_level = self.combo_verbose.get()
        self.dir_templates = None
        self.verbose = None
        self.log_level = None
        self.userid = self.combo_userid.get()
        self.debug = self.debug_ldp.get()
        self.coverage = self.coverage_ldp.get()

    def open_xml_ldp(self):
        self.file_xml_ldp = filedialog.askopenfilename(initialdir = ".",
                                                    title = "Select an ECOA xml project file",
                                                    filetypes = [("XML files","*.xml")]
                                                    )
        if self.file_xml_ldp:
            self.label_xml_ldp.configure(text="Input XML file opened :\n" 
            + os.path.split(self.file_xml_ldp)[1])
            self.label_xml_ldp.place(relx=0.5, rely=0.2, anchor='c', width=300, height=50)

    def open_checker_ldp(self):
        self.file_checker_ldp = filedialog.askopenfilename(initialdir = ".",
                                                    title = "Select a checker executable",
                                                    filetypes = [("Checker executable","*.*")]
                                                    )
        if self.file_checker_ldp:
            self.label_check_ldp.configure(text="Input checker used :\n" 
            + os.path.split(self.file_checker_ldp)[1])
            self.label_check_ldp.place(relx=0.5, rely=0.45, anchor='c', width=300, height=50)

    def open_output_ldp(self):
        self.dir_output_ldp = filedialog.askdirectory()
        if self.dir_output_ldp:
            self.label_output_ldp.configure(text="Output directory given :\n" 
            + os.path.basename(os.path.normpath(self.dir_output_ldp)))
            self.label_output_ldp.place(relx=0.5, rely=0.7, anchor='c', width=300, height=50)

    def ldp_window(self):
        self.file_xml_ldp = None
        self.file_checker_ldp = None
        self.dir_output_ldp = None
        self.var_force_ldp = IntVar()
        self.debug_ldp = IntVar()
        self.coverage_ldp = IntVar()

        new_ldp = Toplevel(self)
        create_window(new_ldp, self.ldp_label, self.ldp_icon, 500, 300)

        label = Label(new_ldp, image=self.ldp_icon)
        label.place(relx=0.02, rely=0.15, anchor='w')
        self.create_ecoa_icon(new_ldp)

        self.label_xml_ldp = Label(new_ldp, justify='center')
        self.label_check_ldp = Label(new_ldp, justify='center')
        self.label_output_ldp = Label(new_ldp, justify='center')

        if shutil.which('ecoa-exvt'):
            self.label_check_ldp.configure(text="Default input checker used :\n ecoa-exvt")
            self.label_check_ldp.place(relx=0.5, rely=0.45, anchor='c', width=200, height=50)

        checkbox_force_ldp = Checkbutton(new_ldp, text="Force existing files overwrite", variable=self.var_force_ldp,
        onvalue=1, offvalue=0)
        checkbox_force_ldp.place(relx=0.02, rely=0.78, anchor='w')

        button_openfile_xml = Button(new_ldp, text="Open an ECOA xml file", command=self.open_xml_ldp)
        button_openfile_xml.place(relx=0.5, rely=0.1, anchor='c')
        button_openfile_check = Button(new_ldp, text="Open a checker executable file", command=self.open_checker_ldp)
        button_openfile_check.place(relx=0.5, rely=0.35, anchor='c')
        button_dir_output = Button(new_ldp, text="Choose an output directory", command=self.open_output_ldp)
        button_dir_output.place(relx=0.5, rely=0.6, anchor='c')

        combo_verbose_label = Label(new_ldp, text='Verbose level :')
        combo_verbose_label.place(relx=0.02, rely=0.5, anchor='w')
        self.combo_verbose = ttk.Combobox(new_ldp, state="readonly", values=["0", "1", "2", "3", "4"], width=2)
        self.combo_verbose.current(3)
        self.combo_verbose.place(relx=0.23, rely=0.5, anchor='w')
        
        combo_userid_label = Label(new_ldp, text='User id :')
        combo_userid_label.place(relx=0.02, rely=0.6, anchor='w')
        self.combo_userid = ttk.Combobox(new_ldp, state="readonly", values=[str(i) for i in range(10)], width=2)
        self.combo_userid.current(0)
        self.combo_userid.place(relx=0.23, rely=0.6, anchor='w')
        
        checkbox_debug_ldp = Checkbutton(new_ldp, text="Debug info", variable=self.debug_ldp,
        onvalue=1, offvalue=0)
        checkbox_debug_ldp.place(relx=0.5, rely=0.78, anchor='w')
        
        checkbox_coverage_ldp = Checkbutton(new_ldp, text="Coverage info", variable=self.coverage_ldp,
        onvalue=1, offvalue=0)
        checkbox_coverage_ldp.place(relx=0.7, rely=0.78, anchor='w')

        self.create_launch_button(new_ldp, True)
        self.create_help_button(new_ldp)
        self.create_compile_button(new_ldp, True)
        self.create_exe_button(new_ldp, True)

        new_ldp.bind("<Button-1>", self.callback_ldp)

