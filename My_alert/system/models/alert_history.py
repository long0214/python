from . import db

class alert_history(db.Model):
    __tablename__ = "alert_history"
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String(256), index=True)
    alert_message = db.Column(db.String(4096))

    def to_json(self):
        return {
            'alert_id': self.alert_id,
            'alert_message': self.alert_message
        }
