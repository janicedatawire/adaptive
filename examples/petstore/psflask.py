# Copyright 2015 datawire. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pickle

from flask import Flask, abort
app = Flask(__name__)

import petstore_impl
import petstore_server

store = petstore_impl.PetStore()
server = petstore_server.PetStore_server(store)

@app.route("/" + petstore_server.service_name + "/<args>")
def run_service(args):
    try:
        command, args, kwargs = pickle.loads(args.decode("base64"))
    except Exception:
        abort(400)

    try:
        method = getattr(server, command)
    except AttributeError:
        abort(404)

    try:
        output = True, method(*args, **kwargs)
    except Exception as exc:
        output = False, exc

    return pickle.dumps(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
