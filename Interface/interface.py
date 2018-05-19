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
        self.size_sample = IntVar()
        self.value_submit = StringVar()
        self.user_query = StringVar()
        self.nb_tweet_collect = IntVar()
        self.nb_tweet_train = IntVar()
        self.toggle_randomness = StringVar()
        self.toggle_nb_pos_neg = StringVar()
        self.train_kernel = StringVar()

        # Populate the window
        self._create_widgets()

    def _create_widgets(self):
        # --------- Ours ---------
        self.display.grid()

        # create the content for the user, where he can choose the action to perform
        self._create_options_panel(self.display)

        # create the tab where the user can perform another custom training
        self._create_training_panel(self.display)

        # create the actions that the user can trigger
        self._create_actions_panel(self.display)

        # TODO : maybe we should only create this tab when there is something to show
        # self.create_viewer_panel(self.display)  # create the content to visualize the action chosen by the user

    def _create_options_panel(self, display):
        fen_user = Frame(display, name="fen_user")

        # Configure the analysis #
        general_options = LabelFrame(fen_user, text="General Options")

        # ---------- Choose the language -------------
        language_frame = LabelFrame(general_options, text="Choose the language")

        self.toggle_language.set("English")

        Checkbutton(language_frame, textvariable=self.toggle_language, variable=self.toggle_language, onvalue="English",
                    offvalue="Français").grid()
        language_frame.grid(column=0, row=0, padx=10, pady=10)

        # ---------- Choose the sample used -------------
        sample_frame = LabelFrame(general_options, text="Choose the sample used")

        self.size_sample.set("1 000 tweets")

        Checkbutton(sample_frame, textvariable=self.size_sample, variable=self.size_sample, onvalue="1 000 tweets",
                    offvalue="10 000 tweets").grid()

        sample_frame.grid(column=1, row=0, padx=10, pady=10)

        # ---------- Choose to randomise the sample -------------
        random_frame = LabelFrame(general_options, text="Order of tweets")

        self.toggle_randomness.set("Randomised")

        Checkbutton(random_frame, textvariable=self.toggle_randomness, variable=self.toggle_randomness,
                    onvalue="Randomised", offvalue="Non-randomised").grid(padx=5, pady=5)

        random_frame.grid(column=2, row=0, padx=10, pady=10)

        # ---------- Choose either number of positive tweets should equal negative -------------
        nb_pos_neg_frame = LabelFrame(general_options, text="Number of positive equal negative tweets")

        self.toggle_nb_pos_neg.set("Equal")

        Checkbutton(nb_pos_neg_frame, textvariable=self.toggle_nb_pos_neg, variable=self.toggle_nb_pos_neg,
                    onvalue="Equal", offvalue="Non-equal").grid(padx=5, pady=5)

        nb_pos_neg_frame.grid(column=3, row=0, padx=10, pady=10)

        # ---------- Choose the kernel used -------------
        kernel_frame = LabelFrame(general_options, text="Choose the kernel used")

        self.analyse_kernel.set("gaussian")

        Radiobutton(kernel_frame, text="Linear", variable=self.analyse_kernel, value="linear").grid(padx=5, pady=5)
        Radiobutton(kernel_frame, text="Polynomial", variable=self.analyse_kernel, value="polynomial").grid(padx=5,
                                                                                                            pady=5)
        Radiobutton(kernel_frame, text="Gaussian", variable=self.analyse_kernel, value="gaussian").grid(padx=5, pady=5)

        kernel_frame.grid(column=4, row=0, padx=10, pady=10)

        general_options.grid(padx=10, pady=10)

        display.add(fen_user, text="Options")

    def _create_training_panel(self, display):
        fen_training = Frame(display, name="fen_visualiser")

        options_frame = LabelFrame(fen_training, text="Tweak the parameters")

        # ---------- Train by using 'x' tweets -------------
        size_frame = LabelFrame(options_frame, text="Size of the training sample")

        self.nb_tweet_train.set(100)

        Spinbox(size_frame, from_=100, to=1000000, increment=100, textvariable=self.nb_tweet_train,
                justify='center').grid(column=1, row=0, padx=5, pady=5)

        size_frame.grid(column=0, row=0, padx=10, pady=10)

        # ---------- Choose to randomise the sample -------------
        random_frame = LabelFrame(options_frame, text="Order of tweets")

        self.toggle_randomness.set("Randomised")

        Checkbutton(random_frame, textvariable=self.toggle_randomness, variable=self.toggle_randomness,
                    onvalue="Randomised", offvalue="Non-randomised").grid(padx=5, pady=5)

        random_frame.grid(column=1, row=0, padx=10, pady=10)

        # ---------- Choose either number of positive tweets should equal negative -------------
        nb_pos_neg_frame = LabelFrame(options_frame, text="Number of positive equal negative tweets")

        self.toggle_nb_pos_neg.set("Equal")

        Checkbutton(nb_pos_neg_frame, textvariable=self.toggle_nb_pos_neg, variable=self.toggle_nb_pos_neg,
                    onvalue="Equal", offvalue="Non-equal").grid(padx=5, pady=5)

        nb_pos_neg_frame.grid(column=2, row=0, padx=10, pady=10)

        # ---------- Choose the kernel to use -------------
        kernel_frame = LabelFrame(options_frame, text="Choose the kernel to use")

        self.train_kernel.set("gaussian")

        Radiobutton(kernel_frame, text="Linear", variable=self.train_kernel, value="linear").grid(padx=5, pady=5)
        Radiobutton(kernel_frame, text="Polynomial", variable=self.train_kernel, value="polynomial").grid(padx=5,
                                                                                                          pady=5)
        Radiobutton(kernel_frame, text="Gaussian", variable=self.train_kernel, value="gaussian").grid(padx=5, pady=5)

        kernel_frame.grid(column=3, row=0, padx=10, pady=10)

        def train_settings():
            custom_training(self.nb_tweet_train, self.toggle_randomness.get() == "Randomised",
                            self.toggle_nb_pos_neg.get() == "Equal", self.toggle_language, self.analyse_kernel)

        Button(options_frame, text="Do it", command=train_settings).grid(column=1, padx=5, pady=5)

        options_frame.grid(padx=10, pady=10)

        display.add(fen_training, text="Training")

    def _create_actions_panel(self, display):
        fen_actions = Frame(display, name="fen_actions")

        # Trigger some specific actions #
        specific_actions = LabelFrame(fen_actions, text="Trigger specific actions")

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
                analyse_text(self.value_submit, self.toggle_language, self.analyse_kernel, self.size_sample)

        Button(custom_text_frame, text="Do it", command=text_analysis).grid(padx=5, pady=5)
        custom_text_frame.grid(column=0, row=0, padx=10, pady=10)

        # ---------- Submit custom text/csv file -------------
        custom_file_frame = LabelFrame(specific_actions, text="Analyse custom file")

        def ask_file():
            file_name = askopenfile(title="Ouvrir fichier de tweets",
                                    filetypes=[('txt files', '.txt'), ('csv files', '.csv')])
            analyse_file(open(file_name, "rb").read(), self.toggle_language, self.analyse_kernel, self.size_sample)

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
                analyse_query(self.user_query, self.toggle_language, self.analyse_kernel, self.size_sample)
            elif self.user_query != "Soumettre un '#' à regarder":
                analyse_query('#' + self.user_query.get(), self.toggle_language, self.analyse_kernel, self.size_sample)

        Button(query_frame, text="Do it", command=query_analysis).grid(padx=5, pady=5)
        query_frame.grid(column=2, row=0, padx=10, pady=10)

        # ---------- Get and analyse 'x' tweets -------------
        number_frame = LabelFrame(specific_actions, text="Collect and analyse 'x' tweets")

        self.nb_tweet_collect.set(5)

        Spinbox(number_frame, from_=5, to=1000, increment=5, textvariable=self.nb_tweet_collect, justify='center').grid(
                padx=5, pady=5)

        def analyse_stream_tweet():
            analyse_tweets(self.nb_tweet_collect, self.toggle_language, self.analyse_kernel, self.size_sample)

        Button(number_frame, text="Do it", command=analyse_stream_tweet).grid(padx=5, pady=5)
        number_frame.grid(column=3, row=0, padx=10, pady=10)

        specific_actions.grid(padx=10, pady=10)

        display.add(fen_actions, text="Actions")

    def create_viewer_panel(self, display):
        fen_visualiser = Frame(display, name="fen_visualiser")

        display.add(fen_visualiser, text="Visualiser")
