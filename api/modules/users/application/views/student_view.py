from sqlalchemy.sql import text

class StudentView:

    def __init__(self, session):
        self.session = session

    def get_all_students(self):
        query = text("""
        Select 
            "S".id "student_id",
            "S".name "student_name",
            "S".profile_image_path "profile_image_path",
            "S".faculty "faculty",
            "U".email "email"
        From custom_users."Students" "S"
        INNER JOIN custom_auth."Users" "U" ON "S".id = "U".id
        """)
        result = self.session.execute(query).fetchall()
        students = []
        for row in result:
            row_dict = dict(row._mapping)
            for key, value in row_dict.items():
                if type(value).__name__ == "UUID":
                    row_dict[key] = str(value)
            students.append(row_dict)
        return students

    def get_student_by_id(self, user_id):
        query = text("""
        Select 
            "S".id "student_id",
            "S".name "student_name",
            "S".profile_image_path "profile_image_path",
            "S".faculty "faculty",
            "U".email "email"
        From custom_users."Students" "S"
        INNER JOIN custom_auth."Users" "U" ON "S".id = "U".id
        where "S".id = :id
        """)
        result = self.session.execute(query, {"id": user_id}).fetchall()
        if not result:
            return None
        row_dict = dict(result[0]._mapping)
        for key, value in row_dict.items():
            if type(value).__name__ == "UUID":
                row_dict[key] = str(value)
        return row_dict