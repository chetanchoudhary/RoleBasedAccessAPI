from flask import Flask, url_for, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.sensor import SensorModel


class Sensor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "value", type=int, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self):
        return {"sensors": list(map(lambda x: x.json(), SensorModel.query.all()))}

    @jwt_required()
    def post(self):
        user = current_identity
        print(user.access)

        if user.access == "admin":
            data = Sensor.parser.parse_args()
            if SensorModel.find_by_name(data["name"]):
                return {
                    "message": "A sensor with name '{}' already exists.".format(
                        data["name"]
                    )
                }

            sensor = SensorModel(data["name"], data["value"])

            try:
                sensor.save_to_db()
            except:
                return {"message": "An error occurred inserting the item."}

            return sensor.json(), 201
        else:
            return {"message": "You do not have ADMIN Rights"}, 405


class SensorByName(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "value", type=int, required=True, help="This field cannot be left blank!"
    )

    TABLE_NAME = "sensors"

    @jwt_required()
    def get(self, name):
        sensor = SensorModel.find_by_name(name)
        if sensor:
            return sensor.json()
        return {"message": "Item not found"}, 404

    @jwt_required()
    def delete(self, name):
        user = current_identity
        print(user.access)

        if user.access == "admin":
            sensor = SensorModel.find_by_name(name)
            if sensor:
                sensor.delete_from_db()

            return {"message": "Sensor deleted"}
        else:
            return {"message": "You do not have ADMIN Rights"}, 405

    @jwt_required()
    def put(self, name):
        user = current_identity
        print(user.access)

        if user.access == "admin":
            data = SensorByName.parser.parse_args()
            sensor = SensorModel.find_by_name(name)

            if sensor is None:
                sensor = SensorModel(name, data["value"])
            else:
                sensor.value = data["value"]

            sensor.save_to_db()
            return sensor.json()

        else:
            return {"message": "You do not have ADMIN Rights."}, 405

