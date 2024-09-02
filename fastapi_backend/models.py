from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from fastapi_backend.database import engine

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id: Column[int] = Column(Integer, primary_key=True)
    company_name: Column[str] = Column(String)
    comments: Column[str] = Column(String)
    abbreviated_names_and_acquisitions: Column[str] = Column(String)


class Sector(Base):
    __tablename__ = "sectors"

    id = Column(Integer, primary_key=True)
    sector_name = Column(String)


class NaturalGasProductionByCompany(Base):
    __tablename__ = "natural_gas_production_by_companies"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship(
        "Company", backref="natural_gas_production_by_companies", lazy="joined"
    )
    production_volume = Column(Integer, comment="MMSCF/D")


class NaturalGasUtilizationBySector(Base):
    __tablename__ = "natural_gas_utilization_by_sectors"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    sector_id = Column(Integer, ForeignKey("sectors.id"))
    sector = relationship(
        "Sector", backref="natural_gas_utilization_by_sectors", lazy="joined"
    )
    utilization = Column(Integer, comment="MMSCF/D")


class CompetitiveBidRounds(Base):
    __tablename__ = "competitive_bid_rounds"

    id = Column(Integer, primary_key=True)
    year_ended = Column(Date)
    number_of_blocks_offered = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    number_of_bids_received = Column(Integer, nullable=True)


Base.metadata.create_all(engine)
