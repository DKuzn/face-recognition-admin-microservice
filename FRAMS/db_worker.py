# FRAMS/db_worker.py
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

from FRMS.database import Face, get_connection, create_table as create_faces
from FRMS.utils.face_detector import FaceDetector
from FRMS.utils.feature_extractor import FeatureExtractor
from PIMS.database import PersonInfo, create_table as create_persons
import base64
import io
from PIL import Image


class DbWorker:
    def __init__(self, features_db, persons_db) -> None:
        self.features_db, _ = get_connection(features_db)
        self.persons_db, _ = get_connection(persons_db)
        create_faces(features_db)
        create_persons(persons_db)
        self._face_detector = FaceDetector()
        self._feature_extractor = FeatureExtractor()

    def add_person(self, b64_image: str, name: str, surname: str):
        face_img = self._open_img(b64_image)
        face = self._face_detector.find_faces(face_img)[0]
        person_id = self._add_person_info(PersonInfo(b64_image, face[1], name, surname))
        features = self._feature_extractor.extract_features(face[0])
        self._add_face(Face(features, person_id))

    def _add_person_info(self, person_info: PersonInfo) -> int:
        self.persons_db.add(person_info)
        self.persons_db.flush()
        person_id = person_info.id
        self.persons_db.commit()
        return person_id

    def _add_face(self, face: Face) -> None:
        self.features_db.add(face)
        self.features_db.commit()

    @staticmethod
    def _open_img(simg) -> Image.Image:
        byte_img: bytes = base64.b64decode(simg)
        img: Image.Image = Image.open(io.BytesIO(byte_img)).convert('RGB')
        return img
