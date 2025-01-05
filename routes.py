from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from controller.user import register_form, login_user
from extensions import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    if 'user_id' in session:
        return redirect(url_for('main.login'))
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.tampil_data'))
        
    if request.method == 'POST':
        user, message = register_form()
        if user:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash(message, 'danger')
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.tampil_data'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = login_user(username, password)
        
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Selamat datang kembali, {user.username}!', 'success')
            return redirect(url_for('main.tampil_data'))
        else:
            flash('Username atau password salah!', 'danger')
            
    return render_template('login.html')

@main.route('/tampil_data')
def tampil_data():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'warning')
        return redirect(url_for('main.login'))
    
    current_user = User.query.get(session['user_id'])
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '')
    
    # Jika role user, hanya tampilkan data user tersebut
    if current_user.role == 'user':
        users = User.query.filter_by(id=current_user.id)
    else:
        # Jika admin, tampilkan semua data dengan filter pencarian jika ada
        if query:
            users = User.query.filter(User.username.contains(query))
        else:
            users = User.query.order_by(User.username.asc())
    
    users_pagination = users.paginate(page=page, per_page=5)
    return render_template('tampil_data.html',
                        users_pagination=users_pagination,
                        query=query,
                        current_user=current_user)

@main.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'warning')
        return redirect(url_for('main.login'))
    
    current_user = User.query.get(session['user_id'])
    # Hanya admin yang bisa edit user lain, user biasa hanya bisa edit dirinya sendiri
    if current_user.role != 'admin' and current_user.id != user_id:
        flash('Anda tidak memiliki akses untuk mengedit user ini!', 'danger')
        return redirect(url_for('main.tampil_data'))
        
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        try:
            user.username = request.form['username']
            user.email = request.form['email']
            
            # Hanya admin yang bisa mengubah role
            if current_user.role == 'admin':
                user.role = request.form['role']
            
            # Update password jika diisi
            if request.form.get('password'):
                user.set_password(request.form['password'])
            
            db.session.commit()
            flash('Data user berhasil diupdate!', 'success')
            return redirect(url_for('main.tampil_data'))
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan! Silakan coba lagi.', 'danger')
            print(f"Error: {str(e)}")  # Untuk debugging
            
    return render_template('edit_user.html', user=user, current_user=current_user)

@main.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'warning')
        return redirect(url_for('main.login'))
    
    current_user = User.query.get(session['user_id'])
    # Hanya admin yang bisa menghapus user
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses untuk menghapus user!', 'danger')
        return redirect(url_for('main.tampil_data'))
        
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Terjadi kesalahan! Silakan coba lagi.', 'danger')
        print(f"Error: {str(e)}")  # Untuk debugging
        
    return redirect(url_for('main.tampil_data'))

@main.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Anda telah berhasil logout!', 'success')
    return redirect(url_for('main.login'))

# Helper function untuk mengecek role admin
def is_admin():
    if 'user_id' not in session:
        return False
    user = User.query.get(session['user_id'])
    return user and user.role == 'admin'