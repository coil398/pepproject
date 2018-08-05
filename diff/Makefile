LIBS = `pkg-config --libs opencv`
CFLAGS = `pkg-config --cflags opencv`

camera_diff: camera_diff.o
	g++ -o $@ $(LIBS) camera_diff.o

camera_diff.o: camera_diff.cpp
	g++ -c $(CFLAGS) camera_diff.cpp

clean:
	rm -f camera_diff.o
