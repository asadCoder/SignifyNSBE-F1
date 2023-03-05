from __future__ import division

# Our Backend for the App!
# Built with Flask

# Import Flask
import flask
from flask import send_file

import re
import sys

from six.moves import queue

# Create the application
app = flask.Flask(__name__)

# serving home.html
@app.route('/', methods=['GET'])
def serve_page():
    return flask.render_template('home.html')

# process query
@app.route('/process_query', methods=['POST'])
def process_query():
    # data = flask.request.form  # is a dictionary
    data = flask.request.get_json();
    input = data['user_input']
    input_in_list = input.split(' ')
    return flask.render_template('home.html', same=processInput(input_in_list), og=input)


def processInput(input_in_list):
    for s, i in enumerate(input_in_list):
        if "bye" in i.lower():
            input_in_list[s] = "static/bye.jpg"
        if "hello" in i.lower():
            input_in_list[s] = "static/hello.png"
        if "yes" in i.lower():
            input_in_list[s] = "static/yes.png"
        if "no" in i.lower():
            input_in_list[s] = "static/no.png"
        if "please" in i.lower():
            input_in_list[s] = "static/please.png"
        if "thanks" in i.lower():
            input_in_list[s] = "static/thanks.png"
        if "who" in i.lower():
            input_in_list[s] = "static/who.png"
        if "what" in i.lower():
            input_in_list[s] = "static/what.png"
        if "when" in i.lower():
            input_in_list[s] = "static/when.png"
        if "where" in i.lower():
            input_in_list[s] = "static/where.png"
        if "why" in i.lower():
            input_in_list[s] = "static/why.png"
        if "which" in i.lower():
            input_in_list[s] = "static/which.png"
        if "how" in i.lower():
            input_in_list[s] = "static/how.png"
    return input_in_list

def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            return flask.render_template('home.html', same=processInput("".join(transcript).split(" ")), og="".join(transcript))

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0

if __name__ == '__main__':
    app.run(debug=True)
