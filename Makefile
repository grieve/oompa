build:
	docker build -t oompa-server .

run: build
	docker run -ti --rm -p 0.0.0.0:5000:5000 -v $(CURDIR):/app oompa-server
