import graphene
from parser import makelist as get_todos


def create_todos_from_filename(filename):
    todos = get_todos(filename)
    results = []
    for i, todo in enumerate(todos):
        results.append(Todo(
            id=i,
            heading=todo.Heading(),
            todo_type=todo.Todo(),
            due=todo.Deadline(),
            closed=todo.Closed(),
            tags=todo.Tags(),
            body=todo.Body()
        ))

    return results


class Todo(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node, )

    heading = graphene.String()
    todo_type = graphene.String()  # TODO Consider enums
    due = graphene.String()
    closed = graphene.String()
    tags = graphene.List(graphene.String)
    body = graphene.String()


class Viewer(graphene.ObjectType):
    todos = graphene.List(Todo)

    class Meta:
        interfaces = (graphene.relay.Node, )

    def resolve_todos(self, args, context, info):
        # TODO: Caching
        return create_todos_from_filename('.org/todo/todo.org')


class Query(graphene.ObjectType):
    viewer = graphene.Field(Viewer)

    def resolve_viewer(self, args, context, info):
        return Viewer(todos=create_todos_from_filename('.org/todo/todo.org'))


schema = graphene.Schema(query=Query)
