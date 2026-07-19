import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class Teacher(db.Model):
    __tablename__ = "teachers"

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

    employee_id = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    designation = db.Column(
        db.String(100),
        nullable=False
    )

    qualification = db.Column(
        db.String(150),
        nullable=True
    )

    experience = db.Column(
        db.Integer,
        nullable=True
    )

    date_of_joining = db.Column(
        db.Date,
        nullable=True
    )

    salary = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    address = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    user = db.relationship(
        "User",
        backref=db.backref("teacher", uselist=False)
    )