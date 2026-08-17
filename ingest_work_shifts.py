from datetime import datetime
import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import WorkShift, Base, get_engine

engine = get_engine()
Base.metadata.create_all(engine)

df = pd.read_csv("data/data.csv", skipinitialspace=True)

Session = sessionmaker(bind=engine)
session = Session()

for _, row in df.iterrows():
    shift_obj = WorkShift(
        day = datetime.strptime(row["Date"], "%m/%d/%Y").date(),
        hours_worked = row["Hours Worked"],
        tip_amount = row["Amount"],
        hourly_wage = row["Hourly Wage"],
    )
    session.merge(shift_obj)

session.commit()

print(session.query(WorkShift).count())
print(session.query(WorkShift).order_by(WorkShift.day).limit(5).all())