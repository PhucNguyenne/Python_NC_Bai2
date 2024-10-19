import tkinter as tk
from view import LoginView, StudentManagementApp

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý sinh viên")

        # Khởi tạo trang đăng nhập
        self.login_view = LoginView(self.root, self.show_student_management)

    def show_student_management(self):
        # Xóa giao diện hiện tại và hiển thị trang quản lý sinh viên
        self.clear_widgets()  # Gọi hàm để xóa widget cũ
        # Khởi tạo trang quản lý sinh viên
        self.student_management_app = StudentManagementApp(self.root, self.logout)

    def show_login_view(self):
        # Xóa giao diện hiện tại và hiển thị trang đăng nhập
        self.clear_widgets()  # Gọi hàm để xóa widget cũ
        self.login_view = LoginView(self.root, self.show_student_management)

    def logout(self):
        # Thực hiện các thao tác khi người dùng đăng xuất
        print("Người dùng đã đăng xuất")
        self.show_login_view()  # Quay về trang đăng nhập

    def clear_widgets(self):
        # Hàm để xóa tất cả các widget trên giao diện hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
