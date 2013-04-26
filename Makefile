NAME=MIGHTYFOUR

all:
	mkdir -p $(NAME)/code
	cp -rv ./bin $(NAME)/code/
	cp -rv ./test $(NAME)/code/
	cp ./group.txt $(NAME)/
	cp ./introspection.txt $(NAME)/
	tar -czvf $(NAME).tar.gz $(NAME)

clean:
	rm -r $(NAME)*
