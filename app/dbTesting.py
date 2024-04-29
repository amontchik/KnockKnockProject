from app import __init__, models
from app.__init__ import app, db
from app.models import Posts

p = Posts(job = "driver")
#print(p)
#db.session.add(p)
#db.session.commit()

#postss = Posts.query.all()
#print(postss)