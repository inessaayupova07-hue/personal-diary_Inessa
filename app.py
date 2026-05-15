from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

DATA_FILE = 'entries.json'

def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_entries(entries):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

entries = load_entries()

@app.route('/')
def index():
    return render_template('index.html', entries=entries)

@app.route('/entry/<int:entry_id>')
def detail(entry_id):
    if 0 <= entry_id < len(entries):
        return render_template('detail.html', entry=entries[entry_id], entry_id=entry_id)
    return "Запись не найдена", 404

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d %H:%M')
        entries.append({'title': title, 'content': content, 'date': date})
        save_entries(entries)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    if request.method == 'POST':
        entries[entry_id]['title'] = request.form['title']
        entries[entry_id]['content'] = request.form['content']
        save_entries(entries)
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entries[entry_id], entry_id=entry_id)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entries.pop(entry_id)
    save_entries(entries)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    filtered = [e for e in entries if query in e['title'].lower()] if query else entries
    return render_template('index.html', entries=filtered)
@app.route('/filter/week')
def filter_week():
    week_ago = datetime.now() - timedelta(days=7)
    filtered = []
    for e in entries:
        try:
            entry_date = datetime.strptime(e['date'], '%Y-%m-%d %H:%M')
            if entry_date >= week_ago:
                filtered.append(e)
        except:
            pass
    return render_template('index.html', entries=filtered)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)