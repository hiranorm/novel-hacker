# coding: utf-8
import os
from PIL import Image
import difflib
from fugashi import Tagger
import threading
import re
import sys

import random
import unicodedata
import collections

import torch
from transformers import BertJapaneseTokenizer, BertForMaskedLM
import pytorch_lightning as pl

import tkinter
import customtkinter

from tkinter import filedialog as tkfd

class ConstantData:
    def __init__(self):
        self.TITLE = " Write Hacker"
        self.FONT_TYPE = "meiryo"
        self.FILE_TYPES=[("テキストファイル","*.txt"),("マークダウンファイル","*.md"),("Pythonファイル","*.py")]
        self.IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

class UserData:
    def __init__(self):
        self.font_size = 14

constant_data = ConstantData()
user_data = UserData()

def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)

class TextFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        # create scrollable textbox
        self.tk_textbox = customtkinter.CTkTextbox(master=self, font=(constant_data.FONT_TYPE, user_data.font_size))
        self.tk_textbox.grid(row=0, column=0, sticky="nsew")
        self.tk_textbox.tag_config("attention", background="yellow", foreground="red")
        self.tk_textbox.tag_config("fix", background="cyan",  foreground="blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #メンバー変数の設定
        self.fonts = (constant_data.FONT_TYPE, 15)
        self.task_list = ("typo","sentence_end","near_word")
        self.task_name = "typo"

        # フォームサイズ設定
        self.geometry("1200x600")
        self.state('zoomed')
        self.title(constant_data.TITLE)

        # CustomTkinter のフォームデザイン設定
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.setup_image()

        self.setup_navigation()
        self.setup_right_frame()
        # select default frame
        self.select_frame_by_name(self.task_name)

    def get_analyzer(self):
        self.analyser = Analyser()
        self.do_button.configure(state='normal')

    def setup_image(self):
        # 画像の定義
        self.logo_image = customtkinter.CTkImage(
            Image.open(find_data_file("images/write_hacker_logo.png")),
            size=(20, 20)
        )
        self.image_icon_image = customtkinter.CTkImage(
            Image.open(find_data_file("images/image_icon_light.png")),
            size=(20, 20)
        )
        self.read_image = customtkinter.CTkImage(
            light_image=Image.open(find_data_file("images/read_dark.png")),
            dark_image=Image.open(find_data_file("images/read_light.png")),
            size=(20, 20)
        )
        self.save_image = customtkinter.CTkImage(
            light_image=Image.open(find_data_file("images/save_dark.png")),
            dark_image=Image.open(find_data_file("images/save_light.png")),
            size=(20, 20)
        )
        self.typo_image = customtkinter.CTkImage(
            light_image=Image.open(find_data_file("images/pencil_dark.png")),
            dark_image=Image.open(find_data_file("images/pencil_light.png")),
            size=(20, 20)
        )
        self.prev_image = customtkinter.CTkImage(
            light_image=Image.open(find_data_file("images/prev_dark.png")),
            dark_image=Image.open(find_data_file("images/prev_light.png")),
            size=(20, 20)
        )
        self.next_image = customtkinter.CTkImage(
            light_image=Image.open(find_data_file("images/next_dark.png")),
            dark_image=Image.open(find_data_file("images/next_light.png")),
            size=(20, 20)
        )
        self.chat_image = customtkinter.CTkImage(
            light_image=Image.open(find_data_file("images/paper_dark.png")),
            dark_image=Image.open(find_data_file("images/paper_light.png")), size=(20, 20)
        )
        self.map_image = customtkinter.CTkImage(
            light_image=Image.open(find_data_file("images/map_dark.png")),
            dark_image=Image.open(find_data_file("images/map_light.png")), size=(20, 20)
        )
        self.kosoado_image = customtkinter.CTkImage(
            light_image=Image.open(find_data_file("images/finger_dark.png")),
            dark_image=Image.open(find_data_file("images/finger_light.png")), size=(20, 20)
        )
        self.normalize_image = customtkinter.CTkImage(
            light_image=Image.open(find_data_file("images/normalize_dark.png")),
            dark_image=Image.open(find_data_file("images/normalize_light.png")), size=(20, 20)
        )
        self.data_image = customtkinter.CTkImage(
            light_image=Image.open(find_data_file("images/data_dark.png")),
            dark_image=Image.open(find_data_file("images/data_light.png")), size=(20, 20)
        )


    def setup_navigation(self):
        # ナビゲーションバー設定
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        # self.navigation_frame.grid_rowconfigure(0, weight=1)
        # self.navigation_frame.grid_rowconfigure(1, weight=1)
        # self.navigation_frame.grid_rowconfigure(2, weight=1)
        # self.navigation_frame.grid_rowconfigure(3, weight=1)
        # self.navigation_frame.grid_rowconfigure(4, weight=1)
        # self.navigation_frame.grid_rowconfigure(5, weight=1)
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text=constant_data.TITLE, image=self.logo_image,
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.typo_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="誤字脱字チェック",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.typo_image,
            anchor="w",
            command=self.typo_button_event
        )
        self.typo_button.grid(row=1, column=0, sticky="ew")

        self.sentence_end_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="文末重複チェック",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.chat_image,
            anchor="w",
            command=self.sentence_end_button_event
        )
        self.sentence_end_button.grid(row=2, column=0, sticky="ew")

        self.near_word_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="単語近傍チェック",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.map_image,
            anchor="w",
            command=self.near_word_button_event
        )
        self.near_word_button.grid(row=3, column=0, sticky="ew")

        self.kosoado_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="こそあど言葉チェック",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.kosoado_image,
            anchor="w",
            command=self.kosoado_button_event
        )
        self.kosoado_button.grid(row=4, column=0, sticky="ew")

        self.normalize_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="正規化チェック",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.normalize_image,
            anchor="w",
            command=self.normalize_button_event
        )
        self.normalize_button.grid(row=5, column=0, sticky="ew")

        self.char_size_frame = customtkinter.CTkFrame(
            self.navigation_frame,
            fg_color="transparent",
        )
        self.char_size_frame.grid(
            row=6,
            column=0,
            padx=20,
            pady=20,
            sticky="sew"
        )
        self.char_size_frame.grid_columnconfigure(0, weight=1)
        self.char_size_frame.grid_columnconfigure(1, weight=1)

        self.char_size_label = customtkinter.CTkLabel(
            self.char_size_frame,
            corner_radius=0,
            height=40,
            text="文字サイズ",
            fg_color="transparent",
            text_color=("gray10", "gray90")
        )
        self.char_size_label.grid(
            row=0,
            column=0,
            padx=20,
            sticky="w"
        )

        self.char_size_menu = customtkinter.CTkOptionMenu(
            self.char_size_frame,
            values=["8", "10", "12", "14", "16", "18", "20", "24"],
            command=self.set_char_size,
            width=100
        )
        self.char_size_menu.set("14")
        self.char_size_menu.grid(
            row=0,
            column=1,
            sticky="w"
        )

        self.appearance_frame = customtkinter.CTkFrame(
            self.navigation_frame,
            fg_color="transparent"
        )
        self.appearance_frame.grid(
            row=7,
            column=0,
            padx=20,
            pady=20,
            sticky="ew"
        )
        self.appearance_frame.grid_columnconfigure(0, weight=1)
        self.appearance_frame.grid_columnconfigure(1, weight=1)

        self.appearance_label = customtkinter.CTkLabel(
            self.appearance_frame,
            corner_radius=0,
            height=40,
            text="モード設定",
            fg_color="transparent",
            text_color=("gray10", "gray90")
        )
        self.appearance_label.grid(
            row=0,
            column=0,
            padx=20,
            sticky="w",
        )

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.appearance_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
            width=100,
        )
        self.appearance_mode_menu.grid(
            row=0,
            column=1,
            sticky="w"
        )

    def setup_right_frame(self):
        # 誤字脱字の右側の定義
        self.right_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)

        self.right_left_bar = customtkinter.CTkFrame(self.right_frame, corner_radius=0, fg_color="transparent")
        self.right_left_bar.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.right_right_bar = customtkinter.CTkFrame(self.right_frame, corner_radius=0, fg_color="transparent")
        self.right_right_bar.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        self.right_right_bar.grid_columnconfigure(2, weight=1)

        self.text_frame = TextFrame(self.right_frame, corner_radius=0, fg_color="transparent")
        self.text_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        # 左バー
        self.right_frame_button_1 = customtkinter.CTkButton(
            self.right_left_bar,
            text="読み込み",
            image=self.read_image,
            command=self.read_file
        )
        self.right_frame_button_1.grid(row=0, column=0, padx=20, pady=10,sticky="nsew")
        self.right_frame_button_2 = customtkinter.CTkButton(
            self.right_left_bar,
            text="保存",
            image=self.save_image,
            command=self.save_file
        )
        self.right_frame_button_2.grid(row=0, column=1, padx=20, pady=10,sticky="nsew")

        # 右バー
        self.do_button = customtkinter.CTkButton(
            self.right_right_bar,
            text="チェック実行",
            image=self.typo_image,
            command=self.do_check_event,
            text_color=("gray10", "gray90"),
            text_color_disabled=("gray10", "gray90"),
            state='disabled',
            #compound="top"
        )
        self.do_button.grid(row=0, column=2, padx=20, pady=10, sticky="nse")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.typo_button.configure(fg_color=("gray75", "gray25") if name == "typo" else "transparent")
        self.sentence_end_button.configure(fg_color=("gray75", "gray25") if name == "sentence_end" else "transparent")
        self.near_word_button.configure(fg_color=("gray75", "gray25") if name == "near_word" else "transparent")
        self.kosoado_button.configure(fg_color=("gray75", "gray25") if name == "kosoado" else "transparent")
        self.normalize_button.configure(fg_color=("gray75", "gray25") if name == "normalize" else "transparent")

        # show selected frame
        self.task_name = name
        if self.task_name in ("typo","sentence_end","near_word","kosoado","normalize"):
            self.right_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.right_frame.grid_forget()

    def typo_button_event(self):
        self.select_frame_by_name("typo")

    def sentence_end_button_event(self):
        self.select_frame_by_name("sentence_end")

    def near_word_button_event(self):
        self.select_frame_by_name("near_word")

    def kosoado_button_event(self):
        self.select_frame_by_name("kosoado")

    def normalize_button_event(self):
        self.select_frame_by_name("normalize")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def do_check_event(self):
        left_text = self.text_frame.tk_textbox.get("0.0", "end")
        if self.task_name == "typo":
            result_text = self.check_typo(left_text)
        elif self.task_name == "sentence_end":
            result_text = self.check_sentence_end(left_text)
        elif self.task_name == "near_word":
            result_text = self.check_near_words(left_text)
        elif self.task_name == "kosoado":
            result_text = self.check_kosoado(left_text)
        elif self.task_name == "normalize":
            result_text = self.check_normalize(left_text)


    def set_char_size(self, size):
        user_data.font_size = int(size)
        input_text = self.text_frame.tk_textbox.get("0.0", "end")
        self.text_reload()
        self.text_frame.tk_textbox.insert("0.0", input_text)

    def text_reload(self):
        self.text_frame = TextFrame(self.right_frame, corner_radius=0, fg_color="transparent")
        self.text_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    def read_file(self):
        read_filename = tkfd.askopenfilename(filetypes=constant_data.FILE_TYPES)
        if len(read_filename)==0:
            return
        with open(read_filename) as f:
            input_text = f.read()
            self.text_frame.tk_textbox.delete("0.0", index2="end")
            self.text_frame.tk_textbox.insert("0.0", input_text)
        return

    def save_file(self):
        save_filename = tkfd.asksaveasfilename(filetypes=constant_data.FILE_TYPES)
        if len(save_filename)==0:
            return
        with open(save_filename, mode='w') as f:
            f.write(self.text_frame.tk_textbox.get("0.0", "end"))
        return

    def check_typo(self, input_text):
        self.text_frame.tk_textbox.delete("0.0", index2="end")
        self.analyser.insert_typo_text(input_text, self.text_frame.tk_textbox)
        return

    def check_sentence_end(self, input_text):
        self.text_frame.tk_textbox.delete("0.0", index2="end")
        self.analyser.insert_sentence_end_text(input_text, self.text_frame.tk_textbox)
        return

    def check_near_words(self, input_text):
        self.text_frame.tk_textbox.delete("0.0", index2="end")
        self.analyser.insert_near_words(input_text, self.text_frame.tk_textbox)
        return

    def check_kosoado(self, input_text):
        self.text_frame.tk_textbox.delete("0.0", index2="end")
        self.analyser.insert_kosoado(input_text, self.text_frame.tk_textbox)
        return

    def check_normalize(self, input_text):
        self.text_frame.tk_textbox.delete("0.0", index2="end")
        self.analyser.insert_normalize(input_text, self.text_frame.tk_textbox)
        return

