from app import db
from app.constant import __maxsize__

class BusinessProfile(db.Model):
    __tablename__ = "business_profile"

    business_profile_id = db.Column(db.Integer, primary_key=True)
    business_profile_name = db.Column(db.String(124), nullable=True)
    business_profile_logo = db.Column(db.LargeBinary(__maxsize__), nullable=True)
    business_profile_logo_name = db.Column(db.String(256), nullable=True)
    business_profile_address = db.Column(db.Text(), nullable=True)
    business_profile_sub_district = db.Column(db.String(64), nullable=True)
    business_profile_district = db.Column(db.String(64), nullable=True)
    business_profile_province = db.Column(db.String(64), nullable=True)
    business_profile_country = db.Column(db.String(64), nullable=True)
    business_profile_postal_code = db.Column(db.String(12), nullable=True)
    business_profile_phone_number = db.Column(db.String(18), nullable=True)
    business_profile_email = db.Column(db.String(120), nullable=True)
    business_profile_website = db.Column(db.String(120), nullable=True)
    business_profile_social_media = db.Column(db.JSON, nullable=True)
    business_profile_created_at = db.Column(db.DateTime(), nullable=False)
    business_profile_updated_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return "<Business {}>".format(self.business_profile_name)

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
    def get():
        """
        Get only single data (first)
        """
        return BusinessProfile.query.first()

    @staticmethod
    def get_image(param):
        """
        Get images with @param is name of data
        """
        return BusinessProfile.query.filter_by(business_profile_logo_name=param).first_or_404()
