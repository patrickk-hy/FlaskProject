from .models import db, TermData
import pandas as pd

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def save_excel_data(data_frame):
    # df = pd.read_csv(data_frame)
    # required_cols = {
    #     'RESIDENCY_GROUP_DESCR', 'ACADEMIC_YEAR', 'TERM', 'TERM_DESCR',
    #     'ACADEMIC_CAREER_DESCR', 'ACAD_PROG', 'ACADEMIC_PROGRAM_DESCR',
    #     'COURSE_ID', 'OFFER_NUMBER', 'FACULTY', 'FACULTY_DESCR',
    #     'SCHOOL', 'SCHOOL_NAME', 'COURSE_NAME', 'COURSE_CODE',
    #     'CATALOG_NUMBER', 'CRSE_ATTR', 'MASKED_ID'
    # }

    records = []
    print('----------------')
    for _, row in data_frame.iterrows():
        record = TermData(
            residency_group_descr=row['RESIDENCY_GROUP_DESCR'],
            academic_year=row['ACADEMIC_YEAR'],
            term=row['TERM'],
            term_descr=row['TERM_DESCR'],
            academic_career_descr=row['ACADEMIC_CAREER_DESCR'],
            acad_prog=row['ACAD_PROG'],
            academic_program_descr=row['ACADEMIC_PROGRAM_DESCR'],
            course_id=row['COURSE_ID'],
            offer_number=row['OFFER_NUMBER'],
            faculty=row['FACULTY'],
            faculty_descr=row['FACULTY_DESCR'],
            school=row['SCHOOL'],
            school_name=row['SCHOOL_NAME'],
            course_name=row['COURSE_NAME'],
            course_code=row['COURSE_CODE'],
            catalog_number=row['CATALOG_NUMBER'],
            crse_attr=row['CRSE_ATTR'],
            masked_id=row['MASKED_ID']
        )
        records.append(record)

    db.session.bulk_save_objects(records)
    db.session.commit()



def aggregate_data():
    # 示例聚合：按column1分组求平均值
    result = db.session.query(
        ExcelData.column1,
        db.func.avg(ExcelData.column2).label('average')
    ).group_by(ExcelData.column1).all()

    return [{"column1": r.column1, "average": float(r.average)} for r in result]