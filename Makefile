

run:
	python3 main.py

install:
	pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

package:
	pip3 freeze > requirements.txt

clean:
	rm -f *.log
