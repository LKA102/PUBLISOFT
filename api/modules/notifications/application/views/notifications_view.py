from sqlalchemy.sql import text
class NotificationsView:

    def __init__(self, session):
        self.session = session

    # Métodos para las notificaciones
    def get_all_notifications(self):
        query = text("""
        SELECT 
            n.id,
            n.title,
            n.message,
            n.type,
            n.leido,
            n.fecha_creacion,
            -- IDs
            n.user_emisor_id AS emisor_id,
            n.user_receptor_id AS receptor_id,
            -- Datos del emisor
            emisor.name AS emisor_name,
            emisor.last_name AS emisor_last_name,
            -- Datos del receptor
            receptor.name AS receptor_name,
            receptor.last_name AS receptor_last_name
            FROM custom_notification.notificaciones n
            LEFT JOIN custom_users."Students" emisor ON n.user_emisor_id = emisor.id
            LEFT JOIN custom_users."Students" receptor ON n.user_receptor_id = receptor.id
            ORDER BY n.fecha_creacion DESC;
        """)
        result = self.session.execute(query).fetchall()
        notifications = []
        for row in result:
            row_dict = dict(row._mapping)
            for key, value in row_dict.items():
                if type(value).__name__ == "UUID":
                    row_dict[key] = str(value)
            notification = {
                "id": row_dict["id"],
                "title": row_dict["title"],
                "message": row_dict["message"],
                "type": row_dict["type"],
                "fecha_creacion": row_dict["fecha_creacion"].replace(microsecond=0).isoformat(),
                "emisor": {
                    "id" : row_dict["emisor_id"],
                    "name" : row_dict["emisor_name"],
                    "last_name": row_dict["emisor_last_name"],
                },
                "receptor": {
                    "id": row_dict["receptor_id"],
                    "name": row_dict["receptor_name"],
                    "last_name": row_dict["receptor_last_name"],
                },
            }
            notifications.append(notification)
        return notifications

    # 2. Notificaciones de un usuario receptor (Yo soy el receptor)
    def get_user_notifications(self, user_id):
        query = text("""
        SELECT 
            n.id,
            n.title,
            n.message,
            n.type,
            n.leido,
            n.fecha_creacion,
            -- Datos del emisor
            emisor.name AS emisor_name,
            emisor.last_name AS emisor_last_name,
            n.user_emisor_id AS emisor_id,
            n.user_receptor_id AS receptor_id,
            -- Datos del receptor
            receptor.name AS receptor_name,
            receptor.last_name AS receptor_last_name
        FROM custom_notification.notificaciones n
        LEFT JOIN custom_users."Students" emisor ON n.user_emisor_id = emisor.id
        LEFT JOIN custom_users."Students" receptor ON n.user_receptor_id = receptor.id
        WHERE n.user_receptor_id = :user_id
        ORDER BY n.fecha_creacion DESC;
        """)
        result = self.session.execute(query, {"user_id": user_id}).fetchall()
        notifications = []
        for row in result:
            row_dict = dict(row._mapping)
            for key, value in row_dict.items():
                if type(value).__name__ == "UUID":
                    row_dict[key] = str(value)
            notification = {
                "id": row_dict["id"],
                "title": row_dict["title"],
                "message": row_dict["message"],
                "type": row_dict["type"],
                "leido": row_dict["leido"],
                "fecha_creacion": row_dict["fecha_creacion"].replace(microsecond=0).isoformat(),
                "emisor": {
                    "id" : row_dict["emisor_id"],
                    "name" : row_dict["emisor_name"],
                    "last_name": row_dict["emisor_last_name"],
                },
                "receptor": {
                    "id": row_dict["receptor_id"],
                    "name": row_dict["receptor_name"],
                    "last_name": row_dict["receptor_last_name"],
                },
            }
            notifications.append(notification)
        return notifications

    # 3. Notificaciones no leídas
    def get_unread_notifications(self, user_id):
        query = text("""
        SELECT 
            n.id,
            n.title,
            n.message,
            n.type,
            n.leido,
            n.fecha_creacion,
            -- Datos del emisor
            emisor.name AS emisor_name,
            emisor.last_name AS emisor_last_name,
            n.user_emisor_id AS emisor_id,
            n.user_receptor_id AS receptor_id,
            -- Datos del receptor
            receptor.name AS receptor_name,
            receptor.last_name AS receptor_last_name
        FROM custom_notification.notificaciones n
        LEFT JOIN custom_users."Students" emisor ON n.user_emisor_id = emisor.id
        LEFT JOIN custom_users."Students" receptor ON n.user_receptor_id = receptor.id
        WHERE n.user_receptor_id = :user_id 
        AND n.leido = false;
        """)
        result = self.session.execute(query, {"user_id": user_id}).fetchall()
        notifications = []
        for row in result:
            row_dict = dict(row._mapping)
            for key, value in row_dict.items():
                if type(value).__name__ == "UUID":
                    row_dict[key] = str(value)
            notification = {
                "id": row_dict["id"],
                "title": row_dict["title"],
                "message": row_dict["message"],
                "type": row_dict["type"],
                "fecha_creacion": row_dict["fecha_creacion"].replace(microsecond=0).isoformat(),
                "emisor": {
                    "id" : row_dict["emisor_id"],
                    "name" : row_dict["emisor_name"],
                    "last_name": row_dict["emisor_last_name"],
                },
                "receptor": {
                    "id": row_dict["receptor_id"],
                    "name": row_dict["receptor_name"],
                    "last_name": row_dict["receptor_last_name"],
                },
            }
            notifications.append(notification)
        return notifications

    # 4. Notificaciones leídas
    def get_read_notifications(self, user_id):
        query = text("""
        SELECT 
            n.id,
            n.title,
            n.message,
            n.type,
            n.leido,
            n.fecha_creacion,
            emisor.name AS emisor_name,
            emisor.last_name AS emisor_last_name,
            n.user_emisor_id AS emisor_id,
            n.user_receptor_id AS receptor_id,
            -- Datos del receptor
            receptor.name AS receptor_name,
            receptor.last_name AS receptor_last_name
        FROM custom_notification.notificaciones n
        LEFT JOIN custom_users."Students" emisor ON n.user_emisor_id = emisor.id
        LEFT JOIN custom_users."Students" receptor ON n.user_receptor_id = receptor.id
        WHERE n.user_receptor_id = :user_id
        AND n.leido = true;
        """)
        result = self.session.execute(query, {"user_id": user_id}).fetchall()
        notifications = []
        for row in result:
            row_dict = dict(row._mapping)
            for key, value in row_dict.items():
                if type(value).__name__ == "UUID":
                    row_dict[key] = str(value)
            notification = {
                "id": row_dict["id"],
                "title": row_dict["title"],
                "message": row_dict["message"],
                "type": row_dict["type"],
                "fecha_creacion": row_dict["fecha_creacion"].replace(microsecond=0).isoformat(),
                "emisor": {
                    "id" : row_dict["emisor_id"],
                    "name" : row_dict["emisor_name"],
                    "last_name": row_dict["emisor_last_name"],
                },
                "receptor": {
                    "id": row_dict["receptor_id"],
                    "name": row_dict["receptor_name"],
                    "last_name": row_dict["receptor_last_name"],
                },
            }
            notifications.append(notification)
        return notifications