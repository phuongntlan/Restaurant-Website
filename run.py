from restaurant import app
from restaurant.admin_routes import admin_bp

#checks if main.py has executed directly and not imported
if __name__ == '__main__':
    app.register_blueprint(admin_bp)
    app.run(debug = True)



