from model import DbConn

class StudentController:
    def __init__(self, treeview):
        self.treeview = treeview

    def load_all_students(self):
        # Sử dụng DbConn để lấy dữ liệu sinh viên từ database
        with DbConn() as db:
            results = db.select()  # Lấy tất cả sinh viên từ bảng
            # Xóa tất cả nội dung hiện tại trong Treeview
            self.treeview.delete(*self.treeview.get_children())
            # Chèn từng dòng kết quả vào Treeview
            for row in results:
                self.treeview.insert('', 'end', values=row)

    def insert_student(self, **student_data):
        with DbConn() as db:
            success = db.insert(**student_data)
            return success

    def update_student(self, update_data, **conditions):
        with DbConn() as db:
            success = db.update(update_data, **conditions)
            return success

    def delete_student(self, **conditions):
        with DbConn() as db:
            success = db.delete(**conditions)
            return success
