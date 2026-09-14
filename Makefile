PX := python3 scripts/px.py

SLUG ?=
LANG ?=

.PHONY: all help list booklet build watch new-booklet clean

all: help

help:
	@echo ""
	@echo "  Mathesis --- an ongoing exploration of mathematics, in booklets"
	@echo "  ──────────────────────────────────────────────────────────────"
	@echo "  make list                              List all booklets & build status"
	@echo "  make booklet SLUG=<slug|#> [LANG=en|fa] Build one booklet (default: both langs)"
	@echo "  make build                              Build every booklet, every language"
	@echo "  make watch SLUG=<slug|#> LANG=en|fa      Rebuild on file changes"
	@echo "  make new-booklet SLUG=<NN-slug>          Scaffold a new booklet"
	@echo "  make clean [SLUG=<slug|#|lang>]          Remove build artifacts"
	@echo ""
	@echo "  Examples:"
	@echo "    make booklet SLUG=1"
	@echo "    make booklet SLUG=01-mathematical-logic-and-proof-theory LANG=en"
	@echo "    make watch SLUG=3 LANG=en"
	@echo ""

list:
	@$(PX) booklets list

booklet:
ifndef SLUG
	$(error SLUG is not set. Usage: make booklet SLUG=<slug|#> [LANG=en|fa])
endif
ifdef LANG
	@$(PX) booklets build $(SLUG):$(LANG)
else
	@$(PX) booklets build $(SLUG)
endif

build:
	@$(PX) booklets build all

watch:
ifndef SLUG
	$(error SLUG is not set. Usage: make watch SLUG=<slug|#> LANG=en|fa)
endif
ifndef LANG
	$(error LANG is not set. Usage: make watch SLUG=<slug|#> LANG=en|fa)
endif
	@$(PX) booklets watch $(SLUG):$(LANG)

new-booklet:
ifndef SLUG
	$(error SLUG is not set. Usage: make new-booklet SLUG=<NN-slug>)
endif
	@$(PX) booklets new $(SLUG)

clean:
	@$(PX) booklets clean $(SLUG)
