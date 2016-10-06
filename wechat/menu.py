from base import Base

class Menu(Base):
    """
    Wechat Menu Class
    sync menu to wechat
    """
    def sync_menu(self, menu):
        """Post menu to service"""
        token = self.get_token()
        url = self.get_url('menu/create', {'access_token':token})
        result = self.get_data(url, menu)
        return result
