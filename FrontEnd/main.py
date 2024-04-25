from flask import escape, request, jsonify

def main(request):
    if request.method == 'POST':
        request_json = request.get_json(silent=True)
        age = request_json.get('age')
        gpa = request_json.get('gpa')

        # Process the data as needed
        response_data = {
            "message": "Data received successfully",
            "yourAge": age,
            "yourGPA": gpa
        }

        # Return a response
        return jsonify(response_data), 200

    else:
        return 'Only POST method is supported.', 405
