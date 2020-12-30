import pandas
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="P@ssw0rd",
  db="mysql"
)

cursor = db.cursor()
#cursor.execute("CREATE DATABASE recommendersystem")
cursor.close()
db.close()

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="P@ssw0rd",
  db="recommendersystem"
)

cursor = db.cursor()
cursor.execute("CREATE TABLE user_movie (user_id INT, movie_id INT, rating INT)")
cursor.execute("CREATE TABLE users (id INT, email VARCHAR(20), name VARCHAR(255), password VARCHAR(8), profile VARCHAR(500), baseline INT)")
cursor.execute("CREATE TABLE movie (id INT, title VARCHAR(100), overview VARCHAR(500), cast VARCHAR(255), director VARCHAR(50), genres VARCHAR(150), keywords VARCHAR(150), profile VARCHAR(500))")
cursor.execute("CREATE TABLE neigbourhood (movie_id INT, similar_movie_id INT)")

cursor.execute("DROP TABLE users")
cursor.execute("DROP TABLE user_movie")
cursor.execute("DROP TABLE movie")
cursor.execute("DROP TABLE neigbourhood")
cursor.execute("DROP DATABASE recommendersystem")
cursor.close()
db.close()