ci-test:
	gcc ci-test.c `pkg-config --cflags --libs sdl2` -o ci-test

clean:
	rm -f ci-test
