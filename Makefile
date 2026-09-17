.PHONY: build test

VERSION := $(shell sed -n 's/^version = "\(.*\)"/\1/p' io_scene_kotor/blender_manifest.toml)

# Blender 3.6 predates extensions and installs add-on zips that hold the
# package directory, so it gets its own archive of the committed tree.
build:
	mkdir -p ./build
	blender --command extension build \
		--source-dir ./io_scene_kotor \
		--output-dir ./build
	git archive --format=zip -o ./build/io_scene_kotor-$(VERSION)-blender-3.6.zip HEAD io_scene_kotor

test:
	blender --background --python ./test/test_models.py

clean:
	rm -rf build/*
	rm -rf test/out/*
