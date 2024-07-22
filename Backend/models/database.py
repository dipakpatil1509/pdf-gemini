from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.env_vars import get_env_var
from contextlib import contextmanager

USERNAME = get_env_var("DB_USERNAME")
PASSWORD = get_env_var("DB_PASSWORD")
SERVER = get_env_var("DB_SERVER")
DBNAME = get_env_var("DB_NAME")
class Database:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{SERVER}/{DBNAME}"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_db()
        return cls._instance

    def init_db(self):
        '''
            We have also specified a parameter create_engine.echo, which will instruct the Engine to log all of the SQL it emits
            to a Python logger that will write to standard out. This flag is a shorthand way of setting up Python logging
            more formally and is useful for experimentation in scripts. Many of the SQL examples will include this SQL
            logging output beneath a [SQL] link that when clicked, will reveal the full SQL interaction.
        '''
        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL, echo=False, )
        self.Base = declarative_base()

    @contextmanager
    def get_session(self):
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        yield session
        session.close()

    def get_base(self):
        return self.Base

db = Database()
SessionLocal = db.get_session()
Base = db.get_base()