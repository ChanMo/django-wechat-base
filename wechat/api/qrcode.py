class Qrcode(Base):
    """
    Qrcode Class
    """
    def get_ticket(self, id):
        token = self.get_token()
        url = self.get_url('qrcode/create', {'access_token':token})
        data = {
            'action_name': 'QR_LIMIT_SCENE',
            'action_info': {
                'scene': {
                    'scene_id': id,
                }
            }
        }
        data = json.dumps(data)
        result = self.get_data(url, data)
        return result['ticket']
