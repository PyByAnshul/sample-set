import os
import random

class Config:
    
    MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017/"
    SECRET_KEY = os.getenv("SECRET_KEY") or "".join(
        [chr(random.randint(65, 92)) for _ in range(50)]
    )