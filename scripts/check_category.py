from app.db import SessionLocal
from app import models
from sqlalchemy import func

db = SessionLocal()
qs = db.query(models.Product)
print('distinct', [r[0] for r in db.query(models.Product.category).distinct().all()])
print('total', qs.count())
q1 = qs.filter(func.lower(models.Product.category) == 'books')
print('lower==books count', q1.count())
print('q1 sql', str(q1.statement))
q2 = qs.filter(models.Product.category.ilike('books'))
print('ilike books count', q2.count())
print('q2 sql', str(q2.statement))
q3 = qs.filter(models.Product.category.ilike('%books%'))
print('ilike %books% count', q3.count())
print('q3 sql', str(q3.statement))

# Also try a parameterized check using Python lowercase on the bound param
category_param = 'books'
q4 = qs.filter(func.lower(models.Product.category) == category_param.lower())
print('lower with param count', q4.count())
print('q4 sql', str(q4.statement))

# Show rows and repr
print('rows for q3:', [r.name for r in q3.all()])
print('rows for q1:', [r.name for r in q1.all()])
print('rows for q2:', [r.name for r in q2.all()])
