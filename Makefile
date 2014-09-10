BITMAPS:=$(patsubst parts/%.dat, bitmaps/%.png, $(wildcard parts/*.dat))
BITMAPSWF:=$(patsubst parts/%.dat, bitmaps-wireframe/%.png, $(wildcard parts/*.dat))

all: parts

parts:
	mkdir -p parts
	python partsgen.py

montage.png: parts $(BITMAPS)
	montage -label '%f' $(BITMAPS) $@

montage-wireframe.png: parts $(BITMAPSWF)
	montage -label '%f' $(BITMAPSWF) $@

bitmaps/%.png: parts/%.dat
	mkdir -p bitmaps
	ldview -SaveActualSize=0 -SaveAlpha=1 -SaveWidth=300 -SaveHeight=300 -SaveZoomToFit=0 -SaveSnapShot=$@ $<

bitmaps-wireframe/%.png: parts/%.dat
	mkdir -p bitmaps-wireframe
	ldview -Wireframe=1 -SaveActualSize=0 -SaveAlpha=1 -SaveWidth=300 -SaveHeight=300 -SaveZoomToFit=0 -SaveSnapShot=$@ $<

clean:
	rm -rf parts bitmaps bitmaps-wireframe montage.png

test: parts montage.png montage-wireframe.png
	sha512sum --check parts.sha512
