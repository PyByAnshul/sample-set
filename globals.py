# import logging
import pymongo
from config import Config
from pymongo.server_api import ServerApi
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger()


PRIM_DB_URL=Config.MONGO_URI

class Db:
    def __init__(self):
        self.mongo_url = PRIM_DB_URL
        self.client = pymongo.MongoClient(PRIM_DB_URL)
        self.db = self.client['sample_set']
        self.post = self.db["post"]

db = Db()
