PREFIX := /usr/bin
TARGET := qt-deploy

all:
	@echo "Nothing to build"

install:
	@echo "installing ap-hotspot utility"
	cp -v $(TARGET).py $(PREFIX)/$(TARGET)
	chmod +x $(PREFIX)/$(TARGET)