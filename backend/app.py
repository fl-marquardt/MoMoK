import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv, find_dotenv
from database import init_db, db, Cluster, Location, Person, Institution, Role, User

# Load environment variables with explicit path and override
print(f"Current working directory: {os.getcwd()}")
dotenv_path = find_dotenv()
if dotenv_path:
    print(f"Loading .env from: {dotenv_path}")
    load_dotenv(dotenv_path, override=True)
    # Verify environment variables were loaded
    db_url = os.getenv('DATABASE_URL')
    print(f"DATABASE_URL loaded: {'Yes' if db_url else 'No'}")
else:
    print("Warning: .env file not found!")

# Initialize Flask app
app = Flask(__name__, 
            static_folder='../frontend',
            static_url_path='',
            template_folder='../frontend')

# Set secret key from environment
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
    result = []
    for location in locations:
        # Convert coordinates to string representation if they exist
        coordinates_str = None
        if location.coordinates:
            try:
                # Try to convert to WKT (Well-Known Text) format
                coordinates_str = str(location.coordinates)
            except Exception as e:
                print(f"Error converting coordinates: {e}")
        
        # Get cluster name if cluster exists
        cluster_name = None
        if location.cluster:
            cluster_name = location.cluster.name
        
        # Create location dict
        location_dict = {
            'id': location.id,
            'name': location.name,
            'description': location.description,
            'coordinates': coordinates_str,
            'coordinates_str': coordinates_str,
            'cluster_id': location.cluster_id,
            'cluster_name': cluster_name
        }
        result.append(location_dict)
    
    return jsonify(result)

@app.route('/api/location/<int:location_id>', methods=['GET', 'DELETE'])
def get_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    if request.method == 'DELETE':
        try:
            # Check for related records
            has_related_records = False
            
            # Check for related measurement equipment
            if location.measurement_equipment:
                has_related_records = True
            
            # Check for related location journals
            if location.location_journals:
                has_related_records = True
                
            # Check for related usage history
            if location.usage_history:
                has_related_records = True
                
            # Check for related hydrological history
            if location.hydrological_history:
                has_related_records = True
                
            # Check for related soil history
            if location.soil_history:
                has_related_records = True
                
            # Check for related vegetation history
            if location.vegetation_history:
                has_related_records = True
                
            # Check for related person roles
            if hasattr(location, 'person_roles') and location.person_roles:
                has_related_records = True
                
            # Check for related land parcels
            if location.land_parcels:
                has_related_records = True
            
            if has_related_records:
                return jsonify({
                    'success': False, 
                    'message': 'Cannot delete location because it has related records. Please remove all related records first.'
                }), 400
            
            db.session.delete(location)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Location deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # GET request handling
    # Convert coordinates to string representation if they exist
    coordinates_str = None
    if location.coordinates:
        try:
            # Try to convert to WKT (Well-Known Text) format
            coordinates_str = str(location.coordinates)
        except Exception as e:
            print(f"Error converting coordinates: {e}")
    
    return jsonify({
        'id': location.id,
        'name': location.name,
        'description': location.description,
        'coordinates_str': coordinates_str,
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

@app.route('/api/check-auth')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'user': {'id': current_user.id, 'username': current_user.username}})
    else:
        return jsonify({'authenticated': False})

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True) 