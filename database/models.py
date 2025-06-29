from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TermData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    residency_group_descr = db.Column(db.String(100))
    academic_year = db.Column(db.Integer)
    term = db.Column(db.Integer)
    term_descr = db.Column(db.String(100))
    academic_career_descr = db.Column(db.String(100))
    acad_prog = db.Column(db.Integer)
    academic_program_descr = db.Column(db.String(100))
    course_id = db.Column(db.Integer)
    offer_number = db.Column(db.Integer)
    faculty = db.Column(db.String(100))
    faculty_descr = db.Column(db.String(100))
    school = db.Column(db.String(100))
    school_name = db.Column(db.String(100))
    course_name = db.Column(db.String(100))
    course_code = db.Column(db.String(100))
    catalog_number = db.Column(db.Integer)
    crse_attr = db.Column(db.String(100))
    masked_id = db.Column(db.String(100))
    # 根据实际Excel结构添加字段