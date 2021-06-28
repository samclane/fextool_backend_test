from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

def search_phone_book(**kwargs):
    search_first_name = kwargs.get("first_name")
    search_last_name = kwargs.get("last_name")
    search_state = kwargs.get("state")

    results = []

    with open("data/phonebook.csv") as phonebook: 
        phonebook_csv_reader = csv.reader(phonebook)

        for row in phonebook_csv_reader:
            first_name, last_name, state, phonenumber = row

            if search_first_name and first_name != search_first_name:
                continue

            if search_last_name and last_name != search_last_name:
                continue

            if search_state and state != search_state:
                continue

            row_to_search_match_dict = {
                "first_name": first_name,
                "last_name": last_name,
                "state": state,
                "phonenumber": phonenumber
            }

            results.append(row_to_search_match_dict)

    return results

@app.route("/search/", methods=['GET'])
def search_phonebook():
    first_name = request.args.get("firstName")
    last_name = request.args.get("lastName")
    state = request.args.get("state")

    if not any([first_name, last_name, state]):
        return jsonify({"error": "At least one of the three fields must be filled."}), 400

    search_results = search_phone_book(
        first_name=first_name, 
        last_name=last_name, 
        state=state
    )

    return jsonify(search_results)

if __name__ == "__main__":
    app.run(debug=True, port=8080, threaded=True)
