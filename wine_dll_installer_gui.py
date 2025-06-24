
import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import time
import shutil
import re

def run_protontricks_command(app_id, dll, update_callback):
    cmd = f"{PROTONTRICKS_CMD} {app_id} --force -q {dll}"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        for line in process.stdout:
            update_callback(line)
        process.wait(timeout=300)
        return "執行完成\n"
    except subprocess.TimeoutExpired:
        return f"安裝 {dll} 超時，可能需要手動檢查。\n"
    except Exception as e:
        return f"執行發生錯誤：{str(e)}\n"

def update_text(text):
    result_text.insert(tk.END, text)
    result_text.see(tk.END)
    result_text.update()

def update_timer_and_status():
    global current_dll
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    status_text = f"正在安裝: {current_dll}" if installing else "等待開始"
    status_timer_label.config(text=f"{status_text} | 已用時間: {minutes:02d}:{seconds:02d}")
    if installing:
        root.after(1000, update_timer_and_status)

def countdown_and_close():
    global countdown, total_time
    if countdown > 0:
        minutes, seconds = divmod(int(total_time), 60)
        status_timer_label.config(text=f"程式會在{countdown}秒後關閉 | 已用時間: {minutes:02d}:{seconds:02d}")
        countdown -= 1
        root.after(1000, countdown_and_close)
    else:
        root.destroy()

def install_dlls_thread():
    global installing, start_time, countdown, current_dll, total_time
    app_id = app_id_entry.get()
    if not app_id.isdigit():
        update_text("錯誤：Steam App ID 必須是一個數字。\n")
        install_button.config(state=tk.NORMAL, text="安裝 DLL")
        installing = False
        return

    result_text.delete(1.0, tk.END)
    update_text(f"開始為 Steam App ID {app_id} 安裝 DLL...\n")

    selected = option_var.get()
    if selected == 1:
        dlls = ["wmp11", "directshow"]
    elif selected == 2:
        dlls = ["wmp9", "directshow"]
    elif selected == 3:
        dlls = ["lavfilters", "quartz"]
    else:
        dlls = [dll for dll, var in custom_vars.items() if var.get()]
        if not dlls:
            update_text("錯誤：自訂模式下請至少勾選一項 DLL。\n")
            install_button.config(state=tk.NORMAL, text="安裝 DLL")
            installing = False
            return

    for dll in dlls:
        current_dll = dll
        update_text(f"正在安裝 {dll}...\n")
        output = run_protontricks_command(app_id, dll, update_text)
        update_text(output)

    update_text("安裝過程完成\n")
    install_button.config(state=tk.NORMAL, text="安裝 DLL")
    installing = False
    total_time = time.time() - start_time
    countdown = 5
    countdown_and_close()

def install_dlls():
    global installing, start_time
    install_button.config(state=tk.DISABLED, text="安裝中")
    installing = True
    start_time = time.time()
    update_timer_and_status()
    threading.Thread(target=install_dlls_thread, daemon=True).start()

def on_app_selected(event):
    index = app_listbox.curselection()
    if not index:
        return
    appid = apps[index[0]][0]
    app_id_entry.delete(0, tk.END)
    app_id_entry.insert(0, appid)

def load_apps():
    global apps
    try:
        cmd = f"{PROTONTRICKS_CMD} --list"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        apps = []
        for line in result.stdout.split('\n'):
            match = re.match(r"(.*) \((\d+)\)$", line.strip())
            if match:
                app_name, app_id = match.groups()
                apps.append((app_id, app_name))

        for app_id, app_name in apps:
            app_listbox.insert(tk.END, f"{app_name} ({app_id})")
    except Exception as e:
        messagebox.showerror("錯誤", f"載入 App 清單失敗：{str(e)}")

# 主視窗
root = tk.Tk()
root.title("Wine DLL 安裝器")
root.geometry("1000x600")

# 確認 protontricks 可用
if shutil.which("protontricks"):
    PROTONTRICKS_CMD = "protontricks"
elif shutil.which("flatpak"):
    result = subprocess.run(["flatpak", "list", "--app"], capture_output=True, text=True)
    if "com.github.Matoking.protontricks" in result.stdout:
        PROTONTRICKS_CMD = "flatpak run com.github.Matoking.protontricks"
    else:
        messagebox.showerror("錯誤", "未找到 protontricks，請先安裝。")
        exit(1)
else:
    messagebox.showerror("錯誤", "未找到 protontricks，請先安裝。")
    exit(1)

# 左右主要容器
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# App ID 輸入框 + 安裝按鈕
entry_frame = tk.Frame(left_frame)
entry_frame.pack(fill=tk.X, pady=(0, 5))
tk.Label(entry_frame, text="Steam App ID:").pack(side=tk.LEFT)
app_id_entry = tk.Entry(entry_frame, width=20)
app_id_entry.pack(side=tk.LEFT, padx=5)
install_button = tk.Button(entry_frame, text="安裝 DLL", command=install_dlls)
install_button.pack(side=tk.LEFT)

# 四選一安裝選項
option_var = tk.IntVar(value=1)
tk.Label(left_frame, text="請選擇安裝模式：", font=("Arial", 10, "bold")).pack(anchor="w")
tk.Radiobutton(left_frame, text="Wmp11 + DirectShow（萬用解）", variable=option_var, value=1).pack(anchor="w")
tk.Radiobutton(left_frame, text="Wmp9 + DirectShow（其次方案）", variable=option_var, value=2).pack(anchor="w")
tk.Radiobutton(left_frame, text="Lavfilters + Quartz（最快）", variable=option_var, value=3).pack(anchor="w")
tk.Radiobutton(left_frame, text="自訂 DLL", variable=option_var, value=4).pack(anchor="w")

# 自定義 DLL 勾選區（用 LabelFrame 包起來）
custom_frame = tk.LabelFrame(left_frame, text="自訂 DLL 選項（至少選一）")
custom_frame.pack(pady=5, fill=tk.X)
custom_vars = {}
custom_options = ["wmp11", "wmp9", "directshow", "lavfilters", "quartz", "mf", "xact"]
for opt in custom_options:
    var = tk.BooleanVar()
    cb = tk.Checkbutton(custom_frame, text=opt, variable=var)
    cb.pack(anchor="w")
    custom_vars[opt] = var

# App 清單列表區（帶 scrollbar）
app_listbox_frame = tk.Frame(left_frame)
app_listbox_frame.pack(fill=tk.BOTH, expand=True, pady=10)
tk.Label(app_listbox_frame, text="可用遊戲 App：").pack(anchor="w")
scrollbar = tk.Scrollbar(app_listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
app_listbox = tk.Listbox(app_listbox_frame, height=10, yscrollcommand=scrollbar.set)
app_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=app_listbox.yview)
app_listbox.bind("<<ListboxSelect>>", on_app_selected)

# 結果輸出區
status_timer_label = tk.Label(right_frame, text="等待開始 | 已用時間: 00:00")
status_timer_label.pack()
tk.Label(right_frame, text="注意：遊戲至少需要啟動過一次。", fg="red").pack(pady=5)
result_text = scrolledtext.ScrolledText(right_frame, height=30, width=80)
result_text.pack(fill=tk.BOTH, expand=True)

# 初始化
apps = []
installing = False
start_time = 0
countdown = 5
current_dll = ""
total_time = 0

load_apps()
root.mainloop()
