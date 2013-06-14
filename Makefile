ANSIBLE_HACKING = ../ansible/hacking
FORMATTER = $(ANSIBLE_HACKING)/module_formatter.py
#TEMPLATES = $(ANSIBLE_HACKING)/templates
TEMPLATES = _templates
FORMATTER_TARGET = markdown
PANDOC = pandoc
LIBRARY_DIR = library
BUILD_DIR = _build

all: index.md

MODULES = $(wildcard $(LIBRARY_DIR)/*)
index.md: $(patsubst $(LIBRARY_DIR)/%,$(BUILD_DIR)/%.md,$(MODULES))
index.md: index-header.yaml
	cp index-header.yaml $@
	for file in $(BUILD_DIR)/*.md; do \
		echo >> $@; \
		cat $$file >> $@; \
	done

$(BUILD_DIR)/%.md: $(LIBRARY_DIR)/% $(BUILD_DIR) $(FORMATTER) $(TEMPLATES)/$(FORMATTER_TARGET).j2
	$(FORMATTER) -T $(TEMPLATES) -t markdown -M . -m $* -o $(BUILD_DIR)
# $(FORMATTER) -T $(TEMPLATES) -t rst -M . -m $* |\
# 	pandoc -f rst -t markdown_github > $@

$(BUILD_DIR):
	mkdir $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR) index.md
