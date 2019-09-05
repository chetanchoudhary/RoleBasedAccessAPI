from flask import jsonify
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserGetPost(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "access", type=str, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self):
        user = current_identity
        print(user.access)

        if user.access == "admin":
            # return {"users": list(map(lambda x: x.json(), UserModel.query.all()))}
            return {"users": [user.json() for user in UserModel.query.all()]}

        else:
            return {"message": "You do not have ADMIN Rights."}, 405

    def post(self):
        data = UserGetPost.parser.parse_args()
        if UserModel.find_by_email(data["email"]):
            return {"message": "User with this email already exists."}, 400

        user = UserModel(data["email"], data["password"], data["access"])
        user.save_to_db()

        return {"message": "A new User has been Created Succesfully"}, 201

