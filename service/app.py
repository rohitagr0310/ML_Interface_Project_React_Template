from flask import Flask, request, jsonify, make_response
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class PredictionSchema(Schema):
    textField1 = fields.String(required=True)
    textField2 = fields.String(required=True)
    select1 = fields.Integer(required=True)
    select2 = fields.Integer(required=True)
    select3 = fields.Integer(required=True)

    def load_key_by_key(self, data):
        loaded_data = {}

        for key, field in self.fields.items():
            if key in data:
                try:
                    # Handle the conversion of string values to integers for integer fields
                    if isinstance(field, fields.Integer) and isinstance(data[key], str):
                        loaded_data[key] = field.deserialize(int(data[key]))
                    else:
                        loaded_data[key] = field.deserialize(data[key])
                except ValidationError as error:
                    raise ValidationError({key: error.messages})

        return loaded_data


@app.route("/prediction", methods=["OPTIONS"])
def options():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.route("/prediction/", methods=["POST"])
def make_prediction():
    json_data = request.get_json()
    print(json_data)
    schema = PredictionSchema()
    try:
        data = schema.load_key_by_key(json_data)

        # Perform prediction with 'data'

        response = jsonify(
            {
                "statusCode": 200,
                "status": "Prediction made",
                "result": "Prediction: " + str(data),
            }
        )
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except ValidationError as error:
        return jsonify(
            {
                "statusCode": 400,
                "status": "Bad Request",
                "error": str(error),
            }
        )
    except Exception as error:
        return jsonify(
            {
                "statusCode": 500,
                "status": "Could not make prediction",
                "error": str(error),
            }
        )


if __name__ == "__main__":
    app.run(debug=True)
