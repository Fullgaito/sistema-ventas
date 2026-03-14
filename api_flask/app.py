import models
import routes
routes.register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)