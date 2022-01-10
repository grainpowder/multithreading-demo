# Multithreading Demo

블로킹을 유발하는 Python task들을 실행하면서 Python multithreading의 대안을 확인

* CPU bounded task : 300차원 정방행렬을 제곱하고 trace를 계산하는 연산을 5번 반복
* IO bounded task : 8개의 사이트에 GET request를 3번씩 전송

## Demo setup

3.7 버전 이상의 Python이 필요하다. 

### on local machine

아래와 같은 커맨드를 입력해 데모를 실행하기 위한 환경을 설정(MacOS 기준)

```shell
cd multithreading-demo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PWD/src # set root directory as ./src
```

### on docker

도커 데몬을 실행하고 아래 커맨드를 입력

```shell
# On local
cd multithreading-demo
docker build -t demo_image:0.1.1 .
docker run \
  -i -t \
  --name demo_container \
  demo_image:0.1.1

# In container
cd $APP_PATH
```

# Commentary

여러 일을 한 사람이 병행하면서 처리하면 동시적(concurrency)으로, 여러 사람이 하나씩 맡아서 처리하면 병렬적(parallelism)으로 처리한다고 한다. 보다 구체적으로, 동시성은 쉽게 말해 한 사람이 이거했다 저거했다 다시 이거했다 저거하면서(context switching) 일을 처리하는 방식이다. 아무튼 핵심은 동시성/병렬성은 여러 일을 처리하는 방법에 대한 분류라는 것이다.

정의된 코드를 한 프로세스 안에서 여러 단위(스레드)로 나누고, 이를 한 프로세스 안에서 동시적/병렬적으로 실행하면 멀티스레딩이라고 한다. 하지만 Python에서는 GIL때문에 멀티스레딩으로는 동시성밖에 구현하지 못한다. GIL은 하나의 스레드가 해당 프로세스에 할당된 모든 자원을 독점하는 Python의 특징을 의미한다. CPU 코어가 하나밖에 없던 시절의 레거시라고 생각하면 된다. 아무튼 이 특징 때문에, 한 Python 프로세스에서 스레드가 여러 개 생기면 각 스레드가 자원을 독점하고 반납하는 과정을 반복하며 동시적으로 연산을 수행할 수 밖에 없게 된다.

## CPU bounded task

잘 알려진 것처럼 동시성은 CPU 바운드보다는 IO 바운드로 인해 발생한 블로킹을 개선하는데 적합하다. 일정량의 연산을 수행하기 전까지 끝나지 않는 일은 한 사람이 여러 단위로 나눠도 그 연산량이 줄어들지는 않기 때문이다. 오히려 context switching 과정에서 비효율만 생긴다. 차라리 사람을 더 불러서 일을 나눠주는게 더 효울적일 수 있다.


```shell
# Local
python src/demo/main.py start cpu

# Container
python3 demo/main.py start cpu
```

CPU 바운드를 야기하는 task를 수행하는 데모를 실행하면 이를 반영하는 결과를 확인할 수 있다. 연산을 하나씩 순서대로 한 거랑 멀티스레딩이랑 소요 시간이 큰 차이가 없다. 오히려 멀티스레딩이 더 오래 걸리는 경우도 흔히 생긴다. 하지만 사람을 더 불러서(즉, 멀티 프로세싱으로) 처리하면 실행 속도가 확연히 개선되는 것을 확인할 수 있다.

## IO bounded task

IO 바운드로 인해 발생한 블로킹은 요청을 보내고 응답을 기다리는 시간동안 발생하는 경우가 많다. 요청을 보내놓고 다른 요청을 보낸다면 이 기다리는 시간을 효율적으로 사용할 수 있기 때문에 수행하는 일을 바꿔가면서 작업을 처리하는 방식(동시성)이 효율적일 수 있다. 

하지만 응답을 기다리는 시간에 다른 요청을 보내는 일련의 과정 자체를 하나의 일로 생각한다면 굳이 context switching이 필연적으로 수반되는 동시성을 사용하지 않아도 된다. 이 작업에 드는 시간까지도 절약하며 블로킹을 개선하기 위해서는 비동기적(asynchronous) 프로그래밍을 사용한다. `await` 키워드를 사용해 루틴의 진입점과 탈출점을 여러 개 정의할 수 있는 코루틴을 `async def`로 정의해서 사용한다.

```shell
# Local
python src/demo/main.py start io

# Container
python3 demo/main.py start io
```

IO 바운드를 야기하는 task를 수행하는 데모를 실행하면 이를 반영하는 결과를 확인할 수 있다. 요청을 하나 보내고 응답을 기다리는 방식보다, 멀티스레딩을 통해 응답을 기다리는 시간을 효율적으로 사용하는 방식으로 task를 수행하는 것이 소요 시간이 더 짧았다. 하지만 코루틴을 사용한 비동기적 프로그래밍으로 단일 스레드에서 task를 수행했을 때의 소요시간이 가장 짧음을 확인할 수 있다.

## Conclusion

여러 일을 처리할 때 생길 수 있는 블로킹의 원인을 파악하자.
  * 원인이 CPU 바운드라면 병렬성을 사용해 블로킹을 개선해야 하고, 멀티 프로세싱을 사용한다.
  * 원인이 IO 바운드라면 코루틴을 활용한 비동기적 프로그래밍을 사용해 블로킹을 개선한다.
