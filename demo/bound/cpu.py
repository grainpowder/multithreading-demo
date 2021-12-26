import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, NoReturn

from util import make_logger


class ProcessorBoundTask:
    logger = make_logger("task")

    @staticmethod
    def generate_square_matrix_of_ones(dimension: int) -> List[List[int]]:
        matrix = []
        for _ in range(dimension):
            matrix.append([1] * dimension)
        return matrix

    @staticmethod
    def multiply_matrices(matrix1: List[List[int]], matrix2: List[List[int]]) -> List[List[int]]:
        """
        naive O(n**3) implementation of matrix multiplication

        :param matrix1: n-dimensional square matrix
        :param matrix2: n-dimensional square matrix
        :return: n-dimensional square matrix
        """
        dimension = len(matrix1)
        result = []
        for i in range(dimension):
            row = []
            for j in range(dimension):
                element = 0
                for k in range(dimension):
                    element += matrix1[i][k] * matrix2[k][j]
                row.append(element)
            result.append(row)
        return result

    @staticmethod
    def calculate_trace(matrix: List[List[int]]) -> int:
        result = 0
        for index in range(len(matrix)):
            result += matrix[index][index]
        return result

    @staticmethod
    def execute(dimension: int) -> NoReturn:
        matrix1 = ProcessorBoundTask.generate_square_matrix_of_ones(dimension)
        matrix2 = ProcessorBoundTask.generate_square_matrix_of_ones(dimension)
        multiplied = ProcessorBoundTask.multiply_matrices(matrix1, matrix2)
        trace = ProcessorBoundTask.calculate_trace(multiplied)

        pid = os.getpid()
        tid = threading.get_ident()
        task_successful = trace == (dimension ** 2)
        ProcessorBoundTask.logger.info(f"PID : {pid}, TID : {tid}, Task ended successfully : {task_successful}")


class SynchronousExecution:

    @staticmethod
    def execute(dimensions: List[int]) -> NoReturn:
        start = time.time()
        [ProcessorBoundTask.execute(dimension) for dimension in dimensions]
        ProcessorBoundTask.logger.info(f"Elapsed time : {time.time() - start:.4f}")


class MultithreadExecution:

    @staticmethod
    def execute(dimensions: List[int]) -> NoReturn:
        start = time.time()
        executor = ThreadPoolExecutor(max_workers=4)
        list(executor.map(ProcessorBoundTask.execute, dimensions))
        ProcessorBoundTask.logger.info(f"Elapsed time : {time.time() - start:.4f}")


class MultiprocessExecution:

    @staticmethod
    def execute(dimensions: List[int]) -> NoReturn:
        start = time.time()
        executor = ProcessPoolExecutor(max_workers=4)
        list(executor.map(ProcessorBoundTask.execute, dimensions))
        ProcessorBoundTask.logger.info(f"Elapsed time : {time.time() - start:.4f}")
