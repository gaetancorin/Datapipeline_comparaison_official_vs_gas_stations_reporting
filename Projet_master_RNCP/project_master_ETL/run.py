from App.views import app
from App.views import scheduler

if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', debug=True)