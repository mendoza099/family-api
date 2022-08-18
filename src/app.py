import os, json
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({
"first_name":"John",
"id": 1,
"lucky_numbers":[7, 13, 22]
})
jackson_family.add_member({
"first_name":"Jane",
"id":2,
"lucky_numbers":[10, 14, 3]
})
jackson_family.add_member({
"first_name":"Jimmy",
"id":3,
"lucky_numbers":[1]
})



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_all():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def handle_get_one(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({}), 404
    
    return jsonify(member), 200
# this only runs if `$ python src/app.py` is executed

@app.route('/member/<int:id>', methods=['DELETE'])
def handle_delete_one(id):
    member = jackson_family.delete_member(id)
    if member:
        return jsonify({
            'done': True
        }), 200     
    
    return jsonify({}), 404
     # hay que hacer el request body como el ejercicio poniendo los datos del diccionario de cada miembro de la familia
@app.route('/member', methods=['POST'])
def handle_post_one():
    # members = jackson_family.get_all_members(), no es necesario por la función add_members. Tampoco se necesita parámetros porque pasamos el body por la funcion y no por la url
    request_body = request.data
    member = json.loads(request_body)
    jackson_family.add_member(member)

    return jsonify({}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)