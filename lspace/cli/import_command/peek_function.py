import click


def peek_function(file_type_object, old_choices, *args, **kwargs):
    click.echo_via_pager(file_type_object.get_text())
    return old_choices
