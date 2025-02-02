from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pydantic_core
from typing import Annotated
from db import get_db_connection
import oracledb
import logging
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

logging.basicConfig(level=logging.INFO)

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
    table_name: str
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

        self.allowable_investment = 0
        
        # Calculate allowable investment based on dps
        self.allowable_investment += min(self.inv_data.dps, 120000)

        # Calculate allowable investment based on government securities
        self.allowable_investment += min(self.inv_data.gov_securities, 500000)

        # Calculate allowable investment based on EFT
        self.allowable_investment += min(self.inv_data.eft, 500000)

        # Calculate allowable investment based on life insurance
        self.allowable_investment += min(self.inv_data.life_insurance_policy_value * 0.1, self.inv_data.life_insurance_given_premium)

        # life_insurance_investment = min(self.inv_data.life_insurance_policy_value * 0.1, self.inv_data.life_insurance_given_premium)
                                          
        # self.allowable_investment += life_insurance_investment

        # Add other investments
        self.allowable_investment += self.inv_data.other

        return self.allowable_investment
    
class RebateCalculator:
    def __init__(self, inv_calculator: InvestmentCalculator):
        self.investment_calculator = inv_calculator

    def calculate_rebate(self, inv_input: InvestmentInput):
            
        # get TAXABLE_INCOME from HI table
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Parameterized query to prevent SQL injection
                cursor.execute(
                    "SELECT TAXABLE_INCOME FROM HI WHERE ID = :id",
                    {"ID": inv_input.id}
                )
                print("working")

                # Fetch a single row
                result = cursor.fetchone()
                # print(result)

                if result is None:
                    raise HTTPException(status_code=404, detail="No matching record found")

                # Extract the first element from the result tuple
                rebate_sector1 = result[0] * 0.03
                print(rebate_sector1)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            connection.close()

        print(self.investment_calculator.inv_calc())

        rebate_sector2 = self.investment_calculator.inv_calc() * 0.15


        print(rebate_sector2)
        
        rebate = min(rebate_sector1, rebate_sector2, 1000000)

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
async def post_rebate(inv_input : InvestmentInput = Query(...)):
    

    inv_calculator = InvestmentCalculator(inv_input)
    investment = inv_calculator.inv_calc()

    rebate_calculator = RebateCalculator(inv_calculator)
    rebate = rebate_calculator.calculate_rebate(inv_input)

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {inv_input.table_name} (ID, ALLOWABLE_INVESTMENT, REBATE) VALUES (:1, :2, :3)",
                (inv_input.id, investment, rebate)
            )
            connection.commit()
            logging.info(f"Inserted rebate: {rebate} for ID: {inv_input.id} into {inv_input.table_name}")
    except Exception as e:
        connection.rollback()
        logging.error(f"Error inserting rebate: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        connection.close()

    return {
        "rebate" : rebate
    }