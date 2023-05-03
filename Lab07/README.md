# [Software Testing] Lab07 - Fuzz Testing
###### tags: `Software Testing-23`

| Student ID | Name |
|------------|------|
| 311551095  | 林聖博|

###### 附上此篇Hackmd Link：https://hackmd.io/@Xc4BxciuS8-SomLNPca0Ng/HyVLrp142

<!-- TOC -->

- [[Software Testing] Lab07 - Fuzz Testing](#software-testing-lab07---fuzz-testing)
    - [Lab Requirements](#lab-requirements)
        - [PoC](#poc)
        - [Step by Step](#step-by-step)
        - [AFL Fuzzing](#afl-fuzzing)
        - [Running AFL Lab](#running-afl-lab)
        - [Crash detail with ASAN error report](#crash-detail-with-asan-error-report)
        - [Additional](#additional)
        - [Reference](#reference)

<!-- /TOC -->

## Lab Requirements
[Lab7](https://github.com/chameleon10712/NYCU-Software-Testing-2023/tree/main/Lab07) provide a small program that converts bmp from color to grayscale.
* Use AFL to find the file that can trigger the vulnerability.
* Use `test.bmp` as initial seed.

The report shall contain the following information:
1. **PoC**: the file that can trigger the vulnerability
2. The commands (steps) that you used in this lab
3. Screenshot of AFL running (with triggered crash)
4. Screenshot of crash detail (with ASAN error report)


### PoC
* Following this file : [id:000000,sig:06,src:000000,op:flip1,pos:18](./PoC/crashes/id:000000,sig:06,src:000000,op:flip1,pos:18)

Command line used to find this crash:
```
./AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp
```

### Step by Step
The commands (steps) used in this lab

#### Environment Setting
1. Run Docker container for AFL Fuzzing Lab
    > **Note** Use `--privileged` let container with full system privileges (root) of the host in a Docker environment
    > ![](https://i.imgur.com/2fhA25F.png)
    ```bash
    $ docker run -it --privileged  -v /home/[user]/path/to/folder:/work ubuntu:22.04 bash
    ```
    ```
    PRETTY_NAME="Ubuntu 22.04.2 LTS"
    NAME="Ubuntu"
    VERSION_ID="22.04"
    VERSION="22.04.2 LTS (Jammy Jellyfish)"
    VERSION_CODENAME=jammy
    ```
2. Install necessary packages
```bash=
$ apt update
$ apt install -y git vim gcc g++ unzip python3 python3-pip
$ apt install automake autoconf libtool pkg-config
```
3. Build AFL
```bash=
$ git clone https://github.com/google/AFL.git
$ cd AFL
$ make
$ make install
```
4. Build libxml2
```bash=
$ git clone https://gitlab.gnome.org/GNOME/libxml2.git
$ cd libxml2
$ ./autogen.sh
$ export CC=/work/AFL/afl-gcc    # AFL C++ compiler
$ export CXX=/work/AFL/afl-g++   # AFL C compiler
$ export AFL_USE_ASAN=1          # Use ASAN (Address SANitizer)
$ ./configure --enable-shared=no
$ make
```
5. AFL setting
```bash=
$ echo core >/proc/sys/kernel/core_pattern
$ echo performance | tee cpu*/cpufreq/scaling_governor
```
6. Download Lab07 from [Course Github](https://github.com/chameleon10712/NYCU-Software-Testing-2023/tree/main/Lab07)
![](https://i.imgur.com/cQASybN.png)
8. Setting Lab work

```bash=
$ cd Lab07
$ export CC=./AFL/afl-gcc
$ export AFL_USE_ASAN=1
$ make
$ mkdir in
$ cp test.bmp in/
$ ./AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp
```

### AFL Fuzzing
```bash
$ afl-fuzz -i in/ -o out/ -b 10 -m none -- ./target [argv1] @@ [argv2]
```
* `-i dir` : seed dir
* `-o dir` : output dir
* `-b CPU_ID` : bind the fuzzing process to the specified CPU core
* `-m megs` : memory limit for child process
* `@@` : the location of the input (if NO -> stdin)

### Running AFL Lab
* Directory Structure
    ![](https://i.imgur.com/hYax0Et.png)
* AFL running **with triggered crash**
    > I try fuzzing about `0 day, 18 hrs, 18 min`
    > And only find **`1 crash(unique)`**
    > ![](https://i.imgur.com/KvYzMk2.png)
<!--     > ![](https://i.imgur.com/FhXI031.png) -->
<!--     > ![](https://i.imgur.com/AoGx5ZQ.png) -->

### Crash detail with ASAN error report
* Execute the following command to reproduce the error (**with ASAN**)：
    ```bash
    ./bmpgrayscale out/crashes/id:000000* a.bmp
    ```
    ![](https://i.imgur.com/TJqhSz9.png)
> When run the fuzz testing in this cases, some crash input will save in `./out/default/crashes`
> ![](https://i.imgur.com/Z755Xb1.png =400x)

---

### Additional
由 ASAN error report 得知， Error 出現在 source code 中 `bmpgrayscale.c:41` 第 41 行中
![](https://i.imgur.com/yVEjJKr.png =500x)

該行使用`memset()`進行記憶體配置(設置)，且`memset()`參數如下:
```cpp=
void *memset(void *str, int c, size_t n)
```

Example for `memset()`:
```cpp=
#include <stdio.h>
#include <string.h>
 
int main ()
{
   char str[50];
 
   strcpy(str,"This is string.h library function");
   puts(str);
 
   memset(str,'$',7);
   puts(str);
   
   return(0);
}
```
```
This is string.h library function
$$$$$$$ string.h library function
```

可發現第三個參數型態為`size_t`(`unsigned int`)，且`bmpgrayscale.c:41`將`n`設定為`2 * padding - 3`，而由目前 crash 輸入可發現此輸入`padding`為`1`，因此，`2 * padding - 3`結果為`-1`。

若`memset(void *str, int c, size_t n)`的參數`n`設定為`-1`會因為`size_t`變成`4294967295`，使得將`pixel[3]`前`4294967295`填充為`gray`的值，而`4294967295`大於`3`，導致 overflow (stack overflow / buffer overflow)。

修改後，添加`2 * padding - 3`判斷(加入35~38行)，避免`< 0`的數值出現
![](https://i.imgur.com/yploxaK.png)

在嘗試進行 AFL Fuzz Testing 就沒有再發現 Crash 的發生
![](https://i.imgur.com/H5LT6ca.png)


### Reference
* https://github.com/google/AFL
* https://afl-1.readthedocs.io/en/latest/
* https://github.com/AFLplusplus/AFLplusplus
* https://aflplus.plus/docs/technical_details/
* https://aflplus.plus/docs/tutorials/libxml2_tutorial/
