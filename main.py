from flask import Flask, render_template_string, request, redirect, url_for, session
import gocomics
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
PASSWORD = os.environ.get('PASSWORD', '1234')

@app.route('/comics', methods=['GET', 'POST'])
def comics_page():
    if 'authenticated' not in session:
        if request.method == 'POST':
            if request.form.get('password') == PASSWORD:
                session['authenticated'] = True
                return redirect(url_for('comics_page'))
            else:
                error = 'Incorrect password.'
                return render_template_string('''
                <form method="post" style="max-width:340px;margin:5em auto;padding:2em 2em 1.5em 2em;background:#fff;border-radius:12px;box-shadow:0 4px 24px #ff7e5f22;text-align:center;">
                    <h2 style="color:#ff7e5f;">Enter Password</h2>
                    <input type="password" name="password" placeholder="Password" style="width:100%;padding:0.7em 1em;margin-bottom:1em;border-radius:8px;border:1.5px solid #ff7e5f;font-size:1.1em;" required>
                    <button type="submit" style="background:linear-gradient(90deg,#ff7e5f 0%,#feb47b 100%);color:#fff;font-size:1.1em;font-weight:700;border:none;border-radius:8px;padding:0.7em 0;width:100%;cursor:pointer;">Login</button>
                    <div style="color:#d7263d;margin-top:1em;">{{error}}</div>
                </form>
                ''', error=error)
        return render_template_string('''
        <form method="post" style="max-width:340px;margin:5em auto;padding:2em 2em 1.5em 2em;background:#fff;border-radius:12px;box-shadow:0 4px 24px #ff7e5f22;text-align:center;">
            <h2 style="color:#ff7e5f;">Enter Password</h2>
            <input type="password" name="password" placeholder="Password" style="width:100%;padding:0.7em 1em;margin-bottom:1em;border-radius:8px;border:1.5px solid #ff7e5f;font-size:1.1em;" required>
            <button type="submit" style="background:linear-gradient(90deg,#ff7e5f 0%,#feb47b 100%);color:#fff;font-size:1.1em;font-weight:700;border:none;border-radius:8px;padding:0.7em 0;width:100%;cursor:pointer;">Login</button>
        </form>
        ''')
    comics = gocomics.search()
    selected_comic = request.args.get('comic')
    selected_date = request.args.get('date')
    comic_img_html = ''
    error = ''
    if selected_comic and selected_date:
        try:
            dt = datetime.strptime(selected_date, '%Y-%m-%d').date()
            comic = gocomics.Comic(selected_comic, dt)
            if comic.image_url:
                comic_img_html = f'<h3>Result:</h3><img src="{comic.image_url}" alt="{selected_comic}" style="max-width:100%;height:auto;">'
            else:
                error = 'Comic not found.'
        except Exception as e:
            error = f'Error: {str(e)}'
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Comics Viewer</title>
        <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" />
        <style>
            html, body { height: 100%; margin: 0; padding: 0; }
            body {
                font-family: 'Roboto', Arial, sans-serif;
                min-height: 100vh;
                background: linear-gradient(120deg, #ffecd2 0%, #fcb69f 100%);
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: rgba(255,255,255,0.92);
                max-width: 420px;
                width: 100%;
                border-radius: 18px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.18);
                padding: 2.5em 2em 2em 2em;
                margin: 2em auto;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            h2 {
                text-align: center;
                color: #ff7e5f;
                margin-bottom: 1.5em;
                letter-spacing: 1px;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 1.2em;
                width: 100%;
            }
            label {
                font-weight: 700;
                color: #333;
                margin-bottom: 0.3em;
            }
            input[type="date"], select {
                font-size: 1.1em;
                padding: 0.7em 1em;
                border-radius: 10px;
                border: 1.5px solid #ff7e5f;
                width: 100%;
                box-sizing: border-box;
                margin-bottom: 0.5em;
                background: #fff8f3;
                transition: border 0.2s, box-shadow 0.2s, background 0.2s;
                box-shadow: 0 2px 8px rgba(255,126,95,0.07);
                outline: none;
            }
            input[type="date"]:focus, select:focus {
                border: 2px solid #feb47b;
                background: #fff3e6;
                box-shadow: 0 4px 16px #ffecd2aa;
            }
            button {
                background: linear-gradient(90deg, #ff7e5f 0%, #feb47b 100%);
                color: #fff;
                font-size: 1.1em;
                font-weight: 700;
                border: none;
                border-radius: 8px;
                padding: 0.7em 0;
                cursor: pointer;
                box-shadow: 0 2px 8px rgba(255,126,95,0.08);
                transition: background 0.2s, transform 0.1s, color 0.2s;
                margin-top: 1em;
            }
            button:hover {
                background: linear-gradient(90deg, #feb47b 0%, #ff7e5f 100%);
                transform: scale(1.04);
                color: #fff;
            }
            .result {
                margin-top: 2em;
                min-height: 120px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            .result img {
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.10);
                max-width: 100%;
                max-height: 400px;
                background: #f9f9f9;
                padding: 1em;
                animation: fadeIn 0.7s;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 0 0 0.15em; /* Move image just a little to the left */
            }
            .error {
                color: #d7263d;
                font-weight: 700;
                margin-top: 1em;
                text-align: center;
            }
            .fa-calendar-days, .fa-book-open {
                color: #ff7e5f;
                margin-right: 0.5em;
            }
            .loader {
                display: none;
                margin: 0 auto;
                text-align: center;
            }
            .fa-spinner {
                font-size: 2em;
                color: #ff7e5f;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: scale(0.97);} to { opacity: 1; transform: scale(1);}
            }
            .select2-container--default .select2-selection--single {
                height: 44px;
                border-radius: 10px;
                border: 1.5px solid #ff7e5f;
                font-size: 1.1em;
                padding: 0.2em 1em;
                background: #fff8f3 !important;
                box-shadow: 0 2px 8px rgba(255,126,95,0.07);
                color: #222;
                transition: background 0.2s, border 0.2s;
                position: relative;
                padding-right: 2.7em !important; /* More space for clear button and arrow */
            }
            .select2-container {
                position: relative;
            }
            .select2-selection__rendered {
                line-height: 44px !important;
                font-weight: 500;
                letter-spacing: 0.5px;
                color: #222 !important;
                position: relative;
                padding-right: 2.7em !important; /* More space for clear button and arrow */
            }
            .select2-selection__arrow {
                z-index: 10;
                right: 0.7em !important;
            }
            .select2-container--default .select2-selection--single:focus, .select2-container--default .select2-selection--single:active {
                border: 2px solid #feb47b; outline: none;
                box-shadow: 0 0 0 2px #ffecd2aa;
            }
            .select2-dropdown {
                border-radius: 10px;
                border: 1.5px solid #ff7e5f;
                box-shadow: 0 4px 24px #ff7e5f22;
                background: #fff8f3 !important;
            }
            .select2-results__option {
                border-radius: 8px;
                margin: 2px 4px;
                padding: 0.7em 1em;
                font-size: 1.05em;
                transition: background 0.3s, color 0.3s;
            }
            .select2-results__option--highlighted {
                background: #ffecd2 !important;
                color: #d7263d !important;
                font-weight: 700;
            }
            .select2-results__option--selected {
                background: #feb47b !important;
                color: #fff !important;
                font-weight: 700;
            }
            .select2-selection__clear {
                font-size: 1.2em !important;
                color: #fff !important;
                background: linear-gradient(135deg, #ff7e5f 60%, #feb47b 100%);
                border-radius: 50%;
                width: 20px;
                height: 20px;
                display: flex !important;
                align-items: center;
                justify-content: center;
                position: absolute !important;
                right: 1.1em !important;
                top: 5% !important; /* Move cross just a little up */
                transform: translateY(-50%);
                z-index: 30;
                pointer-events: auto;
                box-shadow: 0 2px 8px rgba(255,126,95,0.15);
                opacity: 0.92;
                border: 2px solid #fff2;
                transition: background 0.2s, color 0.2s, box-shadow 0.2s, opacity 0.2s;
                cursor: pointer;
                padding: 0 !important;
            }
            .select2-selection__clear::before {
                content: '';
                display: block;
                width: 14px;
                height: 14px;
                background: url('data:image/svg+xml;utf8,<svg fill="white" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 8.586l4.95-4.95 1.414 1.414-4.95 4.95 4.95 4.95-1.414 1.414-4.95-4.95-4.95 4.95-1.414-1.414 4.95-4.95-4.95-4.95L5.05 3.636z"/></svg>') no-repeat center center;
                background-size: 14px 14px;
                margin: auto;
            }
            .select2-selection__clear > span { display: none; }
        </style>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                var correct = false;
                while (!correct) {
                    var pwd = prompt('Enter password to access the site:');
                    if (pwd === "1234") {
                        correct = true;
                    } else {
                        alert('Incorrect password!');
                    }
                }
                var form = document.querySelector('form');
                var btn = form.querySelector('button[type="submit"]');
                var loader = document.querySelector('.loader');
                form.addEventListener('submit', function() {
                    btn.style.display = 'none';
                    loader.style.display = 'block';
                });
                // Enable search in select
                $("#comic").select2({
                    width: '100%',
                    placeholder: 'Select or search for a comic',
                    allowClear: true,
                    dropdownAutoWidth: true
                });
            });
        </script>
    </head>
    <body>
        <div class="container">
            <h2><i class="fa-solid fa-book-open"></i> Comics Viewer</h2>
            <form method="get">
                <label for="date"><i class="fa-solid fa-calendar-days"></i> Select Date:</label>
                <input type="date" id="date" name="date" value="{{ selected_date or '' }}" required>
                <label for="comic"><i class="fa-solid fa-book-open"></i> Select Comic:</label>
                <select id="comic" name="comic" required>
                    {% for comic in comics %}
                    <option value="{{ comic }}" {% if comic == selected_comic %}selected{% endif %}>{{ comic }}</option>
                    {% endfor %}
                </select>
                <button type="submit"><i class="fa-solid fa-eye"></i> Show Comic</button>
                <div class="loader"><i class="fa-solid fa-spinner"></i></div>
            </form>
            <div class="result">
                {% if comic_img_html %}{{ comic_img_html|safe }}{% endif %}
                {% if error %}<div class="error">{{ error }}</div>{% endif %}
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, comics=comics, selected_comic=selected_comic, selected_date=selected_date, comic_img_html=comic_img_html, error=error)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Welcome to Comics Viewer</title>
        <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <style>
            html, body { height: 100%; margin: 0; padding: 0; }
            body {
                font-family: 'Roboto', Arial, sans-serif;
                min-height: 100vh;
                background: linear-gradient(120deg, #ffecd2 0%, #fcb69f 100%);
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .home-container {
                background: rgba(255,255,255,0.95);
                max-width: 420px;
                width: 100%;
                border-radius: 18px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.18);
                padding: 2.5em 2em 2em 2em;
                margin: 2em auto;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            h1 {
                text-align: center;
                color: #ff7e5f;
                margin-bottom: 0.7em;
                letter-spacing: 1px;
                font-size: 2.1em;
            }
            p {
                color: #333;
                font-size: 1.15em;
                text-align: center;
                margin-bottom: 2em;
            }
            a.button {
                display: inline-block;
                background: linear-gradient(90deg, #ff7e5f 0%, #feb47b 100%);
                color: #fff;
                font-size: 1.1em;
                font-weight: 700;
                border: none;
                border-radius: 8px;
                padding: 0.8em 2.2em;
                cursor: pointer;
                box-shadow: 0 2px 8px rgba(255,126,95,0.08);
                transition: background 0.2s, transform 0.1s, color 0.2s;
                text-decoration: none;
            }
            a.button:hover {
                background: linear-gradient(90deg, #feb47b 0%, #ff7e5f 100%);
                color: #fff;
                transform: scale(1.04);
            }
            .fa-book-open {
                color: #ff7e5f;
                margin-right: 0.5em;
            }
        </style>
    </head>
    <body>
        <div class="home-container">
            <h1><i class="fa-solid fa-book-open"></i> Comics Viewer</h1>
            <p>Welcome! Explore your favorite comics by date and name with a beautiful, modern interface.<br><br>
            Click below to get started.</p>
            <a href="/comics" class="button"><i class="fa-solid fa-eye"></i> View Comics</a>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
