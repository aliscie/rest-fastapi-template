import unittest

from fastapi.testclient import TestClient

from blog.database import Base, engine
from main import app


class TestClass(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)
        self.dummy_users()

    def tearDown(self):
        Base.metadata.drop_all(bind=engine)

    def dummy_users(self):
        pass

    def dummy_data(self):
        pass
