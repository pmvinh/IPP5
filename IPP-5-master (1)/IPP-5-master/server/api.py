import json
import logging
from flask import Flask, jsonify, request

from crud import ContactsCRUD
from models import Contact

app = Flask(__name__)
crud = ContactsCRUD()


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    header['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE'
    return response


@app.get("/v1/contact")
def get_contacts():
    contacts = crud.read_all()
    return {"contacts": contacts}, 200


@app.post("/v1/contact")
def create_contact():
    contact_dict = request.get_json()
    contact = Contact(**contact_dict)
    return crud.create(contact), 200


@app.delete("/v1/contact")
def delete_all_contacts():
    return {"contacts": crud.delete_all()}, 200


@app.get("/v1/contact/<uid>")
def get_contact(uid):
    contact = crud.read(uid)
    return contact, 200 if contact else 404


@app.delete("/v1/contact/<uid>")
def delete_contact(uid):
    contact = crud.delete(uid)
    return contact, 200 if contact else 404


@app.put("/v1/contact/<uid>")
def update_contact(uid):
    contact_dict = request.get_json()
    contact = Contact(**contact_dict)
    contact.id = uid
    updated_contact = crud.update(contact)
    return updated_contact, 200 if update_contact else 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
