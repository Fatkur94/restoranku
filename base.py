from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# read all restaurant
@app.route('/')
def restaurantlist():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurant_list.html', restaurants = restaurants)

# read single restaurant
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return render_template('menu.html', restaurant=restaurant, items=items)

# creat single restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		new_restaurant = Restaurant(
			name = request.form['name'])
		session.add(new_restaurant)
		session.commit()
		flash('new restaurant created!')
		return redirect(url_for('restaurantlist')) 
	else:
		return render_template('new_restaurant.html')

#edit restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	edited = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		edited.name = request.form['name']
		session.add(edited)
		session.commit()
		flash('restaurant updated!')
		return redirect(url_for('restaurantlist'))
	else:
		return render_template('editrestaurant.html',
								restaurant_id=restaurant_id, i = edited)

#delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	hapus = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(hapus)
		session.commit()
		flash('restaurant deleted')
		return redirect(url_for('restaurantlist'))
	else:
		return render_template('hapusrestaurant.html', i = hapus)

# create new menu
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(
			name = request.form['name'],
			course = request.form['course'],
			description = request.form['description'],
			price = request.form['price'],
			restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash('new menu item created!')
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# edit current menu
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id =menu_id).one()
	if request.method == 'POST':
		editedItem.name = request.form['name']
		editedItem.description = request.form['description']
		editedItem.price = request.form['price']

		session.add(editedItem)
		session.commit()
		flash('menu item updated!')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

	else:
		return render_template(
			'editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = editedItem)

# delete menu
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id= menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash('new menu item deleted!')
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', i = itemToDelete)


#ADD ALL API here 
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()

	return jsonify(MenuItems=[i.serialize for i in items])

#ADD CURRENT API
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem=[menuItem.serialize ])


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host ='0.0.0.0', port = 5000)