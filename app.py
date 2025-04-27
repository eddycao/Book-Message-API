from flask import Flask
from controllers.book_controller import book_bp
from controllers.message_controller import message_bp

app = Flask(__name__)


app.register_blueprint(book_bp)
app.register_blueprint(message_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
