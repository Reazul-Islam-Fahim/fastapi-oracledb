from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Annotated, List
from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import oracledb

# Database configuration
DB_HOST = "192.168.2.48"
DB_PORT = 1521
DB_SERVICE_NAME = "ORCLPDB"
DB_USER = "test"
DB_PASSWORD = "123"

oracle_connection_string = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SERVICE_NAME}"

# Create a new SQLAlchemy engine
engine = create_engine(oracle_connection_string, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare a base class for SQLAlchemy models
Base = declarative_base()

# Define the Income model
class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    total_income = Column(Float)
    taxable_income = Column(Float)
    tax_liability = Column(Float)

# Define the IncomeInput Pydantic model
class IncomeInput(BaseModel):
    id: Annotated[int, "Enter your id: "]
    is_government: Annotated[str, "Are you a government employee? ('Y' or 'N')"]
    basic_salary: Annotated[int, "Basic salary amount"]
    house_rent_allowance: Annotated[int, "House rent allowance amount"]
    medical_allowance: Annotated[int, "Medical allowance amount"]
    festival_bonus: Annotated[int, "Festival bonus amount"]
    rent_free_accommodation: Annotated[int, "Value of rent-free accommodation"] = 0
    accommodation_at_concessional_rate: Annotated[int, "Value of accommodation at concessional rate"] = 0
    vehicle_facility_months: Annotated[int, "Number of months with vehicle facility"] = 0
    is_higher_cc: Annotated[str, "Is the vehicle higher than 2500cc? ('Y' or 'N')"] = 'N'
    other_non_cash_benefits: Annotated[Dict[str, int], "Other non-cash benefits"] = {}
    government_benefits: Annotated[Dict[str, int], "Government benefits"] = {}
    num_autistic_children: Annotated[int, "Number of autistic children"] = 0
    category: Annotated[int, "Category for exemption limit (1-4)"]

app = FastAPI()

# Dependency for getting DB session
def get_db() -> Session: # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

# Income Calculator class
class IncomeCalculator:
    def __init__(self, is_government, income_data: IncomeInput):
        self.is_government = is_government
        self.income_data = income_data
        self.income_from_job = 0

    def calc_income(self):
        if self.is_government == "N":
            vehicle_facility_provided = self._get_vehicle_facility()
            other_non_cash = self._get_other_benefits()
            self.income_from_job = (
                self.income_data.basic_salary +
                self.income_data.house_rent_allowance +
                self.income_data.medical_allowance +
                self.income_data.festival_bonus +
                self.income_data.rent_free_accommodation +
                self.income_data.accommodation_at_concessional_rate +
                vehicle_facility_provided +
                other_non_cash
            )
        else:
            self.income_from_job = (
                self.income_data.basic_salary +
                self.income_data.house_rent_allowance +
                self.income_data.medical_allowance +
                self.income_data.festival_bonus
            )
            self.income_from_job += sum(self.income_data.government_benefits.values())

        return self.income_from_job

    def _get_vehicle_facility(self):
        vehicle_facility_provided = 0
        if self.income_data.vehicle_facility_months > 0:
            vehicle_facility_provided = self.income_data.vehicle_facility_months * (25000 if self.income_data.is_higher_cc == "Y" else 10000)
        return vehicle_facility_provided

    def _get_other_benefits(self):
        other_non_cash = 0
        if self.income_data.other_non_cash_benefits:
            for value in self.income_data.other_non_cash_benefits.values():
                other_non_cash += value
        return other_non_cash

# Tax Calculator class
class TaxCalculator:
    def __init__(self, taxable_income):
        self.taxable_income = taxable_income
        self.exemption_limit = 0

    def set_exemption_limit(self, category, num_autistic_children):
        exemptions = {
            1: 350000,
            2: 400000,
            3: 475000,
            4: 500000
        }
        self.exemption_limit = exemptions.get(category, 0) + (num_autistic_children * 50000)

    def calculate_tax(self):
        taxable_income_after_exemption = max(0, self.taxable_income - self.exemption_limit)
        return self._calculate_tax_liability(taxable_income_after_exemption)

    def _calculate_tax_liability(self, taxable_income):
        tax_liability = 0
        slabs = [
            (100000, 0.05),
            (400000, 0.10),
            (500000, 0.15),
            (500000, 0.20),
            (2000000, 0.25),
            (float('inf'), 0.30)
        ]

        for limit, rate in slabs:
            if taxable_income <= 0:
                break
            taxable_amount = min(taxable_income, limit)
            tax_liability += taxable_amount * rate
            taxable_income -= taxable_amount

        return tax_liability

# Route to calculate income
@app.post("/calculate_income/")
async def calculate_income(income_input: IncomeInput, db: Session = Depends(get_db)):
    income_calculator = IncomeCalculator(income_input.is_government, income_input)
    total_income = income_calculator.calc_income()

    taxable_income = total_income - (total_income / 3 if (total_income / 3) < 450000 else 450000)

    tax_calculator = TaxCalculator(taxable_income)
    tax_calculator.set_exemption_limit(income_input.category, income_input.num_autistic_children)
    tax_liability = tax_calculator.calculate_tax()

    income_record = Income(total_income=total_income, taxable_income=taxable_income, tax_liability=tax_liability)
    db.add(income_record)
    db.commit()
    db.refresh(income_record)

    return {
        "total_income": total_income,
        "taxable_income": taxable_income,
        "tax_liability": tax_liability
    }

# Route to get all income records
@app.get("/get_income_records", response_model=List[Income])
async def get_income_records(db: Session = Depends(get_db)):
    incomes = db.query(Income).all()
    return {"data": incomes}

# Run the application with: uvicorn filename:app --reload
