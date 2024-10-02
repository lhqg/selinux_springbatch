NAME := springbatch-systemd
SOURCEDIR := %sourcedir%
DESTDIR ?= %builddir%/debian/%name%
DOCDIR := /usr/share/doc
DATAROOTDIR := /usr/share

install: 
	@mkdir -p -m 0755 $(DESTDIR)/usr/lib/systemd/system
	@mkdir -p -m 0755 $(DESTDIR)/opt/springbatch/bin
	@mkdir -p -m 0755 $(DESTDIR)/opt/springbatch/service
	@mkdir -p -m 0755 $(DESTDIR)/usr/share/man/man7
	@mkdir -p -m 0755 $(DESTDIR)/$(DOCDIR)/$(NAME)/examples

	@install -m 0444 $(SOURCEDIR)/systemd/springbatch@.service $(DESTDIR)/usr/lib/systemd/system/
	@install -m 0555 $(SOURCEDIR)/systemd/springbatch-service.sh $(DESTDIR)/opt/springbatch/bin/

	@install -m 0444 $(SOURCEDIR)/systemd/env.SAMPLE $(DESTDIR)/$(DOCDIR)/$(NAME)/examples/

	@install -m 0444 $(SOURCEDIR)/LICENSE $(DESTDIR)/$(DOCDIR)/$(NAME)/
	@install -m 0444 $(SOURCEDIR)/manpages/man7/$(NAME).7 $(DESTDIR)/usr/share/man/man7/
