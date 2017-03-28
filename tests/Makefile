test:
	./run.sh

coverage: test
	wkhtmltopdf cover/index.html notipycoverage.pdf

clean:
	rm -rf cover
	rm -f notipycoverage.pdf
