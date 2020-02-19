from flask import render_template, request, redirect, g, url_for
from config import BaseConfig
from flask_oidc import OpenIDConnect
from okta import UsersClient
import json
from models import db, RecentTasks
from __init__ import app


oidc = OpenIDConnect(app)
okta_user_client = UsersClient(BaseConfig.okta_org_url,
                               BaseConfig.okta_auth_token)


@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_user_client.get_user(oidc.user_getfield("sub"))
        g.username = g.oidc_id_token['preferred_username']
        g.groups = g.oidc_id_token['groups']
        g.group_list = base_groups(g.groups)

    else:
        g.user = None


def base_groups(user_groups):
    group_titles = []
    for group in user_groups:
        if group not in group_titles:
            group_titles.append((group.split('_')[0]).title())
    return group_titles


@app.route("/")
def index():
    return render_template('index.html',
                           title="Automation Dashboard")


@app.route("/dashboard")
@oidc.require_login
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".index"))


@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".index"))


@app.route('/okta_add_app', methods=['GET','POST'])
@oidc.require_login
def okta_add_app():
    title = "Okta Add Application"
    if request.method == 'POST':

        task_details = dict()
        task_details['app_url'] = request.form['url']
        task_details['app_name']= request.form['app_name']
        task_details['redirect_url'] = request.form['redirect_url']

        p.pprint(task_details)
        print(type(task_details))
        new_task = RecentTasks(product=title,
                               task_details=json.dumps(task_details),
                               task_requester=g.username,
                               task_stage='Submitted')
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/okta_add_app')

        except:
            return "There was an issue adding your url"
        # .order_by(MyEntity.my_date.desc()).limit(3).all()
    else:
        tasks = RecentTasks.query.order_by(RecentTasks.date_created.desc()).limit(5).all()
        return render_template("okta_add_app.html",
                               title=title,
                               tasks=tasks,
                               text="some text .. its just for fun")


@app.route('/tasks/<int:id>', methods=['GET'])
@oidc.require_login
def tasks(id):
    # single_task = RecentTasks.query.order_by(RecentTasks.date_created).all()
    return "here is the single record {}".format(id) #`render_template("tasks.html",
                           #title="Tasks",
                           #tasks=single_task)


@app.route('/okta', methods=['GET'])
@oidc.require_login
def okta():
    tasks = RecentTasks.query.order_by(RecentTasks.date_created).all()
    return render_template("okta.html",
                           title="Okta",
                           tasks=tasks,
                           user_groups=g.groups)


@app.route('/teams')
@oidc.require_login
def teams():
    return "teams web page"


@app.route('/others')
@oidc.require_login
def others():
    return "others web page..  uhh.."


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)