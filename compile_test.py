#import safetensors
from fugashi import Tagger
# import transformers
# import torch
import customtkinter
import traceback

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # try:
        tagger = Tagger('-Owakati')
        # except:
        #     with open('error.txt', mode='w') as f:
        #         traceback.print_exc(file=f)
        # フォームサイズ設定
        self.geometry("1200x600")
        self.state('zoomed')
        self.title("compile test")

        # CustomTkinter のフォームデザイン設定
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        

if __name__ == "__main__":
    # アプリケーション実行
    app = App()

    app.mainloop()
