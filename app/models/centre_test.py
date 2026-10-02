from sqlalchemy import Column, Integer, ForeignKey, Numeric

from app.db.database import Base


class CentreTest(Base):
    __tablename__ = "centre_tests"

    centre_id = Column(
        Integer,
        ForeignKey("diagnostic_centres.id", ondelete="CASCADE"),
        primary_key=True
    )

    test_id = Column(
        Integer,
        ForeignKey("diagnostic_tests.id", ondelete="CASCADE"),
        primary_key=True
    )

    price = Column(Numeric(10, 2), nullable=False)