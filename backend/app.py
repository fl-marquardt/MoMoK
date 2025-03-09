import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from database import init_db, db, Cluster, Location, Person, Institution, Role, User

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            static_folder='../frontend',
            static_url_path='',
            template_folder='../frontend')

# Configure app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-development-only')

# Initialize database
db = init_db(app)

# Initialize Flask extensions
login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/clusters')
def get_clusters():
    clusters = Cluster.query.all()
    return jsonify([{
        'id': cluster.id,
        'name': cluster.name,
        'description': cluster.description
    } for cluster in clusters])

@app.route('/api/locations')
def get_locations():
    locations = Location.query.all()
    return jsonify([{
        'id': location.id,
        'name': location.name,
        'description': location.description,
        'coordinates': location.coordinates,
        'cluster_id': location.cluster_id
    } for location in locations])

@app.route('/api/location/<int:location_id>')
def get_location(location_id):
    location = Location.query.get_or_404(location_id)
    return jsonify({
        'id': location.id,
        'name': location.name,
        'description': location.description,
        'coordinates': location.coordinates,
        'cluster_id': location.cluster_id,
        'cluster_name': location.cluster.name if location.cluster else None
    })

@app.route('/api/persons')
def get_persons():
    persons = Person.query.all()
    return jsonify([{
        'id': person.id,
        'first_name': person.first_name,
        'last_name': person.last_name,
        'email': person.email,
        'institution_id': person.institution_id,
        'institution_name': person.institution.name if person.institution else None
    } for person in persons])

@app.route('/api/institutions')
def get_institutions():
    institutions = Institution.query.all()
    return jsonify([{
        'id': institution.id,
        'name': institution.name,
        'type': institution.type,
        'city': institution.city,
        'country': institution.country
    } for institution in institutions])

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True) 