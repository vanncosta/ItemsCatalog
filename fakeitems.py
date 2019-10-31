from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import database_exists, drop_database, create_database

from database_setup import Category, CategoryItem, User, Base

engine = create_engine('sqlite:///itemcatalog.db')

# Clear database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
user1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='''https://supermariorun.com/assets/img/hero/
             hero_chara_mario_update_pc.png''')
session.add(user1)
session.commit()

# Items for Data Analysis
category1 = Category(name="Data Analysis", user_id=1)

session.add(category1)
session.commit()

item1 = CategoryItem(name="Data Visualization", user_id=1,
                     description="Combine data, visuals, and narrative to tell"
                     " impactful stories and make data-driven decisions.",
                     category=category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name="Data Engineering", user_id=1,
                     description="Data Engineering is the foundation for the "
                     "new world of Big Data. Enroll now to build "
                     "production-ready data infrastructure, an essential skill"
                     " for advancing your data career.",
                     category=category1)

session.add(item2)
session.commit()

item3 = CategoryItem(name="Data Scientist", user_id=1,
                     description="Gain real-world data science experience with"
                     "projects designed by industry experts. Build your "
                     "portfolio and advance your data science career.",
                     category=category1)

session.add(item3)
session.commit()

# Items for Business
category2 = Category(name="Business", user_id=1)

session.add(category2)
session.commit()

item1 = CategoryItem(name="Marketing Analytics", user_id=1,
                     description="Gain foundational data skills applicable to "
                     "marketing. Collect and analyze data, model marketing "
                     "scenarios, and communicate your findings with Excel, "
                     "Tableau, Google Analytics, and Data Studio.",
                     category=category2)

session.add(item1)
session.commit()

item2 = CategoryItem(name="AI Product Manager", user_id=1,
                     description="Learn to develop AI products that deliver "
                     "business value. Build skills that help you compete in "
                     "the new AI-powered world.",
                     category=category2)

session.add(item2)
session.commit()

item3 = CategoryItem(name="Digital Marketer", user_id=1,
                     description="Gain real-world experience running live "
                     "campaigns as you learn from top experts in the field. "
                     "Launch your career with a 360-degree understanding of "
                     "digital marketing.",
                     category=category2)

session.add(item3)
session.commit()

# Items for Web Development
category3 = Category(name="Web Development", user_id=1)

session.add(category3)
session.commit()

item1 = CategoryItem(name="Java Developer", user_id=1,
                     description="Learn enterprise scale backend-development "
                     "with Java, and be prepared for the software engineering "
                     "jobs that are in demand at a majority of Fortune 500 "
                     "companies like Google, Amazon, Netflix, and more.",
                     category=category3)

session.add(item1)
session.commit()

item2 = CategoryItem(name="React", user_id=1,
                     description="React is completely transforming Front-End "
                     "Development. Master this powerful UI library from "
                     "Facebook with Udacity.",
                     category=category3)

session.add(item2)
session.commit()

item3 = CategoryItem(name="Full Stack Web Developer", user_id=1,
                     description="In this program, you will prepare for a job "
                     "as a Full Stack Web Developer, and learn to create "
                     "complex server side web applications that use powerful "
                     "relational databases to persistently store data.",
                     category=category3)

session.add(item3)
session.commit()

# Items for Brass
category4 = Category(name="Mobile App Development", user_id=1)

session.add(category4)
session.commit()


categories = session.query(Category).all()
for category in categories:
    print "Category: " + category.name
