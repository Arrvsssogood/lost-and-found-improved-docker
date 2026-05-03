from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__,
            template_folder=os.path.join('app', 'templates'),
            static_folder=os.path.join('app', 'static'))
app.secret_key = os.environ['SECRET_KEY']
app.config['MONGO_URI'] = os.environ['MONGO_URI']
app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

mongo = PyMongo(app)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

def seed_admin():
    """Create default admin account if it doesn't exist."""
    if not mongo.db.users.find_one({'username': 'admin'}):
        mongo.db.users.insert_one({
            'username': 'admin',
            'email': 'admin@finderskeepers.com',
            'password': generate_password_hash('admin123'),
            'is_admin': True,
            'created_at': datetime.utcnow()
        })
        print("✅ Default admin created: admin / admin123")

# ─────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        if mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]}):
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('register'))

        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'is_admin': False,
            'created_at': datetime.utcnow()
        })
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = mongo.db.users.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['is_admin'] = user.get('is_admin', False)
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('admin_dashboard') if user.get('is_admin') else url_for('index'))

        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ─────────────────────────────────────────────
# PUBLIC ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    stats = {
        'total': mongo.db.items.count_documents({'status': {'$ne': 'rejected'}}),
        'found': mongo.db.items.count_documents({'item_type': 'found', 'status': 'approved'}),
        'claimed': mongo.db.items.count_documents({'claimed': True}),
    }
    recent = list(mongo.db.items.find({'status': 'approved'}).sort('created_at', -1).limit(4))
    return render_template('index.html', stats=stats, recent=recent)


@app.route('/gallery')
def gallery():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '')
    item_type = request.args.get('item_type', '')
    claimed = request.args.get('claimed', '')

    query = {'status': 'approved'}

    if search:
        query['$or'] = [
            {'title': {'$regex': search, '$options': 'i'}},
            {'description': {'$regex': search, '$options': 'i'}},
            {'location': {'$regex': search, '$options': 'i'}},
        ]
    if category:
        query['category'] = category
    if item_type:
        query['item_type'] = item_type
    if claimed == 'yes':
        query['claimed'] = True
    elif claimed == 'no':
        query['claimed'] = False

    items = list(mongo.db.items.find(query).sort('created_at', -1))
    return render_template('gallery.html', items=items, search=search,
                           category=category, item_type=item_type, claimed=claimed)


@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        category = request.form.get('category', 'Other')
        item_type = request.form.get('item_type', 'found')
        date_found = request.form.get('date_found', '')

        if not title or not location:
            flash('Title and location are required.', 'danger')
            return redirect(url_for('report'))

        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Make filename unique
                unique_filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                image_filename = unique_filename

        mongo.db.items.insert_one({
            'title': title,
            'description': description,
            'location': location,
            'category': category,
            'item_type': item_type,
            'date_found': date_found,
            'image': image_filename,
            'status': 'pending',
            'claimed': False,
            'submitted_by': session['user_id'],
            'submitted_by_name': session['username'],
            'created_at': datetime.utcnow()
        })
        flash('Item submitted! It will appear publicly after admin approval.', 'success')
        return redirect(url_for('my_items'))

    return render_template('report.html')


@app.route('/my-items')
@login_required
def my_items():
    items = list(mongo.db.items.find({'submitted_by': session['user_id']}).sort('created_at', -1))
    return render_template('my_items.html', items=items)


@app.route('/my-items/delete/<item_id>')
@login_required
def delete_my_item(item_id):
    item = mongo.db.items.find_one({'_id': ObjectId(item_id), 'submitted_by': session['user_id']})
    if item:
        mongo.db.items.delete_one({'_id': ObjectId(item_id)})
        flash('Item deleted.', 'success')
    else:
        flash('Item not found or permission denied.', 'danger')
    return redirect(url_for('my_items'))

# ─────────────────────────────────────────────
# ADMIN ROUTES
# ─────────────────────────────────────────────

