from app import db
from app.constant import __maxsize__

class ApplicationProfile(db.Model):
    __tablename__ = "application_profile"

    application_profile_id = db.Column(db.Integer, primary_key=True)
    application_profile_logo_name = db.Column(db.String(256), unique=True, nullable=True)
    application_profile_logo_data = db.Column(db.LargeBinary(__maxsize__), nullable=True)
    application_profile_name = db.Column(db.String(128), nullable=False)
    application_profile_meta_title = db.Column(db.String(128), nullable=True)
    application_profile_meta_description = db.Column(db.Text(), nullable=True)
    application_profile_meta_keywords = db.Column(db.JSON(), nullable=True)

    def __repr__(self):
        return "<App Profile {}>".format(self.application_profile_meta_title)

    def create(self):
        """
        Create data from self and commit.
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Update data from self.
        """
        db.session.commit()

    @staticmethod
    def get_image(param):
        """
        Get only image by @param
        @param is filename of image
        """
        return ApplicationProfile.query.filter_by(application_profile_logo_name=param).first_or_404()

    @staticmethod
    def get():
        """
        Get only single data (first)
        """
        return ApplicationProfile.query.first()


