BITMAPS:=$(patsubst parts/%.dat, bitmaps/%.png, $(wildcard parts/*.dat))

LDFLAGS+=-lm
LINK.o = $(LINK.cc)
CXXFLAGS=-Wall -pedantic

partsgen: partsgen.o

clean:
	rm -f partsgen.o partsgen
	rm -f bitmaps/*

test: montage.png

montage.png: $(BITMAPS)
	montage -label '%f' $(BITMAPS) $@

bitmaps/%.png: parts/%.dat
	~/debpkg/ldview-4.2\~beta1+dfsg/QT/LDView -SaveActualSize=0 -SaveAlpha=1 -SaveWidth=300 -SaveHeight=300 -SaveZoomToFit=0 -SaveSnapShot=$@ $<
