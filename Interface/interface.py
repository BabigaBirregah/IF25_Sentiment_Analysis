# http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://docs.python.org/3/library/tkinter.ttk.html#notebook
# http://tkinter.fdex.eu/index.html

from tkinter.filedialog import *
from tkinter.ttk import *

from Classifier.SVM import get_from_file
from Classifier.profile import construct_name_file
from Interface.actions import (analyse_file, analyse_query, analyse_text, analyse_tweets, custom_training,
                               load_classifier)
from Ressources.resource import Resource


class ToolTip(object):

    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx()
        y += self.widget.winfo_rooty() + 25
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        Label(self.tw, text=self.text, justify='left', background='white', relief='solid', borderwidth=1,
              wraplength=180).grid(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


class Application(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master)
        super().__init__(master, **kw)
        self.grid()

        # Object to be used
        self.display = Notebook(self, name="nb")  # tab manager
        self.toggle_language = StringVar()
        self.analyse_kernel = StringVar()
        self.size_sample = StringVar()
        self.value_submit = StringVar()
        self.user_query = StringVar()
        self.nb_tweet_collect = IntVar()
        self.nb_tweet_train = IntVar()
        self.toggle_randomness = StringVar()
        self.toggle_randomness_t = StringVar()
        self.toggle_nb_pos_neg = StringVar()
        self.toggle_nb_pos_neg_t = StringVar()
        self.train_kernel = StringVar()
        self.SVMClassifier = None
        self.custom_SVMClassifier = None
        self.Resource = Resource()
        self.count_visualiser = 0

        # Populate the window
        self._create_widgets()

    def _get_classifier(self):
        if self.custom_SVMClassifier:
            return self.custom_SVMClassifier
        elif self.SVMClassifier:
            return self.SVMClassifier
        else:
            self.SVMClassifier = self._load_default_classifier()
            return self.SVMClassifier

    def _load_default_classifier(self):
        self.SVMClassifier = load_classifier(self.size_sample.get(),
                                             self.toggle_randomness.get() == "Randomised",
                                             self.toggle_nb_pos_neg.get() == "Equal",
                                             self.analyse_kernel.get())
        return self.SVMClassifier

    def _create_widgets(self):
        # --------- Ours ---------
        self.display.grid()

        # create the content for the user, where he can choose the action to perform
        self._create_options_panel(self.display)

        # create the tab where the user can perform another custom training
        self._create_training_panel(self.display)

        # create the actions that the user can trigger
        self._create_actions_panel(self.display)

    def _create_options_panel(self, display):
        fen_user = Frame(display, name="fen_user")

        # Configure the analysis #
        general_options = LabelFrame(fen_user, text="General Options")

        # ---------- Choose the language -------------
        language_frame = LabelFrame(general_options, text="Choose the language")

        self.toggle_language.set("English")

        Checkbutton(language_frame, textvariable=self.toggle_language, variable=self.toggle_language, onvalue="English",
                    offvalue="Français").grid()

        ToolTip(language_frame,
                text="French here is not relevant since this application has no data set available for french, "
                     "but may be added")

        language_frame.grid(column=0, row=0, padx=10, pady=10)

        # Options for the default SVM classifier #
        default_classifier = LabelFrame(general_options, text="Default SVM classifier")

        # ---------- Choose the sample used -------------
        sample_frame = LabelFrame(default_classifier, text="Choose the sample used")

        self.size_sample.set("10 000 tweets")

        Checkbutton(sample_frame, textvariable=self.size_sample, variable=self.size_sample, onvalue="10 000 tweets",
                    offvalue="1 000 tweets", command=self._load_default_classifier).grid()

        sample_frame.grid(column=1, row=0, padx=10, pady=10, sticky="n")

        # ---------- Choose to randomise the sample -------------
        random_frame = LabelFrame(default_classifier, text="Order of tweets")

        self.toggle_randomness.set("Randomised")

        Checkbutton(random_frame, textvariable=self.toggle_randomness, variable=self.toggle_randomness,
                    onvalue="Randomised", offvalue="Non-randomised",
                    command=self._load_default_classifier).grid(padx=5,
                                                                pady=5)
        ToolTip(random_frame,
                text="If the data set is read randomly or we just pop the last item to populate the sample")

        random_frame.grid(column=2, row=0, padx=10, pady=10, sticky="n")

        # ---------- Choose either number of positive tweets should equal negative -------------
        nb_pos_neg_frame = LabelFrame(default_classifier, text="Number of positive equal negative tweets")

        self.toggle_nb_pos_neg.set("Equal")

        Checkbutton(nb_pos_neg_frame, textvariable=self.toggle_nb_pos_neg, variable=self.toggle_nb_pos_neg,
                    onvalue="Equal", offvalue="Non-equal", command=self._load_default_classifier).grid(padx=5, pady=5)
        ToolTip(nb_pos_neg_frame, text="If the number of positive and negative tweets should be equal")

        nb_pos_neg_frame.grid(column=3, row=0, padx=10, pady=10, sticky="n")

        # ---------- Choose the kernel used -------------
        kernel_frame = LabelFrame(default_classifier, text="Choose the kernel used")

        self.analyse_kernel.set("linear")

        Radiobutton(kernel_frame, text="Linear", variable=self.analyse_kernel, value="linear",
                    command=self._load_default_classifier).grid(column=0, row=0, padx=5, pady=5, sticky="w")
        Radiobutton(kernel_frame, text="Polynomial", variable=self.analyse_kernel, value="poly_kernel",
                    command=self._load_default_classifier).grid(column=0, row=1, padx=5, pady=5, sticky="w")
        Radiobutton(kernel_frame, text="Gaussian", variable=self.analyse_kernel, value="gaussian",
                    command=self._load_default_classifier).grid(column=1, row=0, padx=5, pady=5, sticky="w")
        Radiobutton(kernel_frame, text="Radial basis", variable=self.analyse_kernel, value="radial_basis",
                    command=self._load_default_classifier).grid(column=1, row=1, padx=5, pady=5, sticky="w")

        kernel_frame.grid(column=4, row=0, padx=10, pady=10)

        default_classifier.grid(column=1, row=0, padx=10, pady=10)

        general_options.grid(padx=10, pady=10)

        display.add(fen_user, text="Options")

    def _create_training_panel(self, display):
        fen_training = Frame(display, name="fen_visualiser")

        custom_SVM_frame = LabelFrame(fen_training, text="Create and use your own SVM classifier")

        # Create your own tailored SVM classifier
        options_frame = LabelFrame(custom_SVM_frame, text="Create custom SVM classifier")

        # ---------- Train by using 'x' tweets -------------
        size_frame = LabelFrame(options_frame, text="Size of the training sample")

        self.nb_tweet_train.set(100)

        Spinbox(size_frame, from_=100, to=1000000, increment=100, textvariable=self.nb_tweet_train,
                justify='center').grid(column=1, row=0, padx=5, pady=5)

        size_frame.grid(column=0, row=0, padx=10, pady=10, sticky="n")

        # ---------- Choose to randomise the sample -------------
        random_frame = LabelFrame(options_frame, text="Order of tweets")

        self.toggle_randomness_t.set("Randomised")

        Checkbutton(random_frame, textvariable=self.toggle_randomness_t, variable=self.toggle_randomness_t,
                    onvalue="Randomised", offvalue="Non-randomised").grid(padx=5, pady=5)
        ToolTip(random_frame,
                text="If the data set is read randomly or we just pop the last item to populate the sample")

        random_frame.grid(column=1, row=0, padx=10, pady=10, sticky="n")

        # ---------- Choose either number of positive tweets should equal negative -------------
        nb_pos_neg_frame = LabelFrame(options_frame, text="Number of positive and negative tweets")

        self.toggle_nb_pos_neg_t.set("Equal")

        Checkbutton(nb_pos_neg_frame, textvariable=self.toggle_nb_pos_neg_t, variable=self.toggle_nb_pos_neg_t,
                    onvalue="Equal", offvalue="Non-equal").grid(padx=5, pady=5)
        ToolTip(nb_pos_neg_frame, text="If the number of positive and negative tweets should be equal")

        nb_pos_neg_frame.grid(column=2, row=0, padx=10, pady=10, sticky="n")

        # ---------- Choose the kernel to use -------------
        kernel_frame = LabelFrame(options_frame, text="Choose the kernel to use")

        self.train_kernel.set("linear")

        Radiobutton(kernel_frame, text="Linear", variable=self.train_kernel,
                    value="linear").grid(column=0, row=0, padx=5, pady=5, sticky="w")
        Radiobutton(kernel_frame, text="Polynomial", variable=self.train_kernel,
                    value="poly_kernel").grid(column=0, row=1, padx=5, pady=5, sticky="w")
        Radiobutton(kernel_frame, text="Gaussian", variable=self.train_kernel,
                    value="gaussian").grid(column=1, row=0, padx=5, pady=5, sticky="w")
        Radiobutton(kernel_frame, text="Radial basis", variable=self.train_kernel, value="radial_basis").grid(
                column=1, row=1, padx=5, pady=5, sticky="w")

        kernel_frame.grid(column=3, row=0, padx=10, pady=10)

        # ---------- Create the desired custom SVM classifier -------------
        def train_settings():
            self.custom_SVMClassifier = custom_training(self.nb_tweet_train.get(),
                                                        self.toggle_randomness_t.get() == "Randomised",
                                                        self.toggle_nb_pos_neg_t.get() == "Equal", self.toggle_language,
                                                        self.train_kernel.get(), self.Resource)

        b_frame_1 = Frame(options_frame)
        Button(b_frame_1, text="Create custom SVM", command=train_settings).grid()
        ToolTip(b_frame_1, text="Will instantiate a SVM classifier to further be used to predict")
        b_frame_1.grid(column=4, row=0, padx=5, pady=5)

        options_frame.grid(padx=10, pady=10)

        # Special treatment for your own SVM classifier
        existing_SVM_frame = LabelFrame(custom_SVM_frame, text="Treatment for an existing custom SVM")

        # ---------- Save custom SVM classifier -------------
        def save_custom_SVM():
            if self.custom_SVMClassifier:
                name_file = construct_name_file(self.nb_tweet_train.get(), self.toggle_randomness_t.get(),
                                                self.toggle_nb_pos_neg_t.get(), self.train_kernel.get())
                self.custom_SVMClassifier.save_to_file(name_file)

        b_frame_2 = Frame(existing_SVM_frame)
        Button(b_frame_2, text="Save custom SVM", command=save_custom_SVM).grid()
        ToolTip(b_frame_2, text="Will save your custom SVM classifier to a json file, to load it afterwards")
        b_frame_2.grid(column=1, row=1, padx=5, pady=5)

        # ---------- Load custom SVM classifier -------------
        def load_custom_SVM():
            file_name = askopenfile(title="Open file of tweets", filetypes=[('json files', '.json')])
            self.custom_SVMClassifier = get_from_file(file_name)

        b_frame_3 = Frame(existing_SVM_frame)
        Button(b_frame_3, text="Load custom SVM", command=load_custom_SVM).grid()
        ToolTip(b_frame_3, text="Will load a custom SVM classifier contained in a json file")
        b_frame_3.grid(column=2, row=1, padx=5, pady=5)

        existing_SVM_frame.grid(padx=10, pady=10)

        custom_SVM_frame.grid()

        display.add(fen_training, text="Training")

    def _create_actions_panel(self, display):
        fen_actions = Frame(display, name="fen_actions")

        # Trigger some specific actions #
        specific_actions = LabelFrame(fen_actions, text="Trigger specific analysis")

        # ---------- Submit custom text -------------
        custom_text_frame = LabelFrame(specific_actions, text="Analyse custom text")

        self.value_submit.set("Text to analyse")

        def default_submit_text(arg):
            if self.value_submit.get() == "Text to analyse":
                self.value_submit.set("")
            elif not self.value_submit.get():
                self.value_submit.set("Text to analyse")

        text_submit = Entry(custom_text_frame, textvariable=self.value_submit)
        text_submit.bind("<Enter>", default_submit_text)
        text_submit.bind("<Leave>", default_submit_text)

        text_submit.grid(padx=5, pady=5)

        def text_analysis():
            if self.value_submit.get() != "Text to analyse":
                result = analyse_text(self.value_submit.get(), self._get_classifier(), self.Resource)
                self._create_viewer_panel(self.display, result)

        Button(custom_text_frame, text="Analyse text", command=text_analysis).grid(padx=5, pady=5)

        ToolTip(custom_text_frame,
                text="Will analyse and predict the sentiment of the text.\nIt will open another tab to visualize the "
                     "result")

        custom_text_frame.grid(column=0, row=0, padx=10, pady=10)

        # ---------- Submit custom text/csv file -------------
        custom_file_frame = LabelFrame(specific_actions, text="Analyse custom file")

        def ask_file():
            file_name = askopenfile(title="Open file of tweets",
                                    filetypes=[('txt files', '.txt'), ('csv files', '.csv')])
            result = analyse_file(open(file_name, "rb").readlines(), self._get_classifier(), self.Resource)
            self._create_viewer_panel(self.display, result)

        Label(custom_file_frame).grid(row=0, padx=5, pady=5, )

        Button(custom_file_frame, text="Open file & Analyse", command=ask_file).grid(row=1, padx=5, pady=5,
                                                                                     sticky="s")

        ToolTip(custom_file_frame,
                text="Will analyse and predict the sentiment of the file. The file is supposed to contain one tweet "
                     "per line.\nIt will open another tab to visualize the result")

        custom_file_frame.grid(column=1, row=0, padx=10, pady=10, sticky="n")

        # ---------- Get and analyse specific tweet -------------
        query_frame = LabelFrame(specific_actions, text="Analyse few trend tweets related topic")

        self.user_query.set("'#ITAR'")

        def default_query_text(arg):
            if self.user_query.get() == "'#ITAR'":
                self.user_query.set("")
            elif not self.user_query.get():
                self.user_query.set("'#ITAR'")

        text_submit = Entry(query_frame, textvariable=self.user_query)

        text_submit.bind("<Enter>", default_query_text)
        text_submit.bind("<Leave>", default_query_text)

        text_submit.grid(padx=5, pady=5)

        def query_analysis():
            if self.user_query.get() != "'#ITAR'" and '#' in self.user_query.get():
                result = analyse_query(self.user_query.get(), self._get_classifier(), self.Resource)
                self._create_viewer_panel(self.display, result)
            elif self.user_query.get() != "'#ITAR'":
                result = analyse_query('#' + self.user_query.get(), self._get_classifier(), self.Resource)
                self._create_viewer_panel(self.display, result)

        Button(query_frame, text="Analyse trend", command=query_analysis).grid(padx=5, pady=5)

        ToolTip(query_frame,
                text="Will analyse and predict the sentiment of some tweets regarding the '#'.\nIt will open another "
                     "tab to visualize the result")

        query_frame.grid(column=2, row=0, padx=10, pady=10)

        # ---------- Get and analyse 'x' tweets -------------
        number_frame = LabelFrame(specific_actions, text="Collect and analyse 'x' tweets")

        self.nb_tweet_collect.set(5)

        Spinbox(number_frame, from_=5, to=1000, increment=5, textvariable=self.nb_tweet_collect, justify='center').grid(
                padx=5, pady=5)

        def analyse_stream_tweet():
            result = analyse_tweets(self.nb_tweet_collect.get(), self._get_classifier(), self.Resource)
            self._create_viewer_panel(self.display, result)

        Button(number_frame, text="Analyse 'x' tweets", command=analyse_stream_tweet).grid(padx=5, pady=5)

        ToolTip(number_frame,
                text="Will analyse and predict the sentiment of 'x' tweets from the Twitter API stream.\nIt will open "
                     "another tab to visualize the result")

        number_frame.grid(column=3, row=0, padx=10, pady=10)

        specific_actions.grid(padx=10, pady=10)

        display.add(fen_actions, text="Actions")

    def _create_viewer_panel(self, display, result):
        self.count_visualiser += 1
        name_viewer = "fen_visualiser_{}".format(self.count_visualiser)

        global_frame = Frame(display, width=900, height=600)

        def close_tab():
            display.forget(self.count_visualiser + 2)

        Button(global_frame, command=close_tab, text="Close tab").grid()

        canvas_result = Canvas(global_frame, width=900, height=600)
        canvas_result.grid(row=1, column=0, sticky="nsew")

        fen_visualiser = Frame(canvas_result, name=name_viewer)
        canvas_result.create_window(0, 0, window=fen_visualiser)

        for idx, value in enumerate(result):
            group_tweet = LabelFrame(fen_visualiser, text="Tweet {}".format(idx))
            Label(group_tweet, text="Text :").grid(column=0, row=idx // 2, sticky="e")
            Label(group_tweet, text=bytes(value[0], 'utf-8')).grid(column=1, row=idx // 2, sticky="w")
            Label(group_tweet, text="Label :").grid(column=0, row=idx // 2 + 1, sticky="e")
            if value[1] == "Negative":
                Label(group_tweet, text=value[1], foreground="red").grid(column=1, row=idx // 2 + 1, sticky="w")
            elif value[1] == "Neutral":
                Label(group_tweet, text=value[1], foreground="gray").grid(column=1, row=idx // 2 + 1, sticky="w")
            elif value[1] == "Positive":
                Label(group_tweet, text=value[1], foreground="green").grid(column=1, row=idx // 2 + 1, sticky="w")
            group_tweet.grid(sticky="w")

        vertical_scrollbar = Scrollbar(global_frame, command=canvas_result.yview)
        canvas_result.configure(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = Scrollbar(global_frame, orient=HORIZONTAL, command=canvas_result.xview)
        canvas_result.configure(xscrollcommand=horizontal_scrollbar.set)

        vertical_scrollbar.grid(row=1, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=2, column=0, sticky="ew")

        def update_scroll_region(event):
            canvas_result.configure(scrollregion=canvas_result.bbox("all"))

        fen_visualiser.bind("<Configure>", update_scroll_region)

        display.add(global_frame, text="Visualiser {}".format(self.count_visualiser))
