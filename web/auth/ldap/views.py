from flask import Blueprint, render_template, request, redirect, flash
from flask_login import logout_user

from web.views.helpers import prevent_csrf
from web.auth.ldap.user_management import authenticate

from ldap import SERVER_DOWN, INVALID_CREDENTIALS


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
@prevent_csrf
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        try:
            user = authenticate(request.form.get('email'), request.form.get('password'))
        except SERVER_DOWN:
            flash("LDAP Server down.", "danger")
            return render_template('login.html')
        except INVALID_CREDENTIALS:
            flash("Invalid credentials.", "danger")
            return render_template('login.html')

        if not user:
            flash("Access not allowed.", "danger")
            return render_template('login.html')

        redir = request.args.get('next', '/')
        return redirect(redir)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
