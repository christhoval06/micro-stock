from apps.menu.menu import Menu, MenuItem

Menu.add_item(
    "user",
    MenuItem(
        "Users",
        None,
        children=[
            MenuItem('Users', parent=True),
            MenuItem('List', url='user:index', item=True),
            MenuItem('Create', url='user:create', item=True),
            MenuItem("Sub Menu", None,
                     children=[
                         MenuItem('List', url='user:index', item=True),
                         MenuItem('Create', url='user:create', item=True)
                     ])],
        check=lambda request: True,
        icon='flaticon-users',
    )
)
