ASFLAGS=--gdwarf-2 -o
LDFLAGS=--static
SOURCES=fork_explode.s
OBJECTS=$(SOURCES:.s=.o)
EXECUTABLE=fork_explode
all: $(SOURCES) $(EXECUTABLE)
$(EXECUTABLE): $(OBJECTS)
	ld $(LDFLAGS) $(OBJECTS) -o $@
.s.o:
	as $(ASFLAGS) $@ -c $<
clean:
	rm -f *.o
