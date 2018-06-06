# http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://docs.python.org/3/library/tkinter.ttk.html#notebook
# http://tkinter.fdex.eu/index.html

from functools import partial
from tkinter.filedialog import *
from tkinter.ttk import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

from Classifier.SVM import get_from_file
from Classifier.profile import construct_name_file, readable_name_classifier
from Interface.actions import (analyse_file, analyse_query, analyse_text, analyse_tweets, custom_training,
                               load_classifier, predict_test)
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
        self.size_sample_p = StringVar()
        self.value_submit = StringVar()
        self.user_query = StringVar()
        self.nb_tweet_collect = IntVar()
        self.nb_tweet_train = IntVar()
        self.nb_tweet_predict = IntVar()
        self.toggle_randomness = StringVar()
        self.toggle_randomness_t = StringVar()
        self.toggle_randomness_p = StringVar()
        self.toggle_nb_pos_neg = StringVar()
        self.toggle_nb_pos_neg_t = StringVar()
        self.toggle_nb_pos_neg_p = StringVar()
        self.train_kernel = StringVar()
        self.predict_kernel = StringVar()
        self.SVMClassifier = None
        self.custom_SVMClassifier = None
        self.Resource = Resource()
        self.count_visualiser = 0
        self.active_view = StringVar()

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

        # create the tab where the user can test the different profile of SVM
        self._create_predict_panel(self.display)

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
                    offvalue="Français").grid(padx=5, pady=5)

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
                    offvalue="1 000 tweets", command=self._load_default_classifier).grid(padx=5, pady=5)

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
                name_file = construct_name_file(self.nb_tweet_train.get(),
                                                self.toggle_randomness_t.get() == "Randomised",
                                                self.toggle_nb_pos_neg_t.get() == "Equal", self.train_kernel.get())
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

    def _create_predict_panel(self, display):
        fen_predict = Frame(display, name="fen_predict")

        # Test  SVM classifier
        options_frame = LabelFrame(fen_predict, text="Test SVM classifier")

        # For all SVMs classifier
        for_all_frame = LabelFrame(options_frame, text="For all the SVM profiles")

        # ---------- Train by using 'x' tweets -------------
        size_frame = LabelFrame(for_all_frame, text="Size of the sample to test")

        self.nb_tweet_predict.set(100)

        Spinbox(size_frame, from_=10, to=1000000, increment=100, textvariable=self.nb_tweet_predict,
                justify='center').grid(column=0, row=0, padx=5, pady=5)

        size_frame.grid(column=0, row=0, padx=10, pady=10)

        # ---------- Threshold for 'Neutral' class -------------
        threshold_frame = LabelFrame(for_all_frame, text="Tolerance 'Neutral'")

        default_value = StringVar()
        default_value.set("0.25")
        threshold_spinbox = Spinbox(threshold_frame, from_=0.0, to=0.80, increment=0.05, justify='center',
                                    textvariable=default_value)
        ToolTip(threshold_frame,
                text="From -'x' to +'x', where 'x' is the value selected, the label of the text will be "
                     "'Neutral'.\nIn the computation of the performance score, 'Neutral' is both considered "
                     "'Positive' and 'Negative'")
        threshold_spinbox.grid(column=0, row=0, padx=5, pady=5)

        threshold_frame.grid(column=1, row=0, padx=10, pady=10)

        for_all_frame.grid(padx=10, pady=10)

        # Test a specific SVM classifier
        specific_frame = LabelFrame(options_frame, text="Test a specific classifier")

        # ---------- Choose the sample used -------------
        sample_frame = LabelFrame(specific_frame, text="Choose the sample used")

        self.size_sample_p.set("10 000 tweets")

        Checkbutton(sample_frame, textvariable=self.size_sample_p, variable=self.size_sample_p, onvalue="10 000 tweets",
                    offvalue="1 000 tweets").grid(padx=5, pady=5)

        sample_frame.grid(column=0, row=0, padx=10, pady=10, sticky="n")

        # ---------- Choose to use a randomised sample -------------
        random_frame = LabelFrame(specific_frame, text="Order of tweets")

        self.toggle_randomness_p.set("Randomised")

        Checkbutton(random_frame, textvariable=self.toggle_randomness_p, variable=self.toggle_randomness_p,
                    onvalue="Randomised", offvalue="Non-randomised").grid(padx=5, pady=5)
        ToolTip(random_frame,
                text="If the data set is read randomly or we just pop the last item to populate the sample")

        random_frame.grid(column=1, row=0, padx=10, pady=10, sticky="n")

        # ---------- Choose either number of positive tweets should equal negative -------------
        nb_pos_neg_frame = LabelFrame(specific_frame, text="Number of positive and negative tweets")

        self.toggle_nb_pos_neg_p.set("Equal")

        Checkbutton(nb_pos_neg_frame, textvariable=self.toggle_nb_pos_neg_p, variable=self.toggle_nb_pos_neg_p,
                    onvalue="Equal", offvalue="Non-equal").grid(padx=5, pady=5)
        ToolTip(nb_pos_neg_frame, text="If the number of positive and negative tweets should be equal")

        nb_pos_neg_frame.grid(column=2, row=0, padx=10, pady=10, sticky="n")

        # ---------- Choose the kernel to use -------------
        kernel_frame = LabelFrame(specific_frame, text="Choose the kernel to use")

        self.predict_kernel.set("linear")

        Radiobutton(kernel_frame, text="Linear", variable=self.predict_kernel,
                    value="linear").grid(column=0, row=0, padx=5, pady=5, sticky="w")
        Radiobutton(kernel_frame, text="Polynomial", variable=self.predict_kernel,
                    value="poly_kernel").grid(column=0, row=1, padx=5, pady=5, sticky="w")
        Radiobutton(kernel_frame, text="Gaussian", variable=self.predict_kernel,
                    value="gaussian").grid(column=1, row=0, padx=5, pady=5, sticky="w")
        Radiobutton(kernel_frame, text="Radial basis", variable=self.predict_kernel, value="radial_basis").grid(
                column=1, row=1, padx=5, pady=5, sticky="w")

        kernel_frame.grid(column=3, row=0, padx=10, pady=10)

        specific_frame.grid(padx=10, pady=10)

        # Test
        test_frame = LabelFrame(options_frame, text="Trigger the test")
        
        # ---------- Test the desired custom SVM classifier -------------
        def test_specific():
            result = predict_test(self.nb_tweet_predict.get(), self.Resource, float(threshold_spinbox.get()),
                                  self.size_sample_p.get(), self.toggle_randomness_p.get() == "Randomised",
                                  self.toggle_nb_pos_neg_p.get() == "Equal", self.predict_kernel.get())
            self._create_viewer_panel(self.display, result)

        b_frame_2 = Frame(test_frame)
        Button(b_frame_2, text="Test a specific SVM", command=test_specific).grid()
        ToolTip(b_frame_2, text="Will test the chosen SVM classifier and measure its performance")
        b_frame_2.grid(column=0, row=0, padx=10, pady=10)

        # Test all SVM default profiles
        def test_all():
            result = predict_test(self.nb_tweet_predict.get(), self.Resource, float(threshold_spinbox.get()))
            self._create_viewer_panel(self.display, result)

        b_frame_1 = Frame(test_frame)
        Button(b_frame_1, text="Test all SVMs", command=test_all).grid()
        ToolTip(b_frame_1, text="Will test all the default SVM classifiers and measure their performances")
        b_frame_1.grid(column=1, row=0, padx=10, pady=10)

        test_frame.grid(padx=10, pady=10)

        options_frame.grid(padx=10, pady=10)

        display.add(fen_predict, text="Performance")


    def _create_actions_panel(self, display):
        fen_actions = Frame(display, name="fen_actions")

        # Trigger some specific actions #
        specific_actions = LabelFrame(fen_actions, text="Trigger specific analysis")

        # ---------- Threshold for 'Neutral' class -------------
        threshold_frame = LabelFrame(specific_actions, text="Tolerance 'Neutral'")

        default_value = StringVar()
        default_value.set("0.25")
        threshold_spinbox = Spinbox(threshold_frame, from_=0.0, to=0.80, increment=0.05, justify='center',
                                    textvariable=default_value)
        ToolTip(threshold_frame,
                text="From -'x' to +'x', where 'x' is the value selected, the label of the text will be "
                     "'Neutral'.\nIn the computation of the performance score, 'Neutral' is both considered "
                     "'Positive' and 'Negative'")
        threshold_spinbox.grid(column=0, row=0, padx=5, pady=5)

        threshold_frame.grid(row=0, padx=10, pady=10)

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
                result = analyse_text(self.value_submit.get(), self._get_classifier(), self.Resource,
                                      float(threshold_spinbox.get()))
                self._create_viewer_panel(self.display, result)

        b_frame_1 = Frame(custom_text_frame)
        Button(b_frame_1, text="Analyse text", command=text_analysis).grid()

        ToolTip(b_frame_1,
                text="Will analyse and predict the sentiment of the text.\nIt will open another tab to visualize the "
                     "result")
        b_frame_1.grid()

        custom_text_frame.grid(column=0, row=1, padx=10, pady=10)

        # ---------- Submit custom text/csv file -------------
        custom_file_frame = LabelFrame(specific_actions, text="Analyse custom file")

        def ask_file():
            file_name = askopenfile(title="Open file of tweets",
                                    filetypes=[('txt files', '.txt'), ('csv files', '.csv')])
            result = analyse_file(open(file_name, "rb").readlines(), self._get_classifier(), self.Resource,
                                  float(threshold_spinbox.get()))
            self._create_viewer_panel(self.display, result)

        Label(custom_file_frame).grid(row=0, padx=5, pady=5, )

        b_frame_2 = Frame(custom_file_frame)
        Button(b_frame_2, text="Open file & Analyse", command=ask_file).grid(row=1, sticky="s")

        ToolTip(b_frame_2,
                text="Will analyse and predict the sentiment of the file. The file is supposed to contain one tweet "
                     "per line.\nIt will open another tab to visualize the result")
        b_frame_2.grid()

        custom_file_frame.grid(column=1, row=1, padx=10, pady=10, sticky="n")

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
                result = analyse_query(self.user_query.get(), self._get_classifier(), self.Resource,
                                       float(threshold_spinbox.get()))
                self._create_viewer_panel(self.display, result)
            elif self.user_query.get() != "'#ITAR'":
                result = analyse_query('#' + self.user_query.get(), self._get_classifier(), self.Resource,
                                       float(threshold_spinbox.get()))
                self._create_viewer_panel(self.display, result)

        b_frame_3 = Frame(query_frame)
        Button(b_frame_3, text="Analyse trend", command=query_analysis).grid()
        ToolTip(b_frame_3,
                text="Will analyse and predict the sentiment of some tweets regarding the '#'.\nIt will open another "
                     "tab to visualize the result")
        b_frame_3.grid()

        query_frame.grid(column=2, row=1, padx=10, pady=10)

        # ---------- Get and analyse 'x' tweets -------------
        number_frame = LabelFrame(specific_actions, text="Collect and analyse 'x' tweets")

        self.nb_tweet_collect.set(5)

        Spinbox(number_frame, from_=5, to=1000, increment=5, textvariable=self.nb_tweet_collect, justify='center').grid(
                padx=5, pady=5)

        def analyse_stream_tweet():
            result = analyse_tweets(self.nb_tweet_collect.get(), self._get_classifier(), self.Resource,
                                    float(threshold_spinbox.get()))
            self._create_viewer_panel(self.display, result)

        b_frame_4 = Frame(number_frame)
        Button(b_frame_4, text="Analyse 'x' tweets", command=analyse_stream_tweet).grid()
        ToolTip(b_frame_4,
                text="Will analyse and predict the sentiment of 'x' tweets from the Twitter API stream.\nIt will open "
                     "another tab to visualize the result")
        b_frame_4.grid()

        number_frame.grid(column=3, row=1, padx=10, pady=10)

        specific_actions.grid(padx=10, pady=10)

        display.add(fen_actions, text="Actions")

    def _create_viewer_panel(self, display, result):
        self.count_visualiser += 1
        name_viewer = "fen_visualiser_{}".format(self.count_visualiser)

        # Frame that contain everything #
        global_frame = Frame(display)

        # ---------- Creating the list view -------------
        self.list_frame = Frame(global_frame, width=900, height=600)

        canvas_result = Canvas(self.list_frame, width=900, height=600)
        canvas_result.grid(row=1, column=0, sticky="nsew")

        fen_visualiser = Frame(canvas_result, name=name_viewer)
        canvas_result.create_window(0, 0, window=fen_visualiser)

        for idx, value in enumerate(result):
            if type(value[1]) is not type(float()):
                group_tweet = LabelFrame(fen_visualiser, text="Tweet {}".format(idx + 1))
                Label(group_tweet, text="Text :").grid(column=0, row=idx // 2, sticky="e")
                Label(group_tweet, text=bytes(value[0], 'utf-8')).grid(column=1, row=idx // 2, sticky="w")
                Label(group_tweet, text="Label :").grid(column=0, row=idx // 2 + 1, sticky="e")
                if value[1][0] == "Negative":
                    Label(group_tweet, text=value[1][0], foreground="red").grid(column=1, row=idx // 2 + 1, sticky="w")
                elif value[1][0] == "Neutral":
                    Label(group_tweet, text=value[1][0], foreground="gray").grid(column=1, row=idx // 2 + 1, sticky="w")
                elif value[1][0] == "Positive":
                    Label(group_tweet, text=value[1][0], foreground="green").grid(column=1, row=idx // 2 + 1,
                                                                                  sticky="w")
            else:
                group_tweet = LabelFrame(fen_visualiser, text="Classifier {}".format(idx + 1))
                Label(group_tweet, text="Classifier :").grid(column=0, row=idx // 2, sticky="e")
                Label(group_tweet, text=readable_name_classifier(value[0])).grid(column=1, row=idx // 2, sticky="w")
                Label(group_tweet, text="Score (%) :").grid(column=0, row=idx // 2 + 1, sticky="e")
                Label(group_tweet, text=value[1], foreground="blue").grid(column=1, row=idx // 2 + 1, sticky="w")
            group_tweet.grid(sticky="w")

        vertical_scrollbar = Scrollbar(self.list_frame, command=canvas_result.yview)
        canvas_result.configure(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = Scrollbar(self.list_frame, orient=HORIZONTAL, command=canvas_result.xview)
        canvas_result.configure(xscrollcommand=horizontal_scrollbar.set)

        vertical_scrollbar.grid(row=1, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=2, column=0, sticky="ew")

        def update_scroll_region(event):
            canvas_result.configure(scrollregion=canvas_result.bbox("all"))

        fen_visualiser.bind("<Configure>", update_scroll_region)

        # ---------- Creating the graphic view -------------
        self.graphic_frame = Frame(global_frame, width=900, height=600)

        self.fig = Figure(figsize=(11, 7), dpi=96, tight_layout=True)

        # Case : result of 'Performance' (measure the performance)
        if type(result[0][1]) is not type(tuple()):
            ax = self.fig.add_subplot(111)
            ax.grid(True)

            for idx, value in enumerate(result):
                if "linear" in value[0]:
                    ax.barh(value[0], value[1], color="red")
                elif "poly" in value[0]:
                    ax.barh(value[0], value[1], color="green")
                elif "gaussian" in value[0]:
                    ax.barh(value[0], value[1], color="blue")
                elif "radial" in value[0]:
                    ax.barh(value[0], value[1], color="orange")
                ax.text(value[1], idx, str(value[1]))
            graph = FigureCanvasTkAgg(self.fig, self.graphic_frame)
            canvas = graph.get_tk_widget()
            canvas.grid()

        # Case : result of 'Actions' (predict the sentiment)
        else:
            def create_graphic(result, dic):
                """
                Create a 2D or 3D graphic depending on the number of selected variables in the dictionary or if
                result contains 'Performance' outcome (performances of SVM classifier) or 'Actions' outcome (containing
                tweet, sentiment and characteristic vector)
                :param result: list of element to be used in the creation of the graphic
                :param dic: dictionary containing all the IntVar of every variable selectable and the number of
                selected variable. Used to create the graphic
                :return:
                """
                try:
                    self.canvas.grid_forget()
                except:
                    pass

                labels, vectors, graph_values = list(), list(), list()
                for element in result:
                    labels.append(element[1][0])
                    vectors.append(element[1][1][0])
                for index, key in enumerate(dic):
                    if key is not "count":
                        if dic[key].get():
                            graph_values.append([t[index] for t in vectors])

                if dic["count"] == 2:
                    ax = self.fig.add_subplot(111)
                    dic_count = dict()
                    for index, label in enumerate(labels):
                        if label == "Negative":
                            color = "red"
                        elif label == "Positive":
                            color = "green"
                        else:
                            color = "blue"
                        try:
                            dic_count[str(graph_values[0][index]) + str(graph_values[1][index])] += 1
                        except:
                            dic_count[str(graph_values[0][index]) + str(graph_values[1][index])] = 1
                        ax.scatter(graph_values[0][index], graph_values[1][index],
                                   s=min(dic_count[str(graph_values[0][index]) + str(graph_values[1][index])] * 50,
                                         2000),
                                   c=color,
                                   alpha=0.25)
                else:
                    ax = self.fig.add_subplot(111, projection="3d")
                    dic_count = dict()
                    for index, label in enumerate(labels):
                        if label == "Negative":
                            color = "red"
                        elif label == "Positive":
                            color = "green"
                        else:
                            color = "blue"
                        try:
                            dic_count[str(graph_values[0][index]) + str(graph_values[1][index]) + str(
                                    graph_values[2][index])] += 1
                        except:
                            dic_count[str(graph_values[0][index]) + str(graph_values[1][index]) + str(
                                    graph_values[2][index])] = 1
                        ax.scatter(graph_values[0][index], graph_values[1][index], graph_values[2][index],
                                   s=min(dic_count[str(graph_values[0][index]) + str(graph_values[1][index]) + str(
                                           graph_values[2][index])] * 50, 2000), c=color, alpha=0.25)
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                graph = FigureCanvasTkAgg(self.fig, self.graphic_frame)
                self.canvas = graph.get_tk_widget()
                self.canvas.grid()


            def select_variable(value, dic, result):
                """
                Track and control the number of selected variables (up to 3) and initiate the creation of the graphic
                if enough are selected.
                :param value: IntVar associated with the Checkbutton that have triggered this call
                :param dic: dictionary containing all the IntVar of every variable selectable and the number of
                selected variable. Used to create the graphic
                :param result: list of element to be used in the creation of the graphic
                :return:
                """
                if value.get() and dic["count"] == 3:
                    value.set(0)
                elif value.get() and dic["count"] < 3:
                    dic["count"] += 1
                else:
                    dic["count"] -= 1

                if 2 <= dic["count"] <= 3:
                    create_graphic(result, dic)

            # ---------- Choos the variables to be used in the graphic -------------
            select_frame = LabelFrame(self.graphic_frame, text="Select 3 variables")
            dict_variable = {
                "pos_word":     IntVar(),
                "neg_word":     IntVar(),
                "pos_emoticon": IntVar(),
                "neg_emoticon": IntVar(),
                "negation":     IntVar(),
                "count":        0
            }
            dict_variable["pos_word"].set(1)
            dict_variable["count"] += 1
            Checkbutton(select_frame, text="Positive Words",
                        command=partial(select_variable, dict_variable["pos_word"], dict_variable, result),
                        variable=dict_variable["pos_word"]).grid(row=0, column=0, padx=5, pady=5)
            dict_variable["neg_word"].set(0)
            Checkbutton(select_frame, text="Negative Words",
                        command=partial(select_variable, dict_variable["neg_word"], dict_variable, result),
                        variable=dict_variable["neg_word"]).grid(row=0, column=1, padx=5, pady=5)
            dict_variable["pos_emoticon"].set(1)
            dict_variable["count"] += 1
            Checkbutton(select_frame, text="Positive Emoticons",
                        command=partial(select_variable, dict_variable["pos_emoticon"], dict_variable, result),
                        variable=dict_variable["pos_emoticon"]).grid(row=0, column=2, padx=5, pady=5)
            dict_variable["neg_emoticon"].set(0)
            Checkbutton(select_frame, text="Negative Emoticons",
                        command=partial(select_variable, dict_variable["neg_emoticon"], dict_variable, result),
                        variable=dict_variable["neg_emoticon"]).grid(row=0, column=3, padx=5, pady=5)
            dict_variable["negation"].set(1)
            dict_variable["count"] += 1
            Checkbutton(select_frame, text="Negation",
                        command=partial(select_variable, dict_variable["negation"], dict_variable, result),
                        variable=dict_variable["negation"]).grid(row=0, column=4, padx=5, pady=5)

            select_frame.grid(padx=10, pady=10)

            # ---------- Indicate the meaning of the color -------------
            legend_frame = LabelFrame(self.graphic_frame, text="Legend about color")

            Label(legend_frame, background="red", width=3).grid(row=0, column=0, padx=5, pady=5)
            Label(legend_frame, text="Negative").grid(row=0, column=1, padx=5, pady=5)
            Label(legend_frame, background="gray", width=3).grid(row=0, column=2, padx=5, pady=5)
            Label(legend_frame, text="Neutral").grid(row=0, column=3, padx=5, pady=5)
            Label(legend_frame, background="green", width=3).grid(row=0, column=4, padx=5, pady=5)
            Label(legend_frame, text="Positive").grid(row=0, column=5, padx=5, pady=5)

            ToolTip(legend_frame,
                    text="The bigger and the more contrast of a dot means that they are a lot of vectors at the same position")

            legend_frame.grid(padx=10, pady=10)

            create_graphic(result, dict_variable)

        # ---------- Action to change the view and close tab -------------
        action_frame = LabelFrame(global_frame, text="Tab actions")

        self.active_view.set("Graphic view")

        def activate_view():
            if self.active_view.get() == "List view":
                self.list_frame.grid()
                self.graphic_frame.grid_forget()
            else:
                self.list_frame.grid_forget()
                self.graphic_frame.grid()

        Checkbutton(action_frame, textvariable=self.active_view, variable=self.active_view, onvalue="Graphic view",
                    offvalue="List view", command=activate_view).grid(column=0, row=0, padx=5, pady=5)

        def close_tab():
            display.forget(self.count_visualiser + 3)
            self.count_visualiser -= 1

        Button(action_frame, command=close_tab, text="Close tab").grid(column=1, row=0, padx=5, pady=5)

        action_frame.grid(padx=10, pady=10)

        activate_view()

        display.add(global_frame, text="Visualiser {}".format(self.count_visualiser))
