# http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://docs.python.org/3/library/tkinter.ttk.html#notebook
# http://tkinter.fdex.eu/index.html

from tkinter.filedialog import *
from tkinter.ttk import *

from Data import twitter_collect


class Application(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master)
        super().__init__(master, **kw)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # --------- Ours ---------
        self.display = Notebook(self, name="nb")  # tab manager
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

        toggle_language = StringVar()
        toggle_language.set("English")

        Checkbutton(language_frame, textvariable=toggle_language, variable=toggle_language, onvalue="English",
                    offvalue="Français").grid()
        language_frame.grid(column=0, row=0)

        # ---------- Choose the kernel used -------------
        kernel_frame = LabelFrame(general_options, text="Choose the kernel used")

        value_kernel = StringVar()
        value_kernel.set("gaussian")

        Radiobutton(kernel_frame, text="Linear", variable=value_kernel, value="linear").grid()
        Radiobutton(kernel_frame, text="Polynomial", variable=value_kernel, value="polynomial").grid()
        Radiobutton(kernel_frame, text="Gaussian", variable=value_kernel, value="gaussian").grid()

        kernel_frame.grid(column=1, row=0)

        # ---------- Choose the sample used -------------
        sample_frame = LabelFrame(general_options, text="Choose the sample used")

        value_sample = StringVar()
        value_sample.set("few_randomised")

        Radiobutton(sample_frame, text="1'000 tweets randomised", variable=value_sample, value="few_randomised").grid()
        Radiobutton(sample_frame, text="10'000 tweets randomised", variable=value_sample,
                    value="many_randomised").grid()
        Radiobutton(sample_frame, text="1'000 tweets non-randomised", variable=value_sample,
                    value="few_non-randomised").grid()
        Radiobutton(sample_frame, text="10'000 tweets non-randomised", variable=value_sample,
                    value="many_non-randomised").grid()

        sample_frame.grid(column=2, row=0)

        general_options.grid()

        # Trigger some specific actions #
        specific_actions = LabelFrame(fen_user, text="Trigger specific actions")

        # ---------- Submit custom text -------------
        custom_text_frame = LabelFrame(specific_actions, text="Analyse custom text")

        self.value_submit = StringVar()
        self.value_submit.set("Soumettre un texte")

        def default_submit_text(arg):
            if self.value_submit.get() == "Soumettre un texte":
                self.value_submit.set("")
            elif not self.value_submit.get():
                self.value_submit.set("Soumettre un texte")

        text_submit = Entry(custom_text_frame, textvariable=self.value_submit)
        text_submit.bind("<Enter>", default_submit_text)
        text_submit.bind("<Leave>", default_submit_text)

        text_submit.grid()

        def text_analysis():
            if self.value_submit != "Soumettre un texte":
                pass  # function_to_call(self.value_submit)

        Button(custom_text_frame, text="Do it", command=text_analysis).grid()
        custom_text_frame.grid(column=0, row=0)

        # ---------- Submit custom text/csv file -------------
        custom_file_frame = LabelFrame(specific_actions, text="Analyse custom file")

        def ask_file():
            file_name = askopenfile(title="Ouvrir fichier de tweets",
                                    filetypes=[('txt files', '.txt'), ('csv files', '.csv')])
            pass  # function_to_call(open(file_name, "rb").read())

        Button(custom_file_frame, text="Do it", command=ask_file).grid()
        custom_file_frame.grid(column=1, row=0)

        # ---------- Get and analyse specific tweet -------------
        query_frame = LabelFrame(specific_actions, text="Analyse some tweet related topic")

        self.user_query = StringVar()
        self.user_query.set("Soumettre un '#' à regarder")

        def default_query_text(arg):
            if self.user_query.get() == "Soumettre un '#' à regarder":
                self.user_query.set("")
            elif not self.user_query.get():
                self.user_query.set("Soumettre un '#' à regarder")

        text_submit = Entry(query_frame, textvariable=self.user_query)

        text_submit.bind("<Enter>", default_query_text)
        text_submit.bind("<Leave>", default_query_text)

        text_submit.grid()

        def query_analysis():
            if self.user_query != "Soumettre un '#' à regarder" and '#' in self.user_query:
                twitter_collect.search_sample(self.user_query)
            elif self.user_query != "Soumettre un '#' à regarder":
                twitter_collect.search_sample('#' + self.user_query.get())

        Button(query_frame, text="Do it", command=query_analysis).grid()
        query_frame.grid(column=2, row=0)

        # ---------- Get and analyse 'x' tweets -------------
        number_frame = LabelFrame(specific_actions, text="Collect and analyse 'x' tweets")

        self.number_tweets = IntVar()
        self.number_tweets.set(5)

        Spinbox(number_frame, from_=5, to=1000, increment=5, textvariable=self.number_tweets, justify='center').grid()

        def collect_tweet_stream():
            twitter_collect.collect_tweet(self.number_tweets)

        Button(number_frame, text="Do it", command=collect_tweet_stream).grid()
        number_frame.grid(column=3, row=0)

        specific_actions.grid()

        display.add(fen_user, text="Options")

    def create_training_panel(self, display):
        fen_training = Frame(display, name="fen_visualiser")

        # ---------- Get and analyse 'x' tweets -------------
        options_frame = LabelFrame(fen_training, text="Tweak the parameters")

        self.number_tweets = IntVar()
        self.number_tweets.set(100)

        Label(options_frame, text="Choose the size of the training sample").grid(column=0, row=0)
        Spinbox(options_frame, from_=100, to=1000000, increment=100, textvariable=self.number_tweets,
                justify='center').grid(column=1, row=0)

        toggle_randomness = StringVar()
        toggle_randomness.set("Randomised")

        Checkbutton(options_frame, textvariable=toggle_randomness, variable=toggle_randomness, onvalue="Randomised",
                    offvalue="Non-randomised").grid()

        def train_settings():
            pass

        Button(options_frame, text="Do it", command=train_settings).grid()
        options_frame.grid()

        display.add(fen_training, text="Training")

    def create_viewer_panel(self, display):
        fen_visualiser = Frame(display, name="fen_visualiser")

        display.add(fen_visualiser, text="Visualiser")
