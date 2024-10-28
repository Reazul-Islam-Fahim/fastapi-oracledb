from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from db import get_db_connection  # Importing the connection function
import uvicorn
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

class ColumnSchema(BaseModel):
    table_name: str
    column_name: str

def is_valid_column_name(name: str) -> bool:
    # Basic validation: column names should start with a letter and can contain letters, numbers, and underscores
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None

def is_valid_table_name(name: str) -> bool:
    # Basic validation: column names should start with a letter and can contain letters, numbers, and underscores
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None


@app.post("/create-column")
async def create_column(column_schema: ColumnSchema = Query(...)):
    if not is_valid_column_name(column_schema.column_name):
        raise HTTPException(status_code=400, detail="Invalid column name.")
    
    if not is_valid_table_name(column_schema.table_name):
        raise HTTPException(status_code=400, detail="Invalid table name.")
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            create_column_sql = f"""
                ALTER TABLE {column_schema.table_name}
                ADD {column_schema.column_name} varchar(255)
            """
            cursor.execute(create_column_sql)
            connection.commit()
            return {"message": f"column '{column_schema.column_name}' created successfully."}
    except Exception as e:
        connection.rollback()
        error_message = f"Error creating column:  {str(e)}"
        logging.error(error_message)
        raise HTTPException(status_code=400, detail= error_message)
    finally:
        connection.close()


@app.delete("/delete-column")
async def delete_column(column_schema: ColumnSchema = Query(...)):
    if not is_valid_column_name(column_schema.column_name):
        raise HTTPException(status_code=400, detail="Invalid column name.")
    
    if not is_valid_table_name(column_schema.table_name):
        raise HTTPException(status_code=400, detail="Invalid table name.")
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            delete_column_sql = f"""
                ALTER TABLE {column_schema.table_name}
                DROP COLUMN {column_schema.column_name}
            """
            cursor.execute(delete_column_sql)
            connection.commit()
            return {"message": f"column '{column_schema.column_name}' deleted successfully."}
    except Exception as e:
        connection.rollback()
        error_message = f"Error deleting column:  {str(e)}"
        logging.error(error_message)
        raise HTTPException(status_code=400, detail= error_message)
    finally:
        connection.close()