ci-test: ci-test.c
	gcc ci-test.c -no-pie `pkg-config --cflags --libs sdl2` -o ci-test

clean:
	rm -f ci-test
