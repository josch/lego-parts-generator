BITMAPS:=$(patsubst parts/%.dat, bitmaps/%.png, $(wildcard parts/*.dat))

all: parts

parts:
	mkdir -p parts
	python partsgen.py

montage.png: $(BITMAPS)
	montage -label '%f' $(BITMAPS) $@

bitmaps/%.png: parts/%.dat
	mkdir -p bitmaps
	ldview -SaveActualSize=0 -SaveAlpha=1 -SaveWidth=300 -SaveHeight=300 -SaveZoomToFit=0 -SaveSnapShot=$@ $<

clean:
	rm -rf parts bitmaps

test:
	sha512sum --check parts.sha512
