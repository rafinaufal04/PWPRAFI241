from flask import request
from models.user import User
from extensions import db

def register_form():
    try:
        username = request.form['username']
        role = request.form['role']
        email = request.form.get('email')
        password = request.form['password']
        
        # Debug print
        print(f"Mencoba registrasi user baru:")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Role: {role}")
        
        # Buat user baru
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        # Debug print
        print(f"Password hash yang dibuat: {user.password}")
        
        db.session.add(user)
        db.session.commit()
        
        print("User berhasil didaftarkan!")
        return user, "Success"
        
    except Exception as e:
        db.session.rollback()
        print(f"Error saat registrasi: {str(e)}")
        return None, str(e)

def login_user(username, password):
    try:
        user = User.query.filter_by(username=username).first()
        
        # Debug print
        print(f"\nMencoba login user:")
        print(f"Username yang dicari: {username}")
        print(f"User ditemukan: {user is not None}")
        
        if user:
            print(f"Password hash di database: {user.password}")
            is_valid = user.check_password(password)
            print(f"Hasil pengecekan password: {is_valid}")
            
            if is_valid:
                return user
                
        return None
        
    except Exception as e:
        print(f"Error saat login: {str(e)}")
        return None