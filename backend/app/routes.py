

def register_routes(app):
    app.register_blueprint(v1, url_prefix='/api/v1')