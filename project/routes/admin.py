from flask import Blueprint

from ..extensions import db
from ..models.user import User
from ..models.berita import Berita
from ..models.berita_img import Berita_img

admin = Blueprint('admin', __name__)

