import typer
from geopephub.metageo_pephub import (
    add_to_queue,
    upload_queued_projects,
    run_upload_checker,
    check_by_date as check_by_date_function,
)
from geopephub.__version__ import __version__

app = typer.Typer()


def validate_target(value: str):
    valid_target = ["geo", "bedbase"]
    if value.lower() not in valid_target:
        raise typer.BadParameter(
            f"Invalid color '{value}'. Choose from: {', '.join(valid_target)}"
        )
    return value.lower()


@app.command()
def run_queuer(
    target: str = typer.Option(
        ...,
        help="Target of the pipeline. Namespace, and purpose of pipeline. Options: ['geo','bedbase']",
        callback=validate_target,
    ),
    tag: str = typer.Option(
        "default",
        help="Tag of the project, that will be uploaded to the pephub",
    ),
    period: int = typer.Option(
        1,
        help="Period (number of day) (time frame) when fetch metadata from GEO [used for q_fetch function]",
    ),
):
    """
    Queue GEO projects that were uploaded or updated in the last period
    """
    add_to_queue(target=target, tag=tag, period=period)


@app.command()
def run_uploader(
    target: str = typer.Option(
        ...,
        help="Target of the pipeline. Namespace, and purpose of pipeline. Options: ['geo','bedbase']",
        callback=validate_target,
    ),
    tag: str = typer.Option(
        "default",
        help="Tag of the project, that will be uploaded to the pephub",
    ),
):
    """
    Upload projects that were queued, but not uploaded yet.
    """
    upload_queued_projects(
        target=target,
        tag=tag,
    )


@app.command()
def run_checker(
    target: str = typer.Option(
        ...,
        help="Target of the pipeline. Namespace, and purpose of pipeline. Options: ['geo','bedbase']",
        callback=validate_target,
    ),
    tag: str = typer.Option(
        "default",
        help="Tag of the project, that will be uploaded to the pephub",
    ),
    cycle_count: int = typer.Option(
        1,
        help="Cycle that has to be checked if it was successful"
        " before the earliest one. e.g "
        "if we want to check todays cycle (if cycles are happening every day)"
        " you should insert 0."
        "(2) if you want to specify cycle that was happening 3 week before, and every cycle is happening"
        "once a week, you should set 2",
    ),
    period: int = typer.Option(
        1,
        help="length of the period - number of days (time frame) when fetch metadata from GEO [used for q_fetch function]",
    ),
):
    """
    Check if all projects were uploaded successfully in specified period and upload them if not.
    To check if all projects were uploaded successfully 3 periods ago, where one period is 1 day, and cycles are happening every day,
    you should set cycle_count=3, and period_length=1. (geopephub run_checker --cycle-count 3 --period-length 1)

    """
    run_upload_checker(
        target=target,
        period_length=period,
        tag=tag,
        number_of_cycles=cycle_count,
    )


@app.command()
def check_by_date(
    target: str = typer.Option(
        ...,
        help="Target of the pipeline. Namespace, and purpose of pipeline. Options: ['geo','bedbase']",
        callback=validate_target,
    ),
    tag: str = typer.Option(
        "default",
        help="Tag of the project, that will be uploaded to the pephub",
    ),
    start_period: str = typer.Option(
        None,
        help="start_period (Earlier in the calender) ['2020/02/25']",
    ),
    end_period: str = typer.Option(
        None,
        help="end period (Later in the calender) ['2021/05/27']",
    ),
):
    """
    Check if all projects were uploaded successfully in specified period and upload them if not.
    Additionally, you can download projects from huge period of time.
    e.g. if you want to download projects from 2020/02/25 to 2021/05/27, you should set start_period=2020/02/25, and end_period=2021/05/27
    """
    check_by_date_function(
        target=target,
        tag=tag,
        start_period=start_period,
        end_period=end_period,
    )


def version_callback(value: bool):
    if value:
        typer.echo(f"geopephub version: {__version__}")
        raise typer.Exit()


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", "-v", callback=version_callback, help="App version"
    ),
):
    pass