from django.shortcuts import render

from django.http import HttpResponse
from .models import Post
from .models import User, UserProfile
import requests

def post_list(request):


    link_users = "http://jsonplaceholder.typicode.com/users"
    link_posts = "http://jsonplaceholder.typicode.com/posts"

    response1 = requests.get(link_users)
    users = response1.json()

    response2 = requests.get(link_posts)
    posts = response2.json()

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
        u = User.objects.update_or_create(id=id, username=username, first_name=name, email=email)
        up = UserProfile.objects.update_or_create(id=id, user_id=id, address=address, phone=phone, website=website, company=company)

    for post in posts:
        id = post['id']
        title = post['title']
        body = post['body']
        userId = post['userId']
        p = Post.objects.update_or_create(id=id, title=title, body=body, userId_id=userId)



    posts = Post.objects.all()
    return render(request,
	          'blog/list.html',
	          {'posts': posts})