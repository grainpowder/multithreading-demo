import typer

from tasks.cpu import *
from tasks.io import *
from util import *

app = typer.Typer()


@app.command("start")
def start(bound_type: BoundType = typer.Argument(..., case_sensitive=False)):
    logger = make_logger("main")

    if bound_type == BoundType.CPU:
        dimensions = [300] * 5

        logger.info("Execute CPU-tasks task synchronously")
        synchronous_execute(dimensions)

        logger.info("Execute CPU-tasks task using multithreading")
        multithread_execute(dimensions)

        logger.info("Execute CPU-tasks task using multiprocessing")
        multiprocess_execute(dimensions)

    elif bound_type == BoundType.IO:
        logger.info("Warming up")
        SynchronousIOBoundTask.execute(warmup=True)

        logger.info("Execute IO-tasks task synchronously")
        SynchronousIOBoundTask.execute(warmup=False)

        logger.info("Execute IO-tasks task using multithreading")
        MultithreadIOBoundTask.execute()

        logger.info("Execute IO-tasks task asynchronously")
        asyncio.run(AsynchronousIOBoundTask.execute())


@app.command("test")
def test(bound_type: BoundType = typer.Argument(..., case_sensitive=False)):
    if bound_type == BoundType.CPU:
        print("cpu")
    elif bound_type == BoundType.IO:
        print("io")


if __name__ == "__main__":
    app()
