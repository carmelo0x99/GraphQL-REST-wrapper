from ariadne import QueryType, gql, make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL

type_defs = load_schema_from_path('schema.graphql')

# Create type instance for Query type defined in our schema...
query = QueryType()

# ...and assign our resolver function to its "hello" field.
@query.field("hello")
def resolve_hello(_, info):
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return "Hello, %s!" % user_agent

schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug = True)

