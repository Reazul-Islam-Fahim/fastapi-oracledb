from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pydantic_core
from typing import Dict, Annotated
from db import get_db_connection
import oracledb
import logging
from fastapi.middleware.cors import CORSMiddleware
from salary_income_calculator import TaxLiabilityCalculator

app = FastAPI()

# origins = [
#     "https://localhost:8000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = origins,
#     allow_credentials = True,
#     allow_methods = ['*'],
#     allow_headers = ['*']
# )

class TableName(BaseModel):
    table_name: str


class InvestmentInput(BaseModel):
    id: Annotated[int, "ID: "]
    dps : Annotated[int, "DPS: "] = 0
    gov_securities : Annotated[int, "Government Securities: "] = 0
    eft : Annotated[int, "Unit Certificate/Mutual Fund/EFT: "] = 0
    life_insurance_policy_value : Annotated[int, "Life Insurance Policy Value: "] = 0
    life_insurance_given_premium : Annotated[int, "Life Insurance Given Premium: "] = 0
    other : Annotated[int, "Others: "] = 0

class InvestmentCalculator:
    def __init__(self, inv_data: InvestmentInput):
        self.inv_data = inv_data
        self.allowable_investment = 0

    def inv_calc(self):
        # Calculate allowable investment based on dps
        self.allowable_investment += min(self.inv_data.dps, 120000)

        # Calculate allowable investment based on government securities
        self.allowable_investment += min(self.inv_data.gov_securities, 500000)

        # Calculate allowable investment based on EFT
        self.allowable_investment += min(self.inv_data.eft, 500000)

        # Calculate allowable investment based on life insurance
        life_insurance_investment = min(self.inv_data.life_insurance_policy_value * 0.1, self.inv_data.life_insurance_given_premium)
                                          
        self.allowable_investment += life_insurance_investment

        # Add other investments
        self.allowable_investment += self.inv_data.other

        return self.allowable_investment
    
class RebateCalculator:
    def __init__(self, inv_calculator: InvestmentCalculator):
        self.investment_calculator = inv_calculator

    def calculate_rebate(self):
            
        rebate_sector1 = TaxLiabilityCalculator._calculate_tax_liability()

        rebate_sector2 = self.investment_calculator.allowable_investment * 0.15
        
        rebate = min(rebate_sector1, rebate_sector2, 1000000 )

        return rebate
    

@app.get("/get_rebate/")
async def get_rebate(tablename : TableName = Query(...)):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {tablename.table_name}")
        column_names = [desc[0] for desc in cursor.description]
            
        # Fetch all rows
        rows = cursor.fetchall()

        # Format rows with column names
        data = [dict(zip(column_names, row)) for row in rows]
        
        return {"data": data}

    except Exception as e:
        logging.error(f"Error fetching income records: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    finally:
        cursor.close()
        connection.close()



@app.post("/post_rebate/")
async def post_rebate(tablename : TableName = Query(...), inv_input : InvestmentInput = Query(...)):
    

    inv_calculator = InvestmentCalculator(inv_input)
    investment = inv_calculator.inv_calc()

    rebate_calculator = RebateCalculator(investment)
    rebate = rebate_calculator.calculate_rebate()

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {tablename.table_name} (ID, Allowable Investment, Rebate) VALUES (:1, :2, :3)",
                (inv_input.id, investment, rebate)
            )
            connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    connection.close()

    return {
        "rebate" : rebate
    }