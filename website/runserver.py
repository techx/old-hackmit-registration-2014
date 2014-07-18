from application import app, db

with app.app_context():
    db.create_all()
port = app.config['PORT']
if not port:
    port = 5000 # Default
debug = app.config['DEBUG']
if not debug:
    print 'NOT DEBUG'
app.run(port=port, debug=debug)
