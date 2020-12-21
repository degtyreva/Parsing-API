import requests
import sqlite3
link_users = "http://jsonplaceholder.typicode.com/users"
link_posts = "http://jsonplaceholder.typicode.com/posts"

response1 = requests.get(link_users)
users = response1.json()

response2 = requests.get(link_posts)
posts = response2.json()

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()


for user in users:

     id = user['id']
     name = user['name']
     username = user['username']
     email = user['email']
     address = 'street: ' + user['address']['street'] + ' suite: ' + user['address']['suite'] + ' city: ' + user['address']['city'] \
               + ' zipcode: ' + user['address']['zipcode'] + ' geo: ' + user['address']['geo']['lat'] + ' ' + user['address']['geo']['lng']
     phone = user['phone']
     website = user['website']
     company = user['company']['name'] + ' ' + user['company']['catchPhrase'] + ' ' + user['company']['bs']
     cur.execute("INSERT INTO blog_user (id, name, username, email, address, phone, website, company) "
                 "VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(id, name, username, email, address, phone, website, company))
     conn.commit()

for post in posts:
     id = post['id']
     title = post['title']
     body = post['body']
     userId = post['userId']
     cur.execute("INSERT INTO blog_post (id, title, body, userId_id) "
                 "VALUES ('%d', '%s', '%s', '%d')" % (
                 id, title, body, userId))
     conn.commit()


# cur.execute("SELECT blog_user.name, blog_post.title, blog_post.body FROM blog_post INNER JOIN blog_user ON blog_user.id = blog_post.userId_id;")
# all_results3 = cur.fetchall()
# column_names = [description[0] for description in cur.description]
# print(column_names)
# for el in all_results3:
#      print(el)
#
# print(len(all_results3))
