from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import sqlite3
from functools import wraps
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'failures'  # Used to sign session cookies

# ------------------ Cookie and Session Settings ------------------
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,       # Prevent JavaScript access
    SESSION_COOKIE_SECURE=False,        # Set to True in production (HTTPS only)
    SESSION_COOKIE_SAMESITE='Lax',      # Controls cross-site sending of cookies
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)  # Auto-expiry
)

# ------------------ Database setup ------------------
def init_db():
    with sqlite3.connect('reviews.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS reviews
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        review TEXT NOT NULL,
                        rating INTEGER NOT NULL,
                        user_id INTEGER NOT NULL)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL)''')
        conn.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)',
                     ('admin', 'password'))

# ------------------ Login required decorator ------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ------------------ Review Form ------------------
class ReviewForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit')

# ------------------ Routes ------------------
@app.route('/')
@login_required
def home():
    try:
        with sqlite3.connect('reviews.db') as conn:
            reviews = conn.execute('SELECT * FROM reviews WHERE user_id = ?',
                                   (session['user_id'],)).fetchall()
        return render_template('home.html', reviews=reviews)
    except Exception as e:
        flash(f'Error fetching reviews: {str(e)}', 'error')
        return render_template('error.html', message='Error fetching reviews')

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        try:
            with sqlite3.connect('reviews.db') as conn:
                conn.execute('INSERT INTO reviews (title, author, review, rating, user_id) VALUES (?, ?, ?, ?, ?)',
                             (form.title.data, form.author.data, form.review.data, form.rating.data, session['user_id']))
                conn.commit()
                flash('Review added successfully!', 'success')
                return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error adding review: {str(e)}', 'error')
    return render_template('review_form.html', form=form, action='Add')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_review(id):
    form = ReviewForm()
    try:
        with sqlite3.connect('reviews.db') as conn:
            review = conn.execute('SELECT * FROM reviews WHERE id = ? AND user_id = ?',
                                  (id, session['user_id'])).fetchone()
            if not review:
                flash('Review not found or unauthorized.', 'error')
                return redirect(url_for('home'))

            if form.validate_on_submit():
                conn.execute('UPDATE reviews SET title = ?, author = ?, review = ?, rating = ? WHERE id = ?',
                             (form.title.data, form.author.data, form.review.data, form.rating.data, id))
                conn.commit()
                flash('Review updated successfully!', 'success')
                return redirect(url_for('home'))

            form.title.data = review[1]
            form.author.data = review[2]
            form.review.data = review[3]
            form.rating.data = review[4]
    except Exception as e:
        flash(f'Error editing review: {str(e)}', 'error')
    return render_template('review_form.html', form=form, action='Edit')

@app.route('/delete/<int:id>')
@login_required
def delete_review(id):
    try:
        with sqlite3.connect('reviews.db') as conn:
            conn.execute('DELETE FROM reviews WHERE id = ? AND user_id = ?', (id, session['user_id']))
            conn.commit()
            flash('Review deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting review: {str(e)}', 'error')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with sqlite3.connect('reviews.db') as conn:
                user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                                    (username, password)).fetchone()
                if user:
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    session.permanent = True  # Activates cookie expiration timer
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid credentials.', 'error')
        except Exception as e:
            flash(f'Error during login: {str(e)}', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/session-info')
@login_required
def session_info():
    return f"Session contents: {dict(session)}"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message='Page not found'), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
