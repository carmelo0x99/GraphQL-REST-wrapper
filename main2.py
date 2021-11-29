import subprocess
from ariadne import ObjectType, make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL

type_defs = load_schema_from_path('schema.graphql')

# Create type instance for Query type defined in our schema...
query = ObjectType('Query')
user = ObjectType('User')
cisco = ObjectType('Cisco')

# ...and assign our resolver function to its "hello" field.
@query.field('hello')
def resolve_hello(_, info):
    request = info.context['request']
    user_agent = request.headers.get('user-agent', 'guest')
    return 'Hello, %s!' % user_agent

@query.field('user')
def resolve_user(_, info):
    return info.context['user']

@user.field('username')
def resolve_username(obj, *_):
    return f'{obj.first_name} {obj.last_name}'

@cisco.field('router')
def resolve_cisco_name(*_):
    URL ='https://n392.meraki.com/api/v0/networks/L_566327653141843049/devices'
    TOKEN = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'
#    return subprocess.check_output(['curl', '-sSL', '-X GET', '-H "X-Cisco-Meraki-API-Key: ' + TOKEN + '"', '-H "Accept: application/json"', URL])
    return ['curl', '-sSL', '-X GET', '-H "X-Cisco-Meraki-API-Key: ' + TOKEN + '"', '-H "Accept: application/json"', URL]

schema = make_executable_schema(type_defs, query, user, cisco)

app = GraphQL(schema, debug = True)

