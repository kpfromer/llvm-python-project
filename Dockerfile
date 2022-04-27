# https://www.cs.utexas.edu/~pingali/CS380C/2019/assignments/llvm-guide.html
FROM debian:stable

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
    cmake \
    ninja-build \
    clang \
    git

RUN git clone --depth 1 https://github.com/llvm/llvm-project.git llvm
RUN cd llvm

RUN mkdir build
RUN cd build
RUN cmake -G Eclipse\ CDT4\ -\ Ninja -DLLVM_TARGETS_TO_BUILD=host ../llvm/
RUN ninja