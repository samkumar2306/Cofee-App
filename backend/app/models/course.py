import uuid

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    course_code = db.Column(db.String(20), unique=True, nullable=False)

    course_name = db.Column(db.String(150), nullable=False)

    department = db.Column(db.String(100), nullable=False)

    duration = db.Column(db.Integer, nullable=False)

    semester_count = db.Column(db.Integer, nullable=False)

    description = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )