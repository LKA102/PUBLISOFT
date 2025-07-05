from sqlalchemy.sql import text

class AdminView:

    def __init__(self, session):
        self.session = session

    def get_all_admins(self):
        query = text("""
        Select 
            "A".id "admin_id",
            "A".name "admin_name",
            "A".profile_image_path "profile_image_path",
            "A".faculty "faculty",
            "U".email "email"
        From custom_users."Administrators" "A"
        INNER JOIN custom_auth."Users" "U" ON "A".id = "U".id
        """)
        result = self.session.execute(query).fetchall()
        admins = []
        for row in result:
            row_dict = dict(row._mapping)
            for key, value in row_dict.items():
                if type(value).__name__ == "UUID":
                    row_dict[key] = str(value)
            admins.append(row_dict)
        return admins

    def get_admin_by_id(self, user_id):
        query = text("""
        Select 
            "A".id "admin_id",
            "A".name "admin_name",
            "A".profile_image_path "profile_image_path",
            "A".faculty "faculty",
            "U".email "email"
        From custom_users."Administrators" "A"
        INNER JOIN custom_auth."Users" "U" ON "A".id = "U".id
        where "A".id = :id
        """)
        result = self.session.execute(query, {"id": user_id}).fetchall()
        if not result:
            return None
        row_dict = dict(result[0]._mapping)
        for key, value in row_dict.items():
            if type(value).__name__ == "UUID":
                row_dict[key] = str(value)
        return row_dict
