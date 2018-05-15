# http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://docs.python.org/3/library/tkinter.ttk.html#notebook
# http://tkinter.fdex.eu/index.html

from tkinter.filedialog import *
from tkinter.ttk import *

from Interface.actions import analyse_file, analyse_query, analyse_text, analyse_tweets, custom_training


class Application(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master)
        super().__init__(master, **kw)
        self.grid()

        # Object to be used
        self.display = Notebook(self, name="nb")  # tab manager
        self.toggle_language = StringVar()
        self.analyse_kernel = StringVar()
        self.value_submit = StringVar()
        self.user_query = StringVar()
        self.nb_tweet_collect = IntVar()
        self.nb_tweet_train = IntVar()
        self.toggle_randomness = StringVar()
        self.train_kernel = StringVar()

        # Populate the window
        self.createWidgets()

    def createWidgets(self):
        # --------- Ours ---------
        self.display.grid()

        # create the content for the user, where he can choose the action to perform
        self.create_user_panel(self.display)

        # create the tab where the user can perform another custom training
        self.create_training_panel(self.display)

        # TODO : maybe we should only create this tab when there is something to show
        # self.create_viewer_panel(self.display)  # create the content to visualize the action chosen by the user

    def create_user_panel(self, display):
        fen_user = Frame(display, name="fen_user")

        # Configure the analysis #
        general_options = LabelFrame(fen_user, text="General Options")

        # ---------- Choose the language -------------
        language_frame = LabelFrame(general_options, text="Choose the language")

        self.toggle_language.set("English")

        Checkbutton(language_frame, textvariable=self.toggle_language, variable=self.toggle_language, onvalue="English",
                    offvalue="Français").grid()
        language_frame.grid(column=0, row=0, padx=10, pady=10)

        # ---------- Choose the kernel used -------------
        kernel_frame = LabelFrame(general_options, text="Choose the kernel used")

        self.analyse_kernel.set("gaussian")

        Radiobutton(kernel_frame, text="Linear", variable=self.analyse_kernel, value="linear").grid(padx=5, pady=5)
        Radiobutton(kernel_frame, text="Polynomial", variable=self.analyse_kernel, value="polynomial").grid(padx=5,
                                                                                                            pady=5)
        Radiobutton(kernel_frame, text="Gaussian", variable=self.analyse_kernel, value="gaussian").grid(padx=5, pady=5)

        kernel_frame.grid(column=1, row=0, padx=10, pady=10)

        # ---------- Choose the sample used -------------
        sample_frame = LabelFrame(general_options, text="Choose the sample used")

        value_sample = StringVar()
        value_sample.set("few_randomised")

        Radiobutton(sample_frame, text="1'000 tweets randomised", variable=value_sample, value="few_randomised").grid(
                padx=5, pady=5)
        Radiobutton(sample_frame, text="10'000 tweets randomised", variable=value_sample,
                    value="many_randomised").grid(padx=5, pady=5)
        Radiobutton(sample_frame, text="1'000 tweets non-randomised", variable=value_sample,
                    value="few_non-randomised").grid(padx=5, pady=5)
        Radiobutton(sample_frame, text="10'000 tweets non-randomised", variable=value_sample,
                    value="many_non-randomised").grid(padx=5, pady=5)

        sample_frame.grid(column=2, row=0, padx=10, pady=10)

        general_options.grid(padx=10, pady=10)

        # Trigger some specific actions #
        specific_actions = LabelFrame(fen_user, text="Trigger specific actions")

        # ---------- Submit custom text -------------
        custom_text_frame = LabelFrame(specific_actions, text="Analyse custom text")

        self.value_submit.set("Soumettre un texte")

        def default_submit_text(arg):
            if self.value_submit.get() == "Soumettre un texte":
                self.value_submit.set("")
            elif not self.value_submit.get():
                self.value_submit.set("Soumettre un texte")

        text_submit = Entry(custom_text_frame, textvariable=self.value_submit)
        text_submit.bind("<Enter>", default_submit_text)
        text_submit.bind("<Leave>", default_submit_text)

        text_submit.grid(padx=5, pady=5)

        def text_analysis():
            if self.value_submit != "Soumettre un texte":
                analyse_text(self.value_submit, self.analyse_kernel)

        Button(custom_text_frame, text="Do it", command=text_analysis).grid(padx=5, pady=5)
        custom_text_frame.grid(column=0, row=0, padx=10, pady=10)

        # ---------- Submit custom text/csv file -------------
        custom_file_frame = LabelFrame(specific_actions, text="Analyse custom file")

        def ask_file():
            file_name = askopenfile(title="Ouvrir fichier de tweets",
                                    filetypes=[('txt files', '.txt'), ('csv files', '.csv')])
            analyse_file(open(file_name, "rb").read(), self.analyse_kernel)

        Button(custom_file_frame, text="Do it", command=ask_file).grid(padx=5, pady=5)
        custom_file_frame.grid(column=1, row=0, padx=10, pady=10)

        # ---------- Get and analyse specific tweet -------------
        query_frame = LabelFrame(specific_actions, text="Analyse some tweet related topic")

        self.user_query.set("Soumettre un '#' à regarder")

        def default_query_text(arg):
            if self.user_query.get() == "Soumettre un '#' à regarder":
                self.user_query.set("")
            elif not self.user_query.get():
                self.user_query.set("Soumettre un '#' à regarder")

        text_submit = Entry(query_frame, textvariable=self.user_query)

        text_submit.bind("<Enter>", default_query_text)
        text_submit.bind("<Leave>", default_query_text)

        text_submit.grid(padx=5, pady=5)

        def query_analysis():
            if self.user_query != "Soumettre un '#' à regarder" and '#' in self.user_query:
                analyse_query(self.user_query, self.analyse_kernel)
            elif self.user_query != "Soumettre un '#' à regarder":
                analyse_query('#' + self.user_query.get(), self.analyse_kernel)

        Button(query_frame, text="Do it", command=query_analysis).grid(padx=5, pady=5)
        query_frame.grid(column=2, row=0, padx=10, pady=10)

        # ---------- Get and analyse 'x' tweets -------------
        number_frame = LabelFrame(specific_actions, text="Collect and analyse 'x' tweets")

        self.nb_tweet_collect.set(5)

        Spinbox(number_frame, from_=5, to=1000, increment=5, textvariable=self.nb_tweet_collect, justify='center').grid(
                padx=5, pady=5)

        def analyse_stream_tweet():
            analyse_tweets(self.nb_tweet_collect, self.analyse_kernel)

        Button(number_frame, text="Do it", command=analyse_stream_tweet).grid(padx=5, pady=5)
        number_frame.grid(column=3, row=0, padx=10, pady=10)

        specific_actions.grid(padx=10, pady=10)

        display.add(fen_user, text="Options")

    def create_training_panel(self, display):
        fen_training = Frame(display, name="fen_visualiser")

        # ---------- Train by using 'x' tweets -------------
        options_frame = LabelFrame(fen_training, text="Tweak the parameters")

        self.nb_tweet_train.set(100)

        Label(options_frame, text="Choose the size of the training sample").grid(column=0, row=0, padx=10, pady=10)
        Spinbox(options_frame, from_=100, to=1000000, increment=100, textvariable=self.nb_tweet_train,
                justify='center').grid(column=1, row=0, padx=5, pady=5)

        # ---------- Choose to randomise the sample -------------
        self.toggle_randomness.set("Randomised")

        Checkbutton(options_frame, textvariable=self.toggle_randomness, variable=self.toggle_randomness,
                    onvalue="Randomised", offvalue="Non-randomised").grid(padx=5, pady=5)

        # ---------- Choose the kernel to use -------------
        kernel_frame = LabelFrame(options_frame, text="Choose the kernel used")

        self.train_kernel.set("gaussian")

        Radiobutton(kernel_frame, text="Linear", variable=self.train_kernel, value="linear").grid(padx=5, pady=5)
        Radiobutton(kernel_frame, text="Polynomial", variable=self.train_kernel, value="polynomial").grid(padx=5,
                                                                                                          pady=5)
        Radiobutton(kernel_frame, text="Gaussian", variable=self.train_kernel, value="gaussian").grid(padx=5, pady=5)

        kernel_frame.grid(column=1, row=0, padx=10, pady=10)

        def train_settings():
            custom_training(self.nb_tweet_train, self.toggle_randomness == "Randomised", self.train_kernel)

        Button(options_frame, text="Do it", command=train_settings).grid(padx=5, pady=5)
        options_frame.grid(padx=10, pady=10)

        display.add(fen_training, text="Training")

    def create_viewer_panel(self, display):
        fen_visualiser = Frame(display, name="fen_visualiser")

        display.add(fen_visualiser, text="Visualiser")
