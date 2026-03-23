
import pystray
from PIL import Image, ImageDraw
import subprocess
import threading

# --- 電源設定のロジック ---
def set_lid_action(value):
    subprocess.run(f"powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION {value}", shell=True)
    subprocess.run(f"powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION {value}", shell=True)
    subprocess.run("powercfg /setactive SCHEME_CURRENT", shell=True)

# --- アイコン作成 (簡易的な正方形) ---
def create_image(color):
    # 64x64のアイコンを作成
    image = Image.new('RGB', (64, 64), color)
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill="white")
    return image

state = False # 現在の状態 (False: 通常, True: スリープ防止中)

def on_clicked(icon, item):
    global state
    state = not item.checked
    
    if state:
        set_lid_action(0) # 何もしない
        icon.icon = create_image("red") # 防止中は赤色に
        print("スリープ防止: ON")
    else:
        set_lid_action(1) # スリープに戻す (元の値を保存して戻すのが理想)
        icon.icon = create_image("blue") # 通常時は青色に
        print("スリープ防止: OFF")

def on_quit(icon, item):
    set_lid_action(1) # 終了時はスリープ設定に戻す
    icon.stop()

# --- メイン処理 ---
icon = pystray.Icon("SleepPreventer")
icon.menu = pystray.Menu(
    pystray.MenuItem("スリープ防止モード", on_clicked, checked=lambda item: state),
    pystray.MenuItem("終了", on_quit)
)
icon.icon = create_image("blue")

print("タスクトレイで起動しました。")
icon.run()