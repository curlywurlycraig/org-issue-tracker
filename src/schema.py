import graphene
from parser import makelist as get_todos


def create_todos_from_filename(filename):
    todos = get_todos(filename)
    results = []
    for todo in todos:
        results.append(Todo(
            heading=todo.Heading(),
            todo_type=todo.Todo(),
            due=todo.Deadline(),
            closed=todo.Closed(),
        ))

    return results


class Todo(graphene.ObjectType):
    heading = graphene.String()
    todo_type = graphene.String()  # TODO Consider enums
    due = graphene.String()
    closed = graphene.String()


class Query(graphene.ObjectType):
    todos = graphene.List(Todo)

    def resolve_todos(self, args, context, info):
        # fetch all todos
        # TODO: Caching
        return create_todos_from_filename('.org/todo/todo.org')


schema = graphene.Schema(query=Query)
