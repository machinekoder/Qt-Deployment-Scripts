PREFIX := /usr/bin
TARGET := qt-deploy
TARGET2 := qt-release

all:
	@echo "Nothing to build"

install:
	@echo "installing Qt-Deployment scripts"
	cp -v $(TARGET).py $(PREFIX)/$(TARGET)
	cp -v $(TARGET2).py $(PREFIX)/$(TARGET2)
	chmod +x $(PREFIX)/$(TARGET)
	chmod +x $(PREFIX)/$(TARGET2)
