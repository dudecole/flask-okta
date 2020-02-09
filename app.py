from flask import Flask, render_template, request, redirect, g, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_oidc import OpenIDConnect
from okta import UsersClient, UserGroupsClient
from okta.framework import ApiClient

import pprint as p

app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/authorization-code/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "{{ LONG_RANDOM_STRING }}"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
okta_org_url = "{{ okta_org_url }}"
okta_auth_token = "{{ okta_auth_toke }}"

oidc = OpenIDConnect(app)
db = SQLAlchemy(app)
okta_user_client = UsersClient(okta_org_url,
                          okta_auth_token)
okta_group_client = UserGroupsClient(okta_org_url,
                          okta_auth_token)


user_groups = [
    {'okta':[
        'okta_add_app',
        'okta_aws_console',
        'another_test'
    ]},
    {'teams':[
        'onboard',
        'add_channel'
    ]},
]


class RecentTasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(50), nullable=False)
    task_details = db.Column(db.String(500), nullable=True)
    task_stage = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_user_client.get_user(oidc.user_getfield("sub"))
        # g.group = okta_group_client.get_groups()
    else:
        g.user = None

        # member_groups = okta_group_client.get_groups(query="okta")
        # print(member_groups)
        # for group in member_groups:
        #     print(group.__dict__)
        #     print(type(group.links.id))


        # for group in g.group:
        #     print("group_name: {}:".format(group.profile.name))
        #     member_group = okta_group_client.get_groups(query=group.profile.name)
        #     p.pprint(type(member_group[0].__dict__))



@app.route("/")
def index():
    return render_template('index.html',
                           title="Automation Dashboard",
                           okta_user=['Okta', 'Teams', 'Others'])


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
        task_url = request.form['url']
        app_name = request.form['app_name']
        redirect_url = request.form['redirect_url']
        task_details = "task_url: {}; " \
                       "app_name: {}; " \
                       "redirect_url: {}; ".format(task_url,
                                                   app_name,
                                                   redirect_url)

        new_task = RecentTasks(product=title,
                               task_details=task_details,
                               task_stage='Submitted')
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/okta_add_app')

        except:
            return "There was an issue adding your url"
    else:
        tasks = RecentTasks.query.order_by(RecentTasks.date_created).all()
        return render_template("okta_add_app.html",
                               title=title,
                               tasks=tasks,
                               text="some text .. its just for fun")


@app.route('/okta', methods=['GET'])
@oidc.require_login
def okta():
    tasks = RecentTasks.query.order_by(RecentTasks.date_created).all()
    return render_template("okta.html",
                           title="Okta",
                           tasks=tasks,
                           user_groups=user_groups)


@app.route('/teams')
@oidc.require_login
def teams():
    return "teams web page"


@app.route('/others')
@oidc.require_login
def others():
    return "others web page..  uhh.."


if __name__ == '__main__':
    app.run(debug=True)