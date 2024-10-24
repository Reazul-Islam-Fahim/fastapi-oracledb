from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_db_connection

app = FastAPI()


# Pydantic model for incoming data
class Item(BaseModel):
    id: int



@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI with Oracle!"}



@app.get("/data")
async def get_data():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM TEST")  # Specify columns for clarity
        rows = cursor.fetchall()
    connection.close()
    return {"data": rows}



@app.post("/data")
async def create_item(item: Item):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO TEST (id) VALUES (:id)",
                (item.id,)  # Add a comma here
            )
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    connection.close()
    return {"message": "Item created successfully", "item": item}
