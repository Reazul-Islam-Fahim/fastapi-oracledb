from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Annotated
from db import get_db_connection
import oracledb
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

class TableName(BaseModel):
    table_name: str

class TaxInput(BaseModel):
    table_name: str
    id: int
    area: str
    min_tax: int

class TaxCalculator:
    def __init__(self, tax_in: TaxInput):
        self.id = tax_in.id
        self.area = tax_in.area
        self.min_tax = tax_in.min_tax

    def tax_calc(self):
        # Determine area tax based on the area
        if self.area.upper() in ["DHAKA", "CHITTAGONG", "CHATTOGRAM", "SOUTH DHAKA", "NORTH DHAKA"]:
            area_tax = 5000
        elif self.area.upper() in ["BARISHAL", "COMILLA", "GAZIPUR", "KHULNA", "MYMENSINGH", "NARAYANGANJ", "RAJSHAHI", "RANGPUR", "SYLHET"]:
            area_tax = 4000
        else:
            area_tax = 3000

        # Fetch tax liability
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT TAX_LIABILITY FROM HI WHERE ID = :id",
                    {"ID": self.id}
                )
                result = cursor.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="No matching record found")
                tax_liability = result[0]

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            connection.close()

        # Fetch rebate
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT REBATE FROM REBATE WHERE ID = :id",
                    {"ID": self.id}
                )
                result = cursor.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="No matching record found")
                rebate = result[0]

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            connection.close()

        # Calculate net tax
        net_tax_liability = tax_liability - rebate
        actual_payable_tax = max(net_tax_liability, self.min_tax, area_tax)

        return actual_payable_tax

@app.get("/get_rebate/")
async def get_rebate(tablename: TableName = Query(...)):
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
async def post_rebate(tax_input: TaxInput = Query(...)):
    tax_calculator = TaxCalculator(tax_input)
    actual_payable_tax = tax_calculator.tax_calc()

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {tax_input.table_name} (ID, TAX) VALUES (:1, :2)",
                (tax_input.id, actual_payable_tax)
            )
            connection.commit()
            logging.info(f"Inserted payable tax: {actual_payable_tax} for ID: {tax_input.id} into {tax_input.table_name}")
    except Exception as e:
        connection.rollback()
        logging.error(f"Error inserting rebate: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        connection.close()

    return {
        "Actual Payable Tax": actual_payable_tax
    }
