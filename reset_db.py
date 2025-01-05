from app import app, db

def reset_database():
    with app.app_context():
        print("Menghapus database lama...")
        db.drop_all()
        
        print("Membuat database baru...")
        db.create_all()
        
        print("Database berhasil direset!")

if __name__ == "__main__":
    reset_database()