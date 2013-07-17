BITMAPS:=$(patsubst parts/%.dat, bitmaps/%.png, $(wildcard parts/*.dat))

all: montage.png

montage.png: $(BITMAPS)
	montage -label '%f' $(BITMAPS) $@

bitmaps/%.png: parts/%.dat
	ldview -SaveActualSize=0 -SaveAlpha=1 -SaveWidth=300 -SaveHeight=300 -SaveZoomToFit=0 -SaveSnapShot=$@ $<