@app.route('/admin')
@admin_required
def admin_dashboard():
    status_filter = request.args.get('status', 'pending')
    search = request.args.get('search', '').strip()

    query = {}
    if status_filter and status_filter != 'all':
        query['status'] = status_filter
    if search:
        query['$or'] = [
            {'title': {'$regex': search, '$options': 'i'}},
            {'location': {'$regex': search, '$options': 'i'}},
            {'submitted_by_name': {'$regex': search, '$options': 'i'}},
        ]

    items = list(mongo.db.items.find(query).sort('created_at', -1))
    counts = {
        'pending': mongo.db.items.count_documents({'status': 'pending'}),
        'approved': mongo.db.items.count_documents({'status': 'approved'}),
        'rejected': mongo.db.items.count_documents({'status': 'rejected'}),
        'all': mongo.db.items.count_documents({}),
    }
    return render_template('admin.html', items=items, counts=counts,
                           status_filter=status_filter, search=search)


@app.route('/admin/approve/<item_id>')
@admin_required
def approve_item(item_id):
    mongo.db.items.update_one({'_id': ObjectId(item_id)}, {'$set': {'status': 'approved'}})
    flash('Item approved.', 'success')
    return redirect(request.referrer or url_for('admin_dashboard'))


@app.route('/admin/reject/<item_id>')
@admin_required
def reject_item(item_id):
    mongo.db.items.update_one({'_id': ObjectId(item_id)}, {'$set': {'status': 'rejected'}})
    flash('Item rejected.', 'warning')
    return redirect(request.referrer or url_for('admin_dashboard'))


@app.route('/admin/toggle-claimed/<item_id>')
@admin_required
def toggle_claimed(item_id):
    item = mongo.db.items.find_one({'_id': ObjectId(item_id)})
    if item:
        new_claimed = not item.get('claimed', False)
        mongo.db.items.update_one({'_id': ObjectId(item_id)}, {'$set': {'claimed': new_claimed}})
    return redirect(request.referrer or url_for('admin_dashboard'))


@app.route('/admin/delete/<item_id>')
@admin_required
def admin_delete_item(item_id):
    mongo.db.items.delete_one({'_id': ObjectId(item_id)})
    flash('Item permanently deleted.', 'danger')
    return redirect(request.referrer or url_for('admin_dashboard'))


@app.route('/admin/edit/<item_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_item(item_id):
    item = mongo.db.items.find_one({'_id': ObjectId(item_id)})
    if not item:
        flash('Item not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        updates = {
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'location': request.form.get('location', '').strip(),
            'category': request.form.get('category', 'Other'),
            'item_type': request.form.get('item_type', 'found'),
            'date_found': request.form.get('date_found', ''),
            'status': request.form.get('status', 'pending'),
        }
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                updates['image'] = unique_filename

        mongo.db.items.update_one({'_id': ObjectId(item_id)}, {'$set': updates})
        flash('Item updated.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_edit.html', item=item)


@app.route('/admin/create', methods=['GET', 'POST'])
@admin_required
def admin_create_item():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        location = request.form.get('location', '').strip()

        if not title or not location:
            flash('Title and location are required.', 'danger')
            return redirect(url_for('admin_create_item'))

        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                image_filename = unique_filename

        mongo.db.items.insert_one({
            'title': title,
            'description': request.form.get('description', '').strip(),
            'location': location,
            'category': request.form.get('category', 'Other'),
            'item_type': request.form.get('item_type', 'found'),
            'date_found': request.form.get('date_found', ''),
            'image': image_filename,
            'status': request.form.get('status', 'approved'),
            'claimed': False,
            'submitted_by': session['user_id'],
            'submitted_by_name': f"Admin ({session['username']})",
            'created_at': datetime.utcnow()
        })
        flash('Item created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_create.html')


@app.route('/admin/users')
@admin_required
def admin_users():
    users = list(mongo.db.users.find({}, {'password': 0}).sort('created_at', -1))
    return render_template('admin_users.html', users=users)


@app.route('/admin/users/delete/<user_id>')
@admin_required
def admin_delete_user(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user and not user.get('is_admin'):
        mongo.db.users.delete_one({'_id': ObjectId(user_id)})
        flash('User deleted.', 'warning')
    else:
        flash('Cannot delete admin users.', 'danger')
    return redirect(url_for('admin_users'))


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        seed_admin()
    app.run(host='0.0.0.0', port=5000, debug=True)
