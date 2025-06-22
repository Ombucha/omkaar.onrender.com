from flask import Flask, render_template_string, request
import gocomics
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/comics', methods=['GET'])
@app.route('/comics/', methods=['GET'])
def comics_page():
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
        <style>
            body { font-family: Arial, sans-serif; margin: 2em; }
            label { display: block; margin-top: 1em; }
            select, input[type=date] { font-size: 1em; padding: 0.2em; }
        </style>
    </head>
    <body>
        <h2>Comics Viewer</h2>
        <form method="get">
            <label for="date">Select Date:</label>
            <input type="date" id="date" name="date" value="{{ selected_date or '' }}" required>
            <label for="comic">Select Comic:</label>
            <select id="comic" name="comic" required>
                {% for comic in comics %}
                <option value="{{ comic }}" {% if comic == selected_comic %}selected{% endif %}>{{ comic }}</option>
                {% endfor %}
            </select>
            <br><br>
            <button type="submit">Show Comic</button>
        </form>
        <div style="margin-top:2em;">
            {% if comic_img_html %}{{ comic_img_html|safe }}{% endif %}
            {% if error %}<div style="color:red;">{{ error }}</div>{% endif %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, comics=comics, selected_comic=selected_comic, selected_date=selected_date, comic_img_html=comic_img_html, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
