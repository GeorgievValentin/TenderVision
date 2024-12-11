from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_CONFIG

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@" \
               f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind = engine)
Base = declarative_base()


class Tender(Base):
    __tablename__ = "tenders"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    organization = Column(String, nullable = False)
    unique_id = Column(String, unique = True, nullable = False)
    award_method = Column(String)
    deadline = Column(Date)
    publish_date = Column(Date)
    details_link = Column(String)


def init_db():
    Base.metadata.create_all(bind = engine)


def save_tenders(tenders):
    session = SessionLocal()
    print(f"Saving {len(tenders)} tenders to the database...")

    for tender in tenders:
        try:
            print(f"Saving tender: {tender['unique_id']}")
            db_tender = Tender(**tender)
            session.merge(db_tender)  # Merge to handle existing records
        except Exception as e:
            print(f"Error saving tender {tender['unique_id']}: {e}")
            session.rollback()  # Rollback to recover session state

    try:
        session.commit()
        print("Tenders have been successfully saved to the database!")
    except Exception as e:
        print(f"Error committing to the database: {e}")
        session.rollback()
    finally:
        session.close()
