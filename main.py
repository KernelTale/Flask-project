from flask import Flask, render_template, redirect, url_for
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_cut-off.db'
db = SQLAlchemy(app)

# BBBBxNNxHH:MM:SS.zhqxGGCR

resource_fields = {
    'id': fields.Integer,
    'member': fields.String,
    'channel': fields.String,
    'time': fields.String,
    'group': fields.String
}

class CutOffModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.String(4), nullable=False)
    channel = db.Column(db.String(2), nullable=False)
    time = db.Column(db.String, nullable=True)
    group = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return f"CutOff(id: {id}, member: {member}, channel: {channel}, time: {time}, group: {group})"

cutoff_put_args = reqparse.RequestParser()
cutoff_put_args.add_argument("member", type=str, help="Member is required", required=True)
cutoff_put_args.add_argument("channel", type=str, help="Channel")
cutoff_put_args.add_argument("time", type=str, help="Time of the cut-off")
cutoff_put_args.add_argument("group", type=str, help="Group")

cutoff_update_args = reqparse.RequestParser()
cutoff_update_args.add_argument("member", type=str, help="Member")
cutoff_update_args.add_argument("channel", type=str, help="Channel")
cutoff_update_args.add_argument("time", type=str, help="Time of the cut-off")
cutoff_update_args.add_argument("group", type=str, help="Group")

class CutOff(Resource):
    @marshal_with(resource_fields)
    def get(self, note_id):
        result = CutOffModel.query.filter_by(id=note_id).first()
        if not result:
            abort(404, message="Could not find note with that ID")
        return result
    
    @marshal_with(resource_fields)
    def put(self, note_id):
        args = cutoff_put_args.parse_args()
        result = CutOffModel.query.filter_by(id=note_id).first()
        if result:
            abort(409, message="Note ID taken...")
            
        note = CutOffModel(id=note_id, member=args['member'], channel=args['channel'], time=args['time'], group=args['group'])
        db.session.add(note)
        db.session.commit()
        return note, 201

    @marshal_with(resource_fields)
    def patch(self, note_id):
        args = cutoff_update_args.parse_args()
        result = CutOffModel.query.filter_by(id=note_id).first()

        if not result:
            abort(404, message="Note doesn't exist, cannot update")

        if args['member']:
            result.member = args['member']
        if args['channel']:
            result.channel = args['channel']
        if args['time']:
            result.time = args['time']
        if args['group']:
            result.group = args['group']
        
        db.session.commit()

        return result

    def delete(self, note_id):
        return '', 204

db.create_all()
api.add_resource(CutOff, "/cutoff/<int:note_id>")

@app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html", values=CutOffModel.query.all())

if __name__ == "__main__":
    app.run(debug=True)