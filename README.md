# write_hacker
小説編集・作成用アプリ。

kivy使用予定。

とりあえず自分が使いやすいものを作る。


## レイアウト
- AnchorLayout : ウィジェットを上下左右と中央に配置。
- BoxLayout : 同サイズのウィジェットを垂直・水平方向に配置。
- FloatLayout : ウィジェットを絶対座標で配置。
- RelativeLayout : ウィジェットを相対座標で配置。
- GridLayout : ウィジェットをグリッド状に配置。
- PageLayout : ウィジェットをページ状に配置。
- ScatterLayout : ウィジェットをRelativeLayoutと同様に配置。マウスによるサイズ変更も可能。
- StackLayout : 個別サイズのウィジェットを垂直・水平方向に配置。

## ボタンの属性
- text : テキスト
- font_size : フォントサイズ
- bold : 太字
- italic : イタリック
- color : 文字色
- background_color : 背景色
- pos : 位置
- size : サイズ

## テキスト入力の属性
・text : テキスト
・font_size : フォントサイズ
・pos : 位置
・size : サイズ

## kivy公式ドキュメント
https://pyky.github.io/kivy-doc-ja/

## 類語提示機能
### wordnet公式ドキュメント
https://wordnet.princeton.edu/documentation

### 日本語ワードネット
https://bond-lab.github.io/wnja/


# customtkinterで作り直し
## customtkinterの利点
モダンな見た目と、学習量が少ないこと。
pythonで自然言語処理を行う都合上、同じ言語でつくりたいから。
また、アプリにしたいのは、ローカルで行いたいから。
一旦自分用に作成する。

## customtkinter公式
https://customtkinter.tomschimansky.com/

## ビルドコマンド

## fugashiを含む
pyinstaller --onefile --noconsole --windowed --noconfirm --clean --icon icon.icns --add-data "/Users/hiran0rm/write_hacker/venv/lib/python3.11/site-packages/customtkinter:customtkinter/" --add-data "/Users/hiran0rm/write_hacker/images:images/" --add-data "/Users/hiran0rm/write_hacker/models:models/" --exclude pandas --collect-data unidic_lite --hidden-import unidic_lite --collect-data ipadic --hidden-import ipadic --hidden-import=pytorch --collect-data torch --copy-metadata torch --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --copy-metadata importlib_metadata --collect-binaries functorch app.py

--key 暗号化

## onefile化しない
pyinstaller --onedir --noconsole --windowed --noconfirm --clean --icon icon.icns --add-data "/Users/hiran0rm/write_hacker/venv/lib/python3.11/site-packages/customtkinter:customtkinter/" --add-data "/Users/hiran0rm/write_hacker/images:images/" --add-data "/Users/hiran0rm/write_hacker/models:models/" --exclude pandas --collect-data unidic_lite --hidden-import unidic_lite --collect-data ipadic --hidden-import ipadic --hidden-import=pytorch --collect-data torch --copy-metadata torch --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata sacremoses --copy-metadata numpy --copy-metadata tokenizers --copy-metadata importlib_metadata --collect-binaries functorch app.py



pyinstaller --onefile --noconsole --windowed --noconfirm --clean --icon icon.icns --add-data "/Users/hiran0rm/write_hacker/venv/lib/python3.11/site-packages/customtkinter:customtkinter/" --add-data "/Users/hiran0rm/write_hacker/images:images/" --exclude pandas --collect-data unidic_lite --hidden-import unidic_lite --collect-data ipadic --hidden-import ipadic  --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy  --copy-metadata importlib_metadata app_free.py


pyinstaller app.spec --clean --noconfirm


exeの前に追加
```
Key = ['mkl']

def remove_from_list(input, keys):
    outlist = []
    for item in input:
        name, _, _ = item
        flag = 0
        for key_word in keys:
            if name.find(key_word) > -1:
                flag = 1
        if flag != 1:
            outlist.append(item)
    return outlist

a.binaries = remove_from_list(a.binaries, Key)
```




# Nuitkaは諦める
pip install Nuitka zstandard ordered-set imageio
condaでインストールしたnuitkaではうまくいかない。

```
nuitka3 --standalone --nofollow-import-to=torch --follow-imports --enable-plugin=tk-inter  --noinclude-setuptools-mode=nofollow --include-data-dir=/Users/hiran0rm/write_hacker/images=./images/ --include-data-dir=/Users/hiran0rm/write_hacker/models=./models/ --include-data-dir=/Users/hiran0rm/write_hacker/torch=./torch/ --macos-create-app-bundle --macos-app-icon='icon.icns' --tcl-library-dir='/usr/local/Cellar/tcl-tk/8.6.13_4/lib' --tk-library-dir='/usr/local/Cellar/tcl-tk/8.6.13_4/lib' app.py

python -m nuitka --onefile --standalone --follow-imports --enable-plugin=tk-inter --noinclude-pytest-mode=nofollow --noinclude-IPython-mode=nofollow --noinclude-setuptools-mode=nofollow --include-data-dir='/Users/hiran0rm/write_hacker/images=./images/'  --macos-create-app-bundle --macos-app-icon='images/write_hacker_logo.png' --tcl-library-dir='/usr/local/Cellar/tcl-tk/8.6.13_4/lib' --tk-library-dir='/usr/local/Cellar/tcl-tk/8.6.13_4/lib' app_free.py

python -m nuitka --standalone --disable-console --follow-imports --enable-plugin=tk-inter --noinclude-setuptools-mode=nofollow --macos-create-app-bundle --macos-app-icon='icon.icns' --include-data-dir='/Users/hiran0rm/write_hacker/images=./images/' --tcl-library-dir='/usr/local/Cellar/tcl-tk/8.6.13_4/lib' --tk-library-dir='/usr/local/Cellar/tcl-tk/8.6.13_4/lib' compile_test.py

```

--onefile --disable-consoleもあとで入れる。



## safetensorがインポートできない

FATAL: Error, failed to find path /Users/runner/work/safetensors/safetensors/bindings/python/target/release/deps/libsafetensors_rust.dylib (resolved DLL to /Users/runner/work/safetensors/safetensors/bindings/python/target/release/deps/libsafetensors_rust.dylib) for /usr/local/lib/python3.10/site-packages/safetensors/_safetensors_rust.cpython-310-darwin.so from 'safetensors', please report the bug.

# cx_freeze

pip install cx_Freeze

python setup_free.py bdist_mac --iconfile='icon.icns'

python setup_pro.py bdist_mac --iconfile='icon.icns'

