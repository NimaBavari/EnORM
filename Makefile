cleanup:
	chmod +x cleanup.sh
	./cleanup.sh

set_dev_env:
	chmod +x set_pre_commit.sh
	./set_pre_commit.sh

.PHONY: test

test:
	chmod +x test.sh
	./test.sh