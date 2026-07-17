import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    admission_no = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    roll_no = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    year = db.Column(
        db.Integer,
        nullable=False
    )

    section = db.Column(
        db.String(10),
        nullable=False
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=True
    )

    gender = db.Column(
       db.String(10),
       nullable=True
    )

    blood_group = db.Column(
        db.String(5),
        nullable=True
    )

    guardian_name = db.Column(
        db.String(100),
        nullable=True
    )

    guardian_phone = db.Column(
        db.String(15),
        nullable=True
    )

    address = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )