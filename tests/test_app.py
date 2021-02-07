# Import the necessary modules
import unittest
from flask import url_for
from flask_testing import TestCase
from datetime import datetime

# import the app's classes and objects
from app import app, db, Log_date,Food,Food_date

# Create the base class
class TestBase(TestCase):
    def create_app(self):

        # Pass in testing configurations for the app. Here we use sqlite without a persistent database for our tests.
        app.config.update(SQLALCHEMY_DATABASE_URI='mysql+pymysql://qatraining:Qatraining@1975@localhost/flask_project1_test',
                # SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True
                )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # Create table
        db.create_all()

        # Create test log_date
        sample_log_date = Log_date(entry_date='2020-02-04')

        # Create test Food
        sample_food = Food(name="Pizza",protein=10,carb=15,fat=10,calories=190)
        
        # Create test food_date
        sample_food_date=Food_date(food_id=1,log_date_id=1)

        # save users to database
        db.session.add(sample_log_date)
        db.session.add(sample_food)
        db.session.commit()
        db.session.add(sample_food_date)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
        
        #  Food_date.query.delete()
        #  Log_date.query.delete()
        #  Food.query.delete()


# Write a test class for testing that the index page loads but we are not able to run a get request for delete and update routes.
class TestViews(TestBase):

    def test_home_get(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)

    def test_food_get(self):
        response = self.client.get(url_for('food'))
        self.assertEqual(response.status_code,200)

    def test_update_food_get(self):
        response = self.client.get(url_for('edit',id=1))
        self.assertEqual(response.status_code,200)
    
    def test_delete_day_get(self):
        response = self.client.get(url_for('delete',id=1))
        self.assertEqual(response.status_code,200)

    def test_day_post(self):
        response = self.client.get(url_for('index',date='2020-02-06'))
        self.assertEqual(response.status_code,200)

    def test_datefood_post(self):
        response = self.client.get(url_for('view',date='2020-02-04'))
        self.assertEqual(response.status_code,200)


# Test Posting new Food
class TestFoodPost(TestBase):
    def test_post_food(self):
        response = self.client.post(
            url_for('food'),
            data = dict(name="Burger", protein=20,carb=24,fat=15,calories=311),
            follow_redirects=True
            )
        self.assertEqual(response.status_code,200)

# Test updating

class TestUpdate(TestBase):
    def test_update_food(self):
        response = self.client.post(
            url_for('edit',id=1),
            data = dict(id=1, name="Burger", protein=20,carb=24,fat=15,calories=311),
            follow_redirects=True
            )
        self.assertEqual(response.status_code,200)
# Test Deleting

class TestDelete(TestBase):
    def test_delete_day(self):
        response = self.client.post(
            url_for('delete',id=1),
            data = dict(id=1),
            follow_redirects=True
            )
        self.assertEqual(response.status_code,200)