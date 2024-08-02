import numpy as np
import functions as fct
from kisti_clientpkg.submit_file import submit_file
from kisti_clientpkg.job_mgmt import run_kriss_emul
from kisti_clientpkg.rabbitmq_utils import rabbitmq_check_cpu_iter, rabbitmq_check_qpu_iter, rabbitmq_update_cpu_iter
from kisti_clientpkg.download_file import download_file
import time, threading
import tkinter as tk
from tkinter import messagebox

def show_popup(root, message, x, y, color):
    popup = tk.Toplevel(root)
    popup.title("Notification")
    popup.geometry(f"300x100+{x}+{y}")
    popup.configure(bg=color)

    label = tk.Label(popup, text=message, pady=20, bg=color)
    label.pack()
    popup.after(3000, popup.destroy)

def test():
    fci_file_name = "./kq-client/FCIDUMP"
    emul_file_name = "test.py"
    download_file1 = 'noref_0_0.rdm1'
    download_file2 = 'noref_0_0.rdm2'

    sum = 0
    cpu_iter = 0
    for i in range(2):
        cpu_iter += 1
        # FCIDUMP file update?
        # 파일을 다시 전송할지? 데이터만 보낼지?
        submit_file(fci_file_name)
        noti1 = f"Sent the {fci_file_name} !!!"
        root.after(0, show_popup, root, noti1, 500, 300, 'lightblue')
        # rabbitmq_update_cpu_iter(cpu_iter)

        run_kriss_emul(emul_file_name)
        # qpu_iter = rabbitmq_check_qpu_iter()
        download_file(download_file1)
        noti2 = f"Received the {download_file1} !!!"
        root.after(0, show_popup, root, noti2, 600, 400, 'lightgreen')
        download_file(download_file2)
        noti3 = f"Received the {download_file2} !!!"
        root.after(0, show_popup, root, noti3, 700, 500, 'lightyellow')
        
        time.sleep(5)

def check_thread():
    if not main_thread.is_alive():
        root.quit()
    else:
        root.after(100, check_thread)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    main_thread = threading.Thread(target=test)
    main_thread.start()

    root.after(100, check_thread)
    root.mainloop()
