# [Software Testing] Lab06
###### tags: `Software Testing-23`

| Student ID | Name |
|------------|------|
| 311551095  | 林聖博|

##### 附上此篇Hackmd Link：https://hackmd.io/@Xc4BxciuS8-SomLNPca0Ng/ryk6CXSmn

- [\[Software Testing\] Lab06](#software-testing-lab06)
  - [Environment](#environment)
    - [Linux Version](#linux-version)
    - [GCC](#gcc)
    - [AddressSanitizer (ASan)](#addresssanitizer-asan)
    - [Valgrind](#valgrind)
  - [Part1](#part1)
    - [Summary](#summary)
    - [Heap out-of-bounds read/write](#heap-out-of-bounds-readwrite)
    - [Stack out-of-bounds read/write](#stack-out-of-bounds-readwrite)
    - [Global out-of-bounds read/write](#global-out-of-bounds-readwrite)
    - [Use-after-free](#use-after-free)
    - [Use-after-return](#use-after-return)
  - [Part2](#part2)
    - [Cross Redzone](#cross-redzone)

## Environment

### Linux Version
```
NAME="Ubuntu"
VERSION="20.04.5 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.5 LTS"
VERSION_ID="20.04"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal
```

### GCC
```
gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1) 
```

### AddressSanitizer (ASan)
```bash
$ gcc -fsanitize=address -g -o <test> <test.c>
$ ./<test>
```

### Valgrind
```bash
$ gcc -o <test> <test.c>
$ valgrind ./<test>
```

---

## Part1

### Summary

|                      | Valgrind | ASAN |
|----------------------|----------|------|
| Heap out-of-bounds   |    能    |  能  |
| Stack out-of-bounds  |   不能   |  能  |
| Global out-of-bounds |   不能   |  能  |
| Use-after-free       |    能    |  能  |
| Use-after-return     |   不能   |  能  |


### Heap out-of-bounds read/write

> Source code `test1.c`

```c=
#include <stdlib.h>
#include <stdio.h>

int main(){
    int length = 4;
    int *p = (int*) malloc(length * sizeof(int));
    
    p[4] = 4;
    printf("%d", p[4]);
    
    return 0;
}
```

#### ASan report
![](https://i.imgur.com/ua2prUg.png)

#### Valgrind report
![](https://i.imgur.com/KPKDU7K.png)

* ASan能，Valgrind能

### Stack out-of-bounds read/write

> Source code `test2.c`

```c=
#include <stdio.h>

int main(){
    int a[100];
    int b = a[101];
    
    return 0;
}
```

#### ASan report
![](https://i.imgur.com/WClaNP8.png)


#### Valgrind report
![](https://i.imgur.com/TA6Gwen.png)

* ASan能，Valgrind不能


### Global out-of-bounds read/write

> Source code `test3.c`

```c=
#include <stdio.h>

int a[100] = {0};

int main(){
    printf("%d\n", a[101]);
    
    return 0;
}

```

#### ASan report
![](https://i.imgur.com/bNPFp4X.png)


#### Valgrind report
![](https://i.imgur.com/1a1D5OA.png)

* ASan能，Valgrind不能


### Use-after-free

> Source code `test4.c`

```c=
#include <stdio.h>
#include <stdlib.h>

int main(){
    int *a = malloc(4 * sizeof(int));
    free(a);
    printf("%d\n", a[1]);
    
    return 0;
}
```

#### ASan report
![](https://i.imgur.com/5z75FNC.png)


#### Valgrind report
![](https://i.imgur.com/OFI9NXX.png)

* ASan能，Valgrind能


### Use-after-return

> Source code `test5.c`

```c=
#include <stdio.h>
#include <stdlib.h>

char* x;

void foo() {
    char stack_buffer[42];
    x = &stack_buffer[13];
}

int main() {
    foo();
    *x = 42; // Boom!
    
    return 0;
}
```


#### ASan report
> **Note**
執行前須加上 SAN_OPTIONS=detect_stack_use_after_return=1，才能抓到錯誤
```shell=
$ gcc -fsanitize=address -g -o test5 test5.c
$ ASAN_OPTIONS=detect_stack_use_after_return=1 ./test5
```

![](https://i.imgur.com/yAd8FLg.png)


#### Valgrind report
![](https://i.imgur.com/pYu432w.png)

* ASan能，Valgrind不能

---

## Part2
<p style="color:blue; font-size:18px; font-weight:bold;"> 寫一個簡單程式 with ASan，Stack buffer overflow 剛好越過 redzone (並沒有對 redzone 做讀寫)，並說明 ASan 能否找的出來？<p>

![](https://i.imgur.com/CVdcika.png)

### Cross Redzone

> Source code `lab6_2.c`
```c=
#include <stdio.h>

int main(){
    int a[8];
    int b[8];
    a[8+8] = 1;   // Cross!
    a[8+100] = 1; // Cross!
    
    return 0;
}
```
    
```bash=
$ gcc -fsanitize=address -g -o lab6_2 lab6_2.c
$ ./lab6_2
```
![](https://i.imgur.com/KBuaJnQ.png)

* **ASan 無法找出錯誤**
  > `a[8+0] ~ a[8+7]` 在 redzone 內可以抓到錯誤 <br>
  > `a[8+8]` 以後，會越過 redzone 無法抓到錯誤

### No Cross Redzone (補充)

> **Note**
`a[8+0] ~ a[8+7]` 在 redzone 內 ASan 可以抓到錯誤
![](https://i.imgur.com/F43rPko.png)
