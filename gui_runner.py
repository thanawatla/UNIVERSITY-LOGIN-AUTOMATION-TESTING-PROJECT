import customtkinter as ctk
import subprocess
from tkinter import messagebox
import os

# ตั้งค่าเริ่มต้น
ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")  

root = ctk.CTk()
root.title("🚀 RMUTK Test Automation Tool")
root.geometry("450x350")
root.resizable(False, False)

# Header
header = ctk.CTkLabel(root, text="🧪 Automated Testing System", 
                      font=ctk.CTkFont("Helvetica", 20, "bold"))
header.pack(pady=(30, 5))

subheader = ctk.CTkLabel(root, text="QA Automation • RMUTK", 
                         font=ctk.CTkFont("Helvetica", 12))
subheader.pack(pady=(0, 20))

# ฟังก์ชันรัน Test
def run_tests():
    try:
        result = subprocess.run(['python', '-m', 'pytest', 'test_login_logout.py'], capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Test Result", "✅ Tests Passed!\n\nดูผลลัพธ์ใน Excel หรือโฟลเดอร์ screenshots/")
        else:
            messagebox.showwarning("Test Result", f"⚠️ Some tests failed!\n\n{result.stdout[-500:]}")
    except Exception as e:
        messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")

# ฟังก์ชันติดตั้งไลบรารี
def install_dependencies():
    try:
        libs = ['playwright', 'pytest', 'openpyxl', 'pillow']
        subprocess.check_call(['pip', 'install'] + libs)
        messagebox.showinfo("ติดตั้งสำเร็จ", "✅ ติดตั้งไลบรารีทั้งหมดเรียบร้อยแล้ว!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"❌ ติดตั้งไม่สำเร็จ: {e}")

# ฟังก์ชันเปิดไฟล์ Excel
def open_excel():
    try:
        excel_file = "test_cases.xlsx"
        if os.path.exists(excel_file):
            if os.name == 'nt':  # Windows
                os.startfile(excel_file)
            elif os.name == 'posix':  # macOS/Linux
                subprocess.call(['open', excel_file])  # macOS
                # หรือ subprocess.call(['xdg-open', excel_file]) สำหรับ Linux
        else:
            messagebox.showerror("Error", "❌ ไม่พบไฟล์ Excel ที่ระบุ")
    except Exception as e:
        messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")

# ปุ่ม
btn_run = ctk.CTkButton(root, text="🚀 Run Test Script", 
                        command=run_tests, 
                        width=200, height=45, corner_radius=15, 
                        fg_color="#3498db", hover_color="#2980b9")
btn_run.pack(pady=(10, 10))

btn_install = ctk.CTkButton(root, text="📦 Install Libraries", 
                            command=install_dependencies, 
                            width=200, height=45, corner_radius=15, 
                            fg_color="#2ecc71", hover_color="#27ae60")
btn_install.pack(pady=(0, 20))

# ปุ่มเปิดไฟล์ Excel
btn_open_excel = ctk.CTkButton(root, text="📂 Open Excel File", 
                               command=open_excel, 
                               width=200, height=45, corner_radius=15, 
                               fg_color="#f39c12", hover_color="#e67e22")
btn_open_excel.pack(pady=(0, 20))

# Footer
footer = ctk.CTkLabel(root, text="© 2025 RMUTK Automation", 
                      font=ctk.CTkFont("Helvetica", 9))
footer.pack(pady=10)

root.mainloop()