from flask import Flask, render_template, url_for, request
from flask import redirect, jsonify, make_response, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
import random
import string
import json
import httplib2
import requests
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

app = Flask(__name__)

# Connect to Database
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Get id from User Logged in
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Get e-mail from user Logged in
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Show Home page, with all items of udacity Course Catalog
@app.route('/')
@app.route('/catalog')
def showCategories():
    # Get all categories
    categories = session.query(Category).all()

    # Get lastest items added
    categoryItems = session.query(CategoryItem).all()

    return render_template('categories.html', categories=categories,
                           categoryItems=categoryItems)


# Show items of a specific category
@app.route('/catalog/<int:catalog_id>')
@app.route('/catalog/<int:catalog_id>/items')
def showCategory(catalog_id):
    # Get all categories
    categories = session.query(Category).all()

    # Get category
    category = session.query(Category).filter_by(id=catalog_id).first()

    # Get name of category
    categoryName = category.name

    # Get all items of a specific category
    categoryItems = session.query(
                                  CategoryItem
                                 ).filter_by(
                                             category_id=catalog_id
                                             ).all()

    # Get count of category items
    categoryItemsCount = session.query(
                                       CategoryItem
                                       ).filter_by(
                                                   category_id=catalog_id
                                                   ).count()
    return render_template('category.html', categories=categories,
                           categoryItems=categoryItems,
                           categoryName=categoryName,
                           categoryItemsCount=categoryItemsCount
                           )


# Show the item's information detailed and show the edit and delete options
# if User Logged in is the its creator
@app.route('/catalog/<int:catalog_id>/items/<int:item_id>')
def showCategoryItem(catalog_id, item_id):
    # Get category item
    categoryItem = session.query(CategoryItem).filter_by(id=item_id).first()

    # Get creator of item
    creator = getUserInfo(categoryItem.user_id)

    return render_template('categoryItem.html',
                           categoryItem=categoryItem,
                           creator=creator
                           )


# Add a new item if there is an user logged in
@app.route('/catalog/add', methods=['GET', 'POST'])
def addCategoryItem():
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        # TODO: Retain data when there is an error

        if not request.form['name']:
            flash('Please add a course name')
            return redirect(url_for('addCategoryItem'))

        if not request.form['description']:
            flash('Please add a description')
            return redirect(url_for('addCategoryItem'))

        # Add category item
        newCategoryItem = CategoryItem(
                                       name=request.form['name'],
                                       description=request.form['description'],
                                       category_id=request.form['category'],
                                       user_id=login_session['user_id']
                                       )
        session.add(newCategoryItem)
        session.commit()

        return redirect(url_for('showCategories'))
    else:
        # Get all categories
        categories = session.query(Category).all()
        return render_template('addCategoryItem.html', categories=categories)


# Edit an item if the user logged in is the its creator
@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(catalog_id, item_id):
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    # Get category item
    categoryItem = session.query(CategoryItem).filter_by(id=item_id).first()

    # Get creator of item
    creator = getUserInfo(categoryItem.user_id)

    # Check if logged in user is creator of category item
    if creator.id != login_session['user_id']:
        return redirect('/login')

    # Get all categories
    categories = session.query(Category).all()

    if request.method == 'POST':
        if request.form['name']:
            categoryItem.name = request.form['name']
        if request.form['description']:
            categoryItem.description = request.form['description']
        if request.form['category']:
            categoryItem.category_id = request.form['category']
        return redirect(url_for('showCategoryItem',
                                catalog_id=categoryItem.category_id,
                                item_id=categoryItem.id
                                )
                        )
    else:
        return render_template('editCategoryItem.html',
                               categories=categories,
                               categoryItem=categoryItem
                               )


# Delete an item if the user logged in is the its creator
@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteCategoryItem(catalog_id, item_id):
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    # Get category item
    categoryItem = session.query(CategoryItem).filter_by(id=item_id).first()

    # Get creator of item
    creator = getUserInfo(categoryItem.user_id)

    # Check if logged in user is creator of category item
    if creator.id != login_session['user_id']:
        return redirect('/login')

    if request.method == 'POST':
        session.delete(categoryItem)
        session.commit()
        return redirect(url_for('showCategory',
                        catalog_id=categoryItem.category_id
                                )
                        )
    else:
        return render_template('deleteCategoryItem.html',
                               categoryItem=categoryItem
                               )


# Call the login page
@app.route('/login')
def login():
    # Create anti-forgery state token
    state = ''.join(random.choice(
                                  string.ascii_uppercase + string.digits
                                  ) for x in xrange(32)
                    )
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Call the logout function and clear the session
@app.route('/logout')
def logout():
    if 'provider' in login_session:
        fbdisconnect()
        del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        print "login session infos deleted"
        return redirect(url_for('showCategories'))
    else:
        print "you are not logged in"
        return redirect(url_for('showCategories'))


# Log in using Facebook account by Facebook's API
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    app_id = json.loads(open('fb_client_secrets.json',
                             'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json',
                                 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "access token retornado %s " % result

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    print "novo token %s " % data

    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("Now logged in as %s" % login_session['username'])
    return output


# Disconnect from Facebook account
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    # The access token must be included to successfully logout
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)  # noqa
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    print "you have been logged out"
    print result


# ENDPOINT API JSON - returns a specific item
@app.route('/catalog/item/<int:item_id>/JSON')
def showItemJSON(item_id):
    item = session.query(CategoryItem).filter_by(id=item_id)
    return jsonify(Item=[i.serialize for i in item])


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
