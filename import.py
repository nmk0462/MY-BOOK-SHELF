import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

os.environ["DATABASE_URL"]="postgres://edahmhhqenhspe:56d4fa2dca5be2e6a56d4cb28dddbac650b5e7dce81088f4c8b114375dc7c768@ec2-18-210-214-86.compute-1.amazonaws.com:5432/dk2rsjrgsaraf"
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    h=1
    f= open("books.csv")
    freader = csv.reader(f)
    for isbn,title,author,year in freader:
        db.execute("INSERT INTO books (isbn, title, author,year) VALUES (:isbn, :title, :author, :year)",{"isbn":isbn,"title":title,"author":author,"year":year})
        print(h)
        h+1
    db.commit()

if __name__ == "__main__" :
    main()