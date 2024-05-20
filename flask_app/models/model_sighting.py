#import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_user
# model the class after the user table from our database
from flask_app import DATABASE
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Sighting:
   def __init__(self, data:dict):
      self.id = data['id']
      self.location = data['location']
      self.date = data['date']
      self.num_of_sas = data['num_of_sas']
      self.happened = data['happened']
      self.created_at = data['created_at']
      self.updated_at = data['updated_at']

      #Add additional columns from database here

   def info(self):
      returnStr = f"Location = {self.location} || Date = {self.date} || num_of_sas = {self.num_of_sas} happened = {self.happened}"
      return returnStr

#CREATE
   @classmethod
   def create_one(cls, data:dict):
      query = "INSERT INTO sightings (location, date, num_of_sas, happened, user_id) VALUES (%(location)s, %(date)s, %(num_of_sas)s, %(happened)s, %(user_id)s)"
      result = connectToMySQL(DATABASE).query_db(query, data)
      print(data)
      return result
       
   # now we use the class methods to query our database 

#READ
   @classmethod
   def get_all(cls) -> list:
      query = "SELECT * FROM sightings;"
      #make sure to call the connectToMySQL function with the schema you are targeting

      results = connectToMySQL(DATABASE).query_db(query)
      #create an empty list to append our instances of sightings
      if not results:
         return []

      instance_list = []
      # iterate over the db results anad create instances of sightings with cls.
      for dictionary in results:
         instance_list.append(cls(dictionary))
      return instance_list

   @classmethod
   def get_one(cls, data):
      query = "SELECT * FROM sightings WHERE sightings.id = %(id)s;"
      print(query)
      results = connectToMySQL(DATABASE).query_db(query, data)
      if not results:
         return []

      instance_list = []

      for dictionary in results:
         instance_list.append(cls(dictionary))
      return instance_list


   @classmethod
   def get_by_email(cls,data):
      query = "SELECT * FROM sightings WHERE email = %(email)s;"
      result = connectToMySQL(DATABASE).query_db(query,data)
      # Didn't find a matching user
      if len(result) < 1:
         return False
      return cls(result[0])


# Validators

   @staticmethod
   def validator(data: dict) -> bool:
      is_valid = True

      if(len(data['location']) < 2):
         flash("Location is required!", "err_sightings_location")
         is_valid = False
         

      if(len(data['date']) < 1):
         flash("Please select a date for your sighting", "err_sightings_date")
         is_valid = False

      if(len(data['num_of_sas'])) == 0:
         flash("Please enter a valid number of Sasquatches", "err_sightings_num_of_sas")
         is_valid = False


      if(len(data['happened']) > 50):
         flash("Max Character count is 50!", "err_sightings_happened")
         is_valid = False

      if(len(data['happened']) < 1):
         flash("What happened at your sighting?", "err_sightings_happened")
         is_valid = False



      return is_valid
      #run through some if checks -> if if checks come out to be bad then is_valid = False



# SAVE
   @classmethod
   def save(cls,data):
      query = "INSERT INTO sightings (location, date, num_of_sas, happened, user_id) VALUES (%(location)s, %(date)s, %(num_of_sas)s, %(happened)s, %(user_id)s);"
      result = connectToMySQL(DATABASE).query_db(query, data)
      return result

   #DELETE
   @classmethod
   def delete(cls, data):
      query = "DELETE FROM sightings WHERE id = %(id)s;"
      return connectToMySQL(DATABASE).query_db(query, data)

   #UPDATE
   @classmethod
   def update(cls, data):
      query = "UPDATE sightings SET location = %(location)s, date = %(date)s, num_of_sas = %(num_of_sas)s, happened = %(happened)s WHERE id = %(id)s;"
      return connectToMySQL(DATABASE).query_db(query, data)

# for the show route to show the one sighting that you selected on the "view sighting" URL
   @classmethod
   def get_one_sighting(cls, data):
      query = "SELECT * FROM sightings JOIN users ON users.id = sightings.user_id WHERE sightings.id = %(id)s;"
      print(query)
      results = connectToMySQL(DATABASE).query_db(query, data)
      if results:

         one_sighting = cls(results[0])
         for dictionary in results:

            users_data = {
               **dictionary,
               "id": dictionary["users.id"],
               "updated_at": dictionary["users.updated_at"],
               "created_at": dictionary["users.created_at"]
            }
            print(users_data)

            u = model_user.User(users_data)
            one_sighting.u = u
         return one_sighting

# for the display route where it shows the user that created the sighting in the "posted by" coloumn
   @classmethod
   def get_sightings(cls):
      query = "SELECT * FROM sightings JOIN users ON users.id = sightings.user_id;"
      print(query)
      results = connectToMySQL(DATABASE).query_db(query)
      if results:

         instance_list = []

         for dictionary in results:
            one_sighting = cls(dictionary)

            users_data = {
               **dictionary,
               "id": dictionary["users.id"],
               "updated_at": dictionary["users.updated_at"],
               "created_at": dictionary["users.created_at"]
            }
            print(users_data)

            u = model_user.User(users_data)
            one_sighting.u = u
            instance_list.append(one_sighting)
         return instance_list
