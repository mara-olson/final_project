"""Models for training & period cycles app."""

from flask_sqlalchemy import SQLAlchemy;

db = SQLAlchemy()

class User(db.Model):
    """A user."""
    
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    team_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime)
    deactivated_at = db.Column(db.DateTime)
    notifications = db.Column(db.Boolean)

    #Relationships with strava_users, activity_logs, mense_logs, & sleep_logs tables
    strava_user = db.relationship("StravaUser", back_populates="user")
    activity_log = db.relationship("ActivityLog", back_populates="user")
    mense_log = db.relationship("MenseLog", back_populates="user")
    sleep_log = db.relationship("SleepLog", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}'

    @classmethod
    def create_user(cls, first_name, last_name, team_name, email, password, created_at):
       """Create and return a new user."""
       user = cls(email=email, password=password, first_name=first_name, last_name=last_name, team_name=team_name, created_at=created_at)
       db.session.add(user)
       db.session.commit()

       return user

    @classmethod
    def get_user_by_id(cls, user_id):
        """Get & return a user by user_id."""
        return cls.query.get(user_id)

    @classmethod
    def get_user_by_email(cls, email):
        """Get & return a user by email."""
        return cls.query.filter(User.email == email).first()


class StravaUser(db.Model):
    """A user connected to their Strava account."""
    
    __tablename__ = "strava_users"

    strava_user_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    
    strava_email = db.Column(db.String, nullable=False)
    team_name = db.Column(db.String)
    
    created_at = db.Column(db.DateTime)
    deactivated_at = db.Column(db.DateTime)

    #Relationships with users & strava_activities tables
    user = db.relationship("User", back_populates="strava_user")
    strava_activity = db.relationship("StravaActivity", back_populates="strava_user")


    def __repr__(self):
        return f'<StravaUser strava_user_id={self.user_id} user_id={self.user_id}'




class StravaActivity(db.Model):
    """An activity imported from Strava.
    
    From API /activities/{id}."""
    
    __tablename__ = "strava_activities"

    strava_activity_id = db.Column(db.Integer, primary_key=True) #id
    strava_user_id = db.Column(db.Integer, db.ForeignKey("strava_users.strava_user_id"), nullable=False) #athlete.id
    activity_name = db.Column(db.String) #name
    activity_type = db.Column(db.String) #type
    activity_date = db.Column(db.DateTime, nullable=False) #start_date
    distance = db.Column(db.Integer) #distance
    duration = db.Column(db.Integer) #elapsed_time or moving_time in minutes
    workout_type = db.Column(db.String) #workout_type (integer from Strava, will need to convert)
    suffer_score = db.Column(db.Integer) #suffer_score (total of 9 increments, I'm assuming 1-10)
    description = db.Column(db.Text) #description

    #Relationship with strava_users table
    strava_user = db.relationship("StravaUser", back_populates="strava_activity")
    

    def __repr__(self):
        return f'<StravaActivity strava_activity_id={self.strava_activity_id} title={self.activity_name}'


class ActivityLog(db.Model):
    """An activity manually added by the user."""
    
    __tablename__ = "activity_logs"

    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False) 
    activity_name = db.Column(db.String, default="Activity") 
    activity_type = db.Column(db.String, default="Run") 
    activity_date = db.Column(db.DateTime, nullable=False) 
    distance = db.Column(db.Integer) 
    duration = db.Column(db.Integer) 
    workout_type = db.Column(db.String) 
    suffer_score = db.Column(db.Integer) 
    activity_notes = db.Column(db.Text) 
    created_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)

    #Relationship with users table
    user = db.relationship("User", back_populates="activity_log")

    def __repr__(self):
        return f'<Activity activity_id={self.activity_id} title={self.activity_name}'

    def to_dict(self):
        return {
                'activity_date': self.activity_date,
                'activity_type': self.activity_type,
                'activity_id': self.activity_id,
                'activity_name': self.activity_name,
                'duration': self.duration,
                'distance': self.distance,
                'suffer_score': self.suffer_score,
                'activity_notes': self.activity_notes,
                'created_at': self.created_at,
                'deleted_at': self.deleted_at
                }
    
    @classmethod
    def create_activity(cls, activity_date, activity_type, activity_name, duration, distance, suffer_score, activity_notes, created_at):
       """Create and return a new user."""
       activity = cls(activity_date=activity_date, activity_type=activity_type, activity_name=activity_name, duration=duration, distance=distance, suffer_score=suffer_score, activity_notes=activity_notes, created_at=created_at)
       db.session.add(activity)
       db.session.commit()

       return activity


class MenseLog(db.Model):
    """A log added by the user related to their menstrual cycle."""
    
    __tablename__ = "mense_logs"

    mense_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    
    flow_volume = db.Column(db.String) #Could be a string (light, medium, heavy) or could be an integer, based on that. For plotting on a graph maybe it makes sense to have an integer?
    
    mood = db.Column(db.Boolean, default=False)
    fatigue = db.Column(db.Boolean, default=False)
    bloating = db.Column(db.Boolean, default=False)
    cramps = db.Column(db.Boolean, default=False)

    mense_notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)

    #Relationship with users table
    user = db.relationship("User", back_populates="mense_log")

    def __repr__(self):
        return f'<Mense mense_id={self.mense_id}'
        

# I think I want to actually include sx data in the period log
class SymptomLog(db.Model):
    """A menstrual-related symptom added by the user."""
    
    __tablename__ = "sx_logs"

    sx_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    
    mood = db.Column(db.Boolean)
    fatigue = db.Column(db.Boolean)
    bloating = db.Column(db.Boolean)
    cramps = db.Column(db.Boolean)
    sx_notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Symptom strava_activity_id={self.sx_id} user={self.user_id}'


class SleepLog(db.Model):
    """A log added by the user related to their sleep."""
   
    __tablename__ = "sleep_logs"

    sleep_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    sleep_duration = db.Column(db.Integer)
    sleep_quality = db.Column(db.Integer)
    sleep_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)

    #Relationship with users table
    user = db.relationship("User", back_populates="sleep_log")

    def __repr__(self):
        return f'<SleepLog sleep_log_id={self.sleep_log_id} user={self.user_id}'


def connect_to_db(flask_app, db_uri="postgresql:///period",echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)