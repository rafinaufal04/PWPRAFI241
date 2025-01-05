from app import app
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

def check_user_data():
    with app.app_context():
        # Cek semua user yang ada
        print("\nDaftar semua user:")
        users = User.query.all()
        for user in users:
            print(f"\nUsername: {user.username}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print(f"Password Hash: {user.password_hash}")

def test_specific_user(username, test_password):
    with app.app_context():
        print(f"\nMencoba login untuk user: {username}")
        user = User.query.filter_by(username=username).first()
        
        if user:
            print("User ditemukan!")
            print(f"Username: {user.username}")
            print(f"Password Hash: {user.password_hash}")
            
            # Test password
            is_valid = user.check_password(test_password)
            print(f"Hasil check password: {is_valid}")
        else:
            print(f"User dengan username {username} tidak ditemukan")

if __name__ == "__main__":
    # Tampilkan semua user
    check_user_data()
    
    # Test user spesifik
    username = input("\nMasukkan username yang ingin dicek: ")
    password = input("Masukkan password untuk dicek: ")
    test_specific_user(username, password) 