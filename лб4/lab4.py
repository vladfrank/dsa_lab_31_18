from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'secret-fbi31'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# словарь с данными клиентов
users = {}
next_id = 1

# модель User 
class User(UserMixin):
    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name


# загружаеи пользователя по ID 
@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id)) 


# корневая страница GET /
@app.route('/')
def index():
    # для авторизованных 
    if current_user.is_authenticated:
        return render_template('index.html')
    # для неавторизованных 
    return redirect(url_for('login'))


# страница входа GET /login
@app.route('/login')
def login():
    return render_template('login.html')


# авторизация POST /login
@app.route('/login', methods=['POST'])
def login_post():
    # получаем email и password из формы
    email = request.form.get('email')
    password = request.form.get('password')
    
    # поиск пользователя по почте
    user = None
    for u in users.values():
        if u.email == email:
            user = u
            break
    
    # если пользователь не найден ошибка
    if not user:
        flash('Пользователь не найден')
        return redirect(url_for('login'))
    
    # если пароль не совпадает ошибка
    if user.password != password:
        flash('Неверный пароль')
        return redirect(url_for('login'))
    
    # если все верно авторизуем и отправляем на корневую страницу
    login_user(user)
    return redirect(url_for('index'))


# страница регистрации GET /signup
@app.route('/signup')
def signup():
    return render_template('signup.html')

# регистрация POST /signup
@app.route('/signup', methods=['POST'])
def signup_post():
    global next_id
    
    # получаем имя, почту и пароль из формы
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # проверка на дублирование почты
    for u in users.values():
        if u.email == email:
            flash('Пользователь уже существует')
            return redirect(url_for('signup'))
    
    # "регистрация"
    users[next_id] = User(next_id, email, password, name)
    next_id += 1
    
    flash('Регистрация успешна')
    return redirect(url_for('login'))

# выход GET /logout
@app.route('/logout')
@login_required
def logout():
    # завершаем сессию
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)