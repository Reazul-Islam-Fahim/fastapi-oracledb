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
    column_name: str

def is_valid_column_name(name: str) -> bool:
    # Basic validation: table names should start with a letter and can contain letters, numbers, and underscores
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None

@app.post("/create-column")
async def create_table(column_schema: ColumnSchema = Query(...)):
    if not is_valid_column_name(column_schema.column_name):
        raise HTTPException(status_code=400, detail="Invalid column name.")
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            create_column_sql = f"""
                ALTER TABLE HI
                ADD {column_schema.column_name} varchar(255)
            """
            cursor.execute(create_column_sql)
            connection.commit()
            return {"message": f"column '{column_schema.column_name}' created successfully."}
    except Exception as e:
        connection.rollback()
        # Consider logging the error here for your own debugging purposes
        raise HTTPException(status_code=400, detail="Error creating column.")
    finally:
        connection.close()


@app.delete("/delete-column")
async def delete_column(column_schema: ColumnSchema = Query(...)):
    if not is_valid_column_name(column_schema.column_name):
        raise HTTPException(status_code=400, detail="Invalid column name.")
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            delete_column_sql = f"""
                ALTER TABLE HI
                DROP {column_schema.column_name}
            """
            cursor.execute(delete_column_sql)
            connection.commit()
            return {"message": f"column '{column_schema.column_name}' deleted successfully."}
    except Exception as e:
        connection.rollback()
        # Consider logging the error here for your own debugging purposes
        raise HTTPException(status_code=400, detail="Error deleting column.")
    finally:
        connection.close()