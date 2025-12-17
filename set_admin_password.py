from django.contrib.auth.models import User
u = User.objects.get(username='admin')
u.set_password('Admin123456')
u.save()
print('Contraseña del admin establecida: Admin123456')
