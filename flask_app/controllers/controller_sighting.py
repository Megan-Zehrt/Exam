from flask_app import app
from flask import render_template,redirect,request,session,flash, url_for
from flask_app.models.model_sighting import Sighting
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument




@app.route("/sighting/new")
def new_sighting():
    if not "user_id" in session:
        return redirect('/')

    sightings= Sighting.get_all()
    user = User.get_one({ 'id': session['user_id']})
    return render_template("new_sighting.html", sightings=sightings, user=user)

@app.route("/create_sighting", methods=['POST'])
def create_sighting():
    is_valid = Sighting.validator(request.form)
    if not is_valid:
        return redirect('/sighting/new')
    data = {
      'location': request.form['location'],
      'date': request.form['date'],
      'num_of_sas': request.form['num_of_sas'],
      'happened': request.form['happened'],
      'user_id': session['user_id']
    }
    id = Sighting.create_one(data)
    return redirect("/dashboard")

# Show sighting

@app.route("/sighting/<int:id>")
def sighting_show_id(id):
    print("*********",id,"**********")
    if not "user_id" in session:
      return redirect('/')

    sight = Sighting.get_sightings()
    sightings = Sighting.get_one_sighting({ 'id': id})
    user = User.get_one({ 'id': session['user_id']})
    return render_template("show_sighting.html", sightings = sightings, user = user, sight=sight )

# Delete sighting
@app.route("/sighting/delete/<int:sighting_id>")
def delete_sighting(sighting_id):
   data = {
      'id': sighting_id
   }
   Sighting.delete(data)
   return redirect("/dashboard")

# Edit sighting

@app.route("/sighting/edit/<int:id>")
def edit_sighting(id):
  if not "user_id" in session:
    return redirect('/')

    is_valid = Sighting.validator(request.form)
    if not is_valid:
        return redirect('/sighting/edit')

  data = {"id" : id}
  sightings = Sighting.get_one_sighting(data)
  print(sightings)
  user = User.get_one({ 'id': session['user_id']})
  return render_template("sighting_edit.html", sightings = sightings, user=user)


@app.route("/sighting/edit", methods=['POST'])
def update_sighting():
    is_valid = Sighting.validator(request.form)
    if not is_valid:
        return redirect(f"/sighting/edit/{request.form['id']}")
    data = {
      'id' : request.form['id'],
      'location': request.form['location'],
      'date': request.form['date'],
      'num_of_sas': request.form['num_of_sas'],
      'happened': request.form['happened'],
      'user_id': session['user_id']
    }
    Sighting.update(data)
    return redirect("/dashboard")