class Analyser:
    def __init__(self):
        self.color_dic = {
            'red':'<span style="color: red;">',
            'yellow':'<span style="background-color:yellow; color: black;">',
            'end':'</span>'
        }
        self.sentence_end_marks = ('。','」','】','!','?','！','？',)
        self.bert_model = 'cl-tohoku/bert-base-japanese-whole-word-masking'
        self.best_model_path = find_data_file("models/calibration_model_cpu_20230702.ckpt")

        self.tokenizer = SC_tokenizer.from_pretrained(self.bert_model)

        model = BertForMaskedLM_pl.load_from_checkpoint(self.best_model_path)
        self.bert_mlm = model.bert_mlm
        del model
        self.tagger = Tagger('-Owakati')

    def insert_diff_hl(self, origin, correct, text_frame):
        """
        文字列の差異をハイライト表示する
        """
        d = difflib.Differ()

        diffs = d.compare(origin, correct)

        result = ''
        for diff in diffs:
            status, _, character = list(diff)
            if status == '-':
                text_frame.insert("end", self.decode_char(character), "attention")
            elif status == '+':
                text_frame.insert("end", self.decode_char(character), "fix")
            else:
                text_frame.insert("end", self.decode_char(character))

        return

    def insert_typo_text(self, input_text, text_frame):
        input_text = self.encode_char(input_text)
        word_nodes = self.tagger(input_text)

        texts = []
        sentence = ""
        for word_node in word_nodes:
            sentence += word_node.surface
            if word_node.surface in self.sentence_end_marks:
                texts.append(sentence)
                sentence = ""

        for text in texts:
            text = unicodedata.normalize('NFKC', text)
            predict_text = self.predict_cpu(text)
            self.insert_diff_hl(text, predict_text, text_frame)
        return

    def predict_cpu(self, text):
        """
        文章を入力として受け、BERTが予測した文章を出力
        """
        # 符号化
        encoding, spans = self.tokenizer.encode_plus_untagged(
            text, return_tensors='pt'
        )
        encoding = { k: v for k, v in encoding.items() }

        # ラベルの予測値の計算
        with torch.no_grad():
            output = self.bert_mlm(**encoding)
            scores = output.logits
            labels_predicted = scores[0].argmax(-1).cpu().numpy().tolist()

        # ラベル列を文章に変換
        predict_text = self.tokenizer.convert_bert_output_to_text(
            text, labels_predicted, spans
        )

        return predict_text

    def encode_char(self, input_text):
        input_text = re.sub("\n",'@',input_text) #改行コード
        input_text = re.sub("　","■", input_text) #全角スペース
        input_text = re.sub(" ","★", input_text) #半角スペース
        input_text = re.sub(",","●", input_text) #カンマ
        return input_text

    def decode_char(self, input_text):
        input_text = re.sub('@', "\n",input_text) #改行コード
        input_text = re.sub("■", "　", input_text) #全角スペース
        input_text = re.sub("★", " ", input_text) #半角スペース
        input_text = re.sub("●", "," , input_text) #カンマ
        return input_text

    def insert_sentence_end_text(self, input_text, text_frame):
        input_text = self.encode_char(input_text)
        word_nodes = self.tagger(input_text)
        words = [word_node.surface for word_node in word_nodes]

        sentences = []
        sentence = []
        for word in words:
            sentence.append(word)
            if word in self.sentence_end_marks:
                sentences.append(sentence)
                sentence = []
        for si, sentence in enumerate(sentences):
            if len(sentence)<2:
                for wi, word in enumerate(sentence):
                    text_frame.insert("end", self.decode_char(word))
                continue
            else:
                pass

            if si == 0:
                if len(sentences[si+1])>1 and sentences[si+1][-2] == sentence[-2]:
                    for wi, word in enumerate(sentence):
                        if wi == len(sentence)-2:
                            text_frame.insert("end", self.decode_char(word), "attention")
                        else:
                            text_frame.insert("end", self.decode_char(word))
                else:
                    for wi, word in enumerate(sentence):
                        text_frame.insert("end", self.decode_char(word))
            elif si == len(sentences)-1:
                if len(sentences[si-1])>1 and sentences[si-1][-2] == sentence[-2]:
                    for wi, word in enumerate(sentence):
                        if wi == len(sentence)-2:
                            text_frame.insert("end", self.decode_char(word), "attention")
                        else:
                            text_frame.insert("end", self.decode_char(word))
                else:
                    for wi, word in enumerate(sentence):
                        text_frame.insert("end", self.decode_char(word))
            else:
                if (
                    len(sentences[si-1])>1 and sentences[si-1][-2] == sentence[-2]
                ) or (
                    len(sentences[si+1])>1 and sentences[si+1][-2] == sentence[-2]
                ):
                    for wi, word in enumerate(sentence):
                        if wi == len(sentence)-2:
                            text_frame.insert("end", self.decode_char(word), "attention")
                        else:
                            text_frame.insert("end", self.decode_char(word))
                else:
                    for wi, word in enumerate(sentence):
                        text_frame.insert("end", self.decode_char(word))

        return

    def insert_near_words(self, input_text, text_frame):
        input_text = self.encode_char(input_text)
        word_nodes = self.tagger(input_text)

        total_words = []
        sentence_words = []
        for wi, word in enumerate(word_nodes):
            sentence_words.append(word)
            if word.surface in self.sentence_end_marks:
                total_words.append(sentence_words)
                sentence_words = []
        del sentence_words
        if len(total_words) == 1:
            text_frame.insert("end", self.encode_char(input_text))
            return

        output_text = ""
        for si, sentence in enumerate(total_words):
            for wi, word in enumerate(sentence):
                if word.pos.split(',')[0] in ("代名詞","名詞","動詞","形容詞"):
                    pass
                else:
                    text_frame.insert("end", self.decode_char(word.surface))
                    continue

                if si == 0 and word.surface in [word_node.surface for word_node in total_words[si+1]]:
                    text_frame.insert("end", self.decode_char(word.surface), "attention")
                elif si == len(total_words)-1 and \
                    word.surface in [word_node.surface for word_node in total_words[si-1]]:
                    text_frame.insert("end", self.decode_char(word.surface), "attention")
                elif (si != 0 and si != len(total_words)-1) and \
                    ((word.surface in [word_node.surface for word_node in total_words[si-1]]) or \
                    (word.surface in [word_node.surface for word_node in total_words[si+1]])):
                    text_frame.insert("end", self.decode_char(word.surface), "attention")
                else:
                    text_frame.insert("end", self.decode_char(word.surface))
        return

    def insert_kosoado(self, input_text, text_frame):
        input_text = self.encode_char(input_text)
        word_nodes = self.tagger(input_text)

        output_text = ""
        for word_node in word_nodes:
            if word_node.pos.split(',')[0] == "代名詞":
                text_frame.insert("end", self.decode_char(word_node.surface), "attention")
            else:
                text_frame.insert("end", self.decode_char(word_node.surface))
        return

    def insert_normalize(self, input_text, text_frame):
        input_text = self.encode_char(input_text)
        normalize_text = unicodedata.normalize('NFKC', input_text)
        self.insert_diff_hl(input_text, normalize_text, text_frame)
        return

class SC_tokenizer(BertJapaneseTokenizer):

    def encode_plus_tagged(
        self, wrong_text, correct_text, max_length=128
    ):
        """
        ファインチューニング時に使用。
        誤変換を含む文章と正しい文章を入力とし、
        符号化を行いBERTに入力できる形式にする。
        """
        # 誤変換した文章をトークン化し、符号化
        encoding = self(
            wrong_text,
            max_length=max_length,
            padding='max_length',
            truncation=True
        )
        # 正しい文章をトークン化し、符号化
        encoding_correct = self(
            correct_text,
            max_length=max_length,
            padding='max_length',
            truncation=True
        )
        # 正しい文章の符号をラベルとする
        encoding['labels'] = encoding_correct['input_ids']

        return encoding

    def encode_plus_untagged(
        self, text, max_length=None, return_tensors=None
    ):
        """
        文章を符号化し、それぞれのトークンの文章中の位置も特定しておく。
        """
        # 文章のトークン化を行い、
        # それぞれのトークンと文章中の文字列を対応づける。
        tokens = [] # トークンを追加していく。
        tokens_original = [] # トークンに対応する文章中の文字列を追加していく。
        words = self.word_tokenizer.tokenize(text) # MeCabで単語に分割

        for word in words:
            # 単語をサブワードに分割
            tokens_word = self.subword_tokenizer.tokenize(word)
            tokens.extend(tokens_word)
            if tokens_word[0] == '[UNK]': # 未知語への対応
                tokens_original.append(word)
            else:
                tokens_original.extend([
                    token.replace('##','') for token in tokens_word
                ])

        # 各トークンの文章中での位置を調べる。（空白の位置を考慮する）
        position = 0
        spans = [] # トークンの位置を追加していく。
        for token in tokens_original:
            l = len(token)
            while 1:
                if token != text[position:position+l]:
                    position += 1
                else:
                    spans.append([position, position+l])
                    position += l
                    break

        # 符号化を行いBERTに入力できる形式にする。
        input_ids = self.convert_tokens_to_ids(tokens)
        encoding = self.prepare_for_model(
            input_ids,
            max_length=max_length,
            padding='max_length' if max_length else False,
            truncation=True if max_length else False
        )
        sequence_length = len(encoding['input_ids'])
        # 特殊トークン[CLS]に対するダミーのspanを追加。
        spans = [[-1, -1]] + spans[:sequence_length-2]
        # 特殊トークン[SEP]、[PAD]に対するダミーのspanを追加。
        spans = spans + [[-1, -1]] * ( sequence_length - len(spans) )

        # 必要に応じてtorch.Tensorにする。
        if return_tensors == 'pt':
            encoding = { k: torch.tensor([v]) for k, v in encoding.items() }

        return encoding, spans

    def convert_bert_output_to_text(self, text, labels, spans):
        """
        推論時に使用。
        文章と、各トークンのラベルの予測値、文章中での位置を入力とする。
        そこから、BERTによって予測された文章に変換。
        """
        assert len(spans) == len(labels)

        # labels, spansから特殊トークンに対応する部分を取り除く
        labels = [label for label, span in zip(labels, spans) if span[0]!=-1]
        spans = [span for span in spans if span[0]!=-1]

        # BERTが予測した文章を作成
        predicted_text = ''
        position = 0
        for label, span in zip(labels, spans):
            start, end = span
            if position != start: # 空白の処理
                predicted_text += text[position:start]
            predicted_token = self.convert_ids_to_tokens(label)
            predicted_token = predicted_token.replace('##', '')
            predicted_token = unicodedata.normalize(
                'NFKC', predicted_token
            )
            predicted_text += predicted_token
            position = end

        return predicted_text

class BertForMaskedLM_pl(pl.LightningModule):

    def __init__(self, model_name, lr):
        super().__init__()
        self.save_hyperparameters()
        self.bert_mlm = BertForMaskedLM.from_pretrained(model_name)

    def training_step(self, batch, batch_idx):
        output = self.bert_mlm(**batch)
        loss = output.loss
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        output = self.bert_mlm(**batch)
        val_loss = output.loss
        self.log('val_loss', val_loss)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)


if __name__ == "__main__":
    # アプリケーション実行
    app = App()

    thread1 = threading.Thread(target=app.get_analyzer)
    thread1.start()

    app.mainloop()

