from app import app
import os


if __name__== '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, port=int((os.environ.get('PORT', 8080))))