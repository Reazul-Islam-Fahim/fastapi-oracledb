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


class TableName(BaseModel):
    table_name: str


class TaxInput(BaseModel):
    area: str
    min_tax : int

    
class AreaTaxCalculator(BaseModel):
    def __init__(self, tax_in : TaxInput):
        self.area = tax_in.area
        self.min_tax = tax_in.min_tax

    def tex_calc(self):
        if self.area.upper() == "DHAKA" or self.area.upper() == "CHITTAGONG"  or self.area.upper() == "CHATTOGRAM" or self.area.upper() == "SOUTH DHAKA" or self.area.upper() == "NORTH DHAKA":
            area_tax = 5000
        if self.area.upper() == "BARISHAL" or self.area.upper() == "COMILLA"  or self.area.upper() == "GAZIPUR" or self.area.upper() == "KHULNA" or self.area.upper() == "MYMENSINGH" or self.area.upper() == "NARAYANGANJ" or self.area.upper() == "RAJSHAHI" or self.area.upper() == "RANGPUR" or self.area.upper() == "SYLHET":
            area_tax = 4000
        else:
            area_tax = 3000

        return area_tax