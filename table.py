from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from db import get_db_connection  # Importing the connection function
import uvicorn
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

class TableName(BaseModel):
    table_name : str

class TableSchema(BaseModel):
    table_name: str
    col1 : str
    col2 : str
    col3 : str

def is_valid_table_name(name: str) -> bool:
    # Basic validation: table names should start with a letter and can contain letters, numbers, and underscores
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None

@app.post("/create-table")
async def create_table(table_schema: TableSchema = Query(...)):
    if not is_valid_table_name(table_schema.table_name):
        raise HTTPException(status_code=400, detail="Invalid table name.")

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            create_table_sql = f"""
                CREATE TABLE {table_schema.table_name} (
                    {table_schema.col1} NUMBER PRIMARY KEY,
                    {table_schema.col2} NUMBER,
                    {table_schema.col3} NUMBER
                )
            """
            cursor.execute(create_table_sql)
            connection.commit()
            return {"message": f"Table '{table_schema.table_name}' created successfully."}
    except Exception as e:
        connection.rollback()
        error_message = f"Error creating table:  {str(e)}"
        logging.error(error_message)
        raise HTTPException(status_code=400, detail= error_message)
    finally:
        connection.close()


@app.get("/table")
async def get_table(table_name: TableName = Query(...)):
    if not is_valid_table_name(table_name.table_name):
        raise HTTPException(status_code=400, detail="Invalid table name.")

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            show_table_sql = f"""
                SELECT * FROM {table_name.table_name}
            """
            cursor.execute(show_table_sql)
            connection.commit()
            return {"message": f"Table '{table_name.table_name}' fetched successfully."}
    except Exception as e:
        connection.rollback()
        error_message = f"Error fetching table:  {str(e)}"
        logging.error(error_message)
        raise HTTPException(status_code=400, detail= error_message)
    finally:
        connection.close()


@app.delete("/delete-table")
async def delete_table(table_name: TableName = Query(...)):
    if not is_valid_table_name(table_name.table_name):
        raise HTTPException(status_code=400, detail="Invalid table name.")

    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            delete_table_sql = f"""DROP TABLE {table_name.table_name} CASCADE CONSTRAINTS"""
            cursor.execute(delete_table_sql)
            connection.commit()
            return {"message": f"Table '{table_name.table_name}' deleted successfully."}
    except Exception as e:
        connection.rollback()
        error_message = f"Error deleting table:  {str(e)}"
        logging.error(error_message)
        raise HTTPException(status_code=400, detail= error_message)
    finally:
        connection.close()


@app.get("/")
async def show():
    return {"Welcome": "You can do manipulation in this API"}