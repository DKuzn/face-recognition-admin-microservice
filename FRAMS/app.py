# FRAMS/app.py
#
# Copyright (C) 2022  Дмитрий Кузнецов
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Tuple, Dict, Union
from FRAMS.datamodels import RequestModel
from FRAMS.db_worker import DbWorker
from FRAMS import __version__
import os

app: FastAPI = FastAPI(title='Face Recognition Admin Microservice', version=__version__)

origins: List[str] = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FEATURES_DB = os.environ['FEATURES_DB']
PERSONS_DB = os.environ['PERSONS_DB']

db_worker = DbWorker(FEATURES_DB, PERSONS_DB)


@app.post('/')
async def main(request: RequestModel):
    if request.image and (request.name or request.surname):
        try:
            db_worker.add_person(request.image, request.name, request.surname)
        except IndexError:
            raise HTTPException(status_code=422, detail="Cannot find face on the image.")
    else: 
        raise HTTPException(status_code=422, detail='One or more fields are empty.')
