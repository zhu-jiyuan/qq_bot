

run:
	python3 main.py

install:
	pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/


.PHONY: package

package:
	pip3 freeze > requirements.txt
	rm -f qqbot.tar.gz
	git ls-files | tar -czvf qqbot.tar.gz --exclude='.git' -T - config.yaml

clean:
	rm -f *.log
	mongo qqbot --eval "printjson(db.dropDatabase())"
