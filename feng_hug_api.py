#!/usr/bin/env python3
import os
import sys
import tempfile

from falcon import HTTP_500
import hug
import sh

PARSER_PATH = '/opt/feng-hirst-rst-parser/src'
PARSER_EXECUTABLE = 'parser_wrapper.py' # Feng/Hirst uses Python 2, but our API is in Python 3


@hug.response_middleware()
def process_data(request, response, resource):
    """This is a middleware function that gets called for every request a hug API processes.
    It will allow Javascript clients on other hosts / ports to access the API (CORS request).
    """
    response.set_header('Access-Control-Allow-Origin', '*')

@hug.response_middleware()
def process_response(request, response, resource, req_succeeded=True):
    """This is a middleware function that gets called for every request a hug API processes
    AFTER the response is routed. Here, we delete the (temporary) file
    that contained the parser result.
    """
    os.unlink(response.stream.name)

@hug.post('/parse', output=hug.output_format.file)
def call_parser(body, response):
    parser = sh.Command(os.path.join(PARSER_PATH, PARSER_EXECUTABLE))

    if body and 'input' in body:
        input_file_content = body['input']
        with tempfile.NamedTemporaryFile() as input_file:
            input_file.write(input_file_content)
            input_file.flush()
            try:
                result = parser(input_file.name, _cwd=PARSER_PATH)
                with tempfile.NamedTemporaryFile(delete=False) as output_file:
                    output_file.write(result.stdout)
                    output_file.flush()
                    return output_file.name

            except sh.ErrorReturnCode_1 as err:
                response.status = HTTP_500
                trace = str(err.stderr, 'utf-8')
                error_msg = "{0}\n\n{1}".format(err, trace).encode('utf-8')

                with tempfile.NamedTemporaryFile(delete=False) as error_file:
                    error_file.write(error_msg)
                    error_file.flush()
                    return error_file.name

    else:
        response.status = HTTP_400
        return {'body': body}
