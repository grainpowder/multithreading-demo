import typer

from tasks.cpu import *
from tasks.io import *
from util import *

app = typer.Typer()


@app.command("start")
def start(bound_type: BoundType = typer.Argument(..., case_sensitive=False, help="type of bounded task")):
    logger = make_logger("start")

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
def test(
        bound_type: BoundType = typer.Argument(..., case_sensitive=False, help="type of bounded task"),
        dimension: int = typer.Option(3, "-d", "--dimension", max=10, help="dimension of matrix for CPU bounded task")
):
    logger = make_logger("test")

    if bound_type == BoundType.CPU:
        logger.info("Generate matrices of ones")
        matrix1 = ProcessorBoundTask.generate_square_matrix_of_ones(dimension)
        matrix2 = ProcessorBoundTask.generate_square_matrix_of_ones(dimension)
        logger.info(f"A = {matrix1[0]}\tB = {matrix2[1]}")
        spaces = " " * 4
        for index in range(1, len(matrix1)):
            logger.info(f"{spaces}{matrix1[index]}\t{spaces}{matrix2[index]}")

        logger.info("Multiply generated matrices of ones")
        multiplied = ProcessorBoundTask.multiply_matrices(matrix1, matrix2)
        logger.info(f"AB = {multiplied[0]}")
        for index in range(1, len(multiplied)):
            logger.info(f" {spaces}{multiplied[index]}")

        logger.info("Calculate trace of multiplied matrix")
        trace = ProcessorBoundTask.calculate_trace(multiplied)
        logger.info(f"\tTr(AB) = {trace}")

        logger.info("Validate calculated trace value")
        logger.info(f"\t{dimension} * {dimension} = {trace}")

    elif bound_type == BoundType.IO:
        test_url = "https://naver.com"

        logger.info(f"Send request to {test_url}")
        with httpx.Client() as client:
            response = SynchronousIOBoundTask.fetch(client, test_url, True)
            logger.info(f"Got {response.status_code} response from {response.url}")


if __name__ == "__main__":
    app()
