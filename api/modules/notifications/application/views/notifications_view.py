
class NotificationsView:

    def __init__(self, session):
        self.session = session

    # Métodos para las notificaciones
    def get_all_notifications(self):
        query ="""
        Select * from custom_notifications.notifications  
        """

        result = self.session.execute(query)
        return result.fetchall()

    def get_user_notifications(self, user_id):
        query = """
        Select * from custom_notifications.notifications
        where user_id = ?
        """
        result = self.session.execute(query, (user_id,))
        return result.fetchall()

    def get_unread_notifications(self, user_id):
        pass

    def get_read_notifications(self, user_id):
        pass