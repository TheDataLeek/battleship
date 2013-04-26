NAME=MIGHTYFOUR

all:
	mkdir -p $(NAME)/code
	cp -rv ./bin $(NAME)/code/
	cp -rv ./test $(NAME)/code/
	cp ./group.txt $(NAME)/
	cp ./introspection.txt $(NAME)/
	zip -r $(NAME).zip $(NAME)

clean:
	rm -r $(NAME)*
