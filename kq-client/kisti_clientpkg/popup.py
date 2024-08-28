from submit_file import submit_file
from job_mgmt import run_kriss_emul
from rabbitmq_utils import rabbitmq_check_cpu_iter, rabbitmq_check_qpu_iter, rabbitmq_update_cpu_iter
from download_file import download_file
import time, threading
import tkinter as tk
from PIL import Image, ImageTk

def show_popup(root, message, x, y, color, font_size=30):
    popup = tk.Toplevel(root)
    popup.title("Notification")
    popup.geometry(f"300x200+{x}+{y}")
    popup.configure(bg=color)

    label = tk.Label(popup, text=message, pady=60, bg=color, font=("Helvetica", font_size, "bold"))
    label.pack()
    popup.after(3000, popup.destroy)
    
    
def show_image_popup(root, image_path, x, y, width=300, height=150, delay=3000):
    try:
        popup = tk.Toplevel(root)
        popup.title("Image Viewer")
        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.configure(bg='white')

        image = Image.open(image_path)
        image = image.resize((width, height), Image.Resampling.LANCZOS)  # Updated attribute
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(popup, image=photo, bg='white')
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

        popup.after(delay, popup.destroy)
    except Exception as e:
        show_popup(root, f"Error: {str(e)}", x, y, 'red')

def gui_target(root):
    try:
        download_file4 = './kq-client/storage/mywork/cost_function_plot.jpg'
        print(f"Attempting to show image popup for: {download_file4}")
        root.after(0, show_image_popup, root, download_file4, 1200, 800)
        time.sleep(5)  # Simulate some processing delay
    except Exception as e:
        print(f"Error in gui_target: {str(e)}")

def check_thread(root, main_thread):
    if not main_thread.is_alive():
        root.quit()
    else:
        root.after(100, check_thread, root, main_thread)

def gui_setup(target_function):
    root = tk.Tk()
    root.withdraw()

    main_thread = threading.Thread(target=target_function, args=(root,))
    main_thread.start()

    root.after(100, check_thread, root, main_thread)
    root.mainloop()
    
