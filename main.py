import os
from flask import Flask, request, Response, send_from_directory
from dotenv import load_dotenv
from threading import Thread
import logging
import json
import google.cloud.logging
from Functions.GravityForms import (
    handleGravityFormsSubmission,
    handleGravityFormsDelete
)
from Functions.Slack import (
    handleSlackAction
)
from Functions.Triggers import (
    handleCheckUnapprovedTrigger
)
from Functions.Shared import (
    sendEmail
)

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
googleLoggingClient = google.cloud.logging.Client()
googleLoggingClient.setup_logging()

app = Flask(__name__)

@app.route('/')
def status():
    return Response('Service is running.', 200)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/webhooks/gravityforms/workout', methods=['POST'])
def processGravityFormsWorkout():
    thread = Thread(target=handleGravityFormsSubmission, kwargs={'body':request.json})
    thread.start()
    return Response(status=200)

@app.route('/webhooks/gravityforms/workoutdelete', methods=['POST'])
def processGravityFormsWorkoutDelete():
    thread = Thread(target=handleGravityFormsDelete, kwargs={'body':request.json})
    thread.start()
    return Response(status=200)

@app.route('/webhooks/slack', methods=['POST'])
def processSlack():
    body=json.loads(request.form['payload'])
    
    if body['type'] == 'block_actions':
        thread = Thread(target=handleSlackAction, kwargs={'body':body})
    else:
        logging.warning('Received an interactive message from Slack with an unhandled type: ' + body['type'])
        return Response(status=400)
        
    thread.start()
    return Response(status=200)

@app.route('/triggers/checkunapproved')
def checkForUnapprovedWorkouts():
    thread = Thread(target=handleCheckUnapprovedTrigger)
    thread.start()
    return Response(status=200)

@app.route('/test')
def test():
    sendEmail('Map Request Approved', ['damon.vinciguerra@gmail.com'], 'this is a test')
    return Response(status=200)

if __name__ == "__main__":
    logging.info('Starting up app')
    load_dotenv()
    app.run(port=8080, debug=False)