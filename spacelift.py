import json
import urllib.request
import os

api_key_id = os.environ.get("SPACELIFT_API_KEY_ID")
api_key_secret = os.environ.get("SPACELIFT_API_KEY_SECRET")
domain = os.environ.get("SPACELIFT_DOMAIN")
stack_to_get = os.environ.get("SPACELIFT_STACK_TO_GET")

def query_api(query: str, variables: dict = None, token: str = None) -> dict:
    headers = {
        "Content-Type": "application/json",
    }

    if token is not None:
        headers["Authorization"] = f"Bearer {token}"

    data = {
        "query": query,
    }

    if variables is not None:
        data["variables"] = variables

    req = urllib.request.Request(f"https://{domain}/graphql", json.dumps(data).encode('utf-8'), headers)
    with urllib.request.urlopen(req) as response:
        resp = json.loads(response.read().decode('utf-8'))

    if "errors" in resp:
        print(f"Error: {resp['errors']}")
        return resp
    else:
        return resp

def getStackWithId(id, token):
    query = """
query getStackWithId($keyId: ID!) {
  stack(id: $keyId) {
      space
    }
}
    """

    variables = {
        "keyId": id
    }

    return query_api(query, variables, token)

def createStackWithBlueprint(id, inputs, token):
    query = """
mutation createStackFromBlueprint($id: ID!, $input: BlueprintStackCreateInput!) {
    blueprintCreateStack(id: $id, input: $input) {
        stackID
    }
}
    """

    variables = {
        "id": id,
        "input": {
            "templateInputs": inputs
        }
    }

    return query_api(query, variables, token)

def get_token():
    token_mutation = """
        mutation GetSpaceliftToken($id: ID!, $secret: String!) {
            apiKeyUser(id: $id, secret: $secret) {
                jwt
            }
        }
    """

    token_variables = {
        "id": api_key_id,
        "secret": api_key_secret
    }

    token_response = query_api(token_mutation, token_variables)
    return token_response["data"]["apiKeyUser"]["jwt"]


t = get_token()
res = getStackWithId(stack_to_get, t)
print(res)