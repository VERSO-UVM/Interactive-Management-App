from flask import request as __request

def insert_factor(r: __request) -> None:
    idea = r.form['idea']
        clarification = r.form['clarification']
        label = r.form['label']
        category = r.form['category']

        new_factor = Factor(
            idea=idea, clarification=clarification, label=label, category=category)
        factors.append(new_factor)

def update_factor() -> None:
    factor = next((f for f in factors if f.id == id), None)
    if factor is None:
        return "Factor not found", 404

    if request.method == 'POST':
        factor.idea = request.form['idea']
        factor.clarification = request.form['clarification']
        factor.label = request.form['label']
        factor.category = request.form['category']
        factor.updated_at = datetime.utcnow()

        return redirect(url_for('index'))

    return render_template('edit_factor.html', factor=factor, categories=categories)

def delete_factor() -> None:
    pass
