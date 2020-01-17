from flask import Flask
from flask_restful import Api
from flask.app import Flask as FlaskApp
from flask.cli import with_appcontext
import click
from meetup_search.commands.get_groups import get_groups as command_get_groups
from meetup_search.commands.get_group import get_group as command_get_group
from meetup_search.commands.update_groups import update_groups as command_update_groups
from meetup_search.commands.get_zip_codes import load_zip_codes as command_load_zip_codes
from meetup_search.models.group import Group
from meetup_search.models.meetup_zip import MeetupZip
from typing import Optional
from envparse import env
from meetup_search.rest_api.api import MeetupSearchApi, MeetupSearchSuggestApi
from flask_cors import CORS


def create_app(config_path: Optional[str] = None) -> FlaskApp:
    """
    Create a flask app and load a config file. 
    When no config_path is given it will try to load the config file from FLASK_CONFIGURATION enviroment var and when the
    FLASK_CONFIGURATION does not exists, it load the production config file.

    Keyword Arguments:
        config_path {Optional[str]} -- Path to a flask config file (default: None)

    Returns:
        FlaskApp -- flask app with loaded configs
    """

    if not config_path:
        config_path = env("FLASK_CONFIGURATION", "/app/config/production.py")

    # init flask app
    app = Flask(__name__)
    app.config.from_pyfile(config_path)
    CORS(app, resources={r"/*": {"origins": env("CORS_ORIGINS")}})

    # init flask api
    api: Api = Api(app)
    api.add_resource(MeetupSearchApi, "/")
    api.add_resource(MeetupSearchSuggestApi, "/suggest/")

    # set flask cli commands

    @click.command(name="get_group")
    @with_appcontext
    @click.option("--sandbox", nargs=1, type=bool)
    @click.argument(
        "meetup_group_urlname", type=str, required=False,
    )
    def get_group(meetup_group_urlname: Optional[str] = None, sandbox: bool = False):
        """
        load single group from meetup.com into elasticsearch

        Keyword Arguments:
            meetup_group_urlname {Optional[str]} -- meetup group urlname to load the group from meetup (default: {None})
            sandbox {bool} -- if true -> meetup_group_urlname will auto set to sandbox group (default: {False})
        """
        if sandbox:
            meetup_group_urlname = "Meetup-API-Testing"

        if meetup_group_urlname:
            command_get_group(meetup_group_urlname=meetup_group_urlname)
        else:
            print("No meetup_group_urlname was given!")
            exit(1)

    @click.command(name="get_groups")
    @click.option("--load_events", nargs=1, type=bool, default=True)
    @with_appcontext
    @click.argument(
        "meetup_files_path",
        type=click.Path(exists=True),
        required=False,
        default="meetup_groups",
    )
    def get_groups(meetup_files_path: str, load_events: bool = True):
        """
        import new meetup groups from JSON files and get all events from meetup.com

        Arguments:
            meetup_files_path {str} -- path of the meetup JSON files
            load_events {bool} -- load all events from groups (default: {True})
        """
        command_get_groups(meetup_files_path=meetup_files_path, load_events=load_events)

    @click.command(name="migrate_models")
    @with_appcontext
    def migrate_models():
        """
        init elasticsearch models
        """
        Group.init()
        MeetupZip.init()

    @click.command(name="load_zip_codes")
    @click.argument("lat_min", type=float, required=True)
    @click.argument("lat_max", type=float, required=True)
    @click.argument("lon_min", type=float, required=True)
    @click.argument("lon_max", type=float, required=True)
    @with_appcontext
    def load_zip_codes(lat_min: float, lat_max: float, lon_min: float, lon_max: float):
        """
        Load all meetup zip codes from a boundingbox [min_lat, max_lat, min_lon, max_lon]

        Arguments:
            lat_min {float} -- boundingbox lat min
            lat_max {float} -- boundingbox lat max
            lon_min {float} -- boundingbox lon min
            lon_max {float} -- boundingbox lon max
        """
        command_load_zip_codes(lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)

    @click.command(name="update_groups")
    @with_appcontext
    def update_groups():
        """
        update for all groups new events
        """
        command_update_groups()

    # add commands to flask app
    app.cli.add_command(get_group)
    app.cli.add_command(get_groups)
    app.cli.add_command(update_groups)
    app.cli.add_command(load_zip_codes)
    app.cli.add_command(migrate_models)

    return app


flask_app: FlaskApp = create_app()

if __name__ == "__main__":
    flask_app.run(host=env("FLASK_HOST", "127.0.0.1"))
