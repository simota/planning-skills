# Wire this repo into a skills directory, and keep it inside its budgets.
#
# The repo is the single source of truth: each planning-* directory is symlinked
# individually into every installed CLI's skills directory (claude, codex,
# agy), so each of those directories keeps whatever else it already carries.

REPO       := $(CURDIR)
CLAUDE_DIR ?= $(HOME)/.claude/skills
CODEX_DIR  ?= $(HOME)/.codex/skills
AGY_DIR    ?= $(HOME)/.gemini/antigravity-cli/skills

# Every CLI reading a SKILL.md gets the same working tree. A host is only
# written to when it is installed here, and its own home — the parent of the
# skills directory — is what says so: judging by the skills directory itself
# would skip a host that has one but has never been given a skill.
# Quoted one by one where it is used: a home directory may contain a space,
# and an unquoted list would split it into two paths and link into the first.
HOST_DIRS  := "$(CLAUDE_DIR)" "$(CODEX_DIR)" "$(AGY_DIR)"

.DEFAULT_GOAL := help
.PHONY: help check validate test figures figures-full figures-rewrite engines refute render hooks link unlink status

help:
	@echo "make check     validate + test + figures (what CI runs)"
	@echo "make validate  static rules over the corpus"
	@echo "make test      prove every rule still fires"
	@echo "make refute CLAIMS=f.json RUNNING=<engine>   put each claim to the engines that did not make it"
	@echo "make engines  ask each checker engine for one object; reports what is unreachable"
	@echo "make render    write the delivered blocks back into every SKILL.md"
	@echo "make figures   check the published figures against the model fixture"
	@echo "make figures-full  re-run the seeded model (~1 min); fails if the fixture disagrees"
	@echo "make figures-rewrite  the same, writing the new fixture — the model changed on purpose"
	@echo "make hooks     install the pre-commit hook"
	@echo "make link      symlink the skills into claude / codex / agy"
	@echo "make unlink    remove those symlinks"
	@echo "make status    show what is linked"

check: validate test figures

validate:
	@python3 planning-tools/validate.py

test:
	@python3 planning-tools/test_validate.py
	@python3 planning-tools/test_planning_regressions.py
	@python3 planning-tools/test_engine.py

engines:
	@python3 planning-tools/engine.py --selftest

refute:
	@test -n "$(CLAIMS)" && test -n "$(RUNNING)" || { \
		echo "usage: make refute CLAIMS=claims.json RUNNING=<the engine running this>"; exit 2; }
	@python3 planning-tools/refute.py --running "$(RUNNING)" "$(CLAIMS)"

render:
	@python3 planning-tools/render.py

figures:
	@python3 planning-tools/figures_check.py

figures-full:
	@python3 planning-tools/figures_check.py --full

figures-rewrite:
	@python3 planning-tools/figures_check.py --rewrite

# Where git looks, not where it usually is: a worktree's hooks live in the main
# repository, and `core.hooksPath` moves them anywhere — possibly a directory
# every repository shares, so a hook already there is never silently replaced.
hooks:
	@dir=$$(git rev-parse --git-path hooks) && mkdir -p "$$dir" && hook="$$dir/pre-commit" && \
		if [ "$$hook" -ef planning-tools/githooks/pre-commit ] || cmp -s planning-tools/githooks/pre-commit "$$hook"; then :; \
		elif [ -e "$$hook" ] && [ -z "$(FORCE)" ]; then \
			echo "$$hook already exists and differs; not replacing it (FORCE=1 to overwrite)"; exit 1; \
		else cp planning-tools/githooks/pre-commit "$$hook"; fi && \
		chmod +x "$$hook" && echo "pre-commit installed in $$dir"

# A skill is a directory holding a SKILL.md, under skills/ where the plugin
# format expects it. The prefix alone is not the test: planning-registry/ and
# planning-tools/ share it and must never be installed.
SKILL_DIRS := $(patsubst %/SKILL.md,%,$(wildcard skills/planning-*/SKILL.md))

link:
	@for dir in $(HOST_DIRS); do \
		if [ ! -d "$$(dirname "$$dir")" ]; then echo "skip $$dir (host not installed here)"; continue; fi; \
		mkdir -p "$$dir"; \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -e "$$target" ] && [ ! -L "$$target" ]; then \
				echo "  skip $$name (a real path is already there)"; \
			elif [ -L "$$target" ] && [ -e "$$target" ] && [ "$$(readlink "$$target")" != "$(REPO)/$$path" ]; then \
				echo "  skip $$name (links to $$(readlink "$$target"), not this repo)"; \
			else \
				ln -sfn "$(REPO)/$$path" "$$target"; echo "  link $$name"; \
			fi; \
		done; \
	done

unlink:
	@for dir in $(HOST_DIRS); do \
		[ -d "$$dir" ] || continue; \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$(REPO)/$$path" ]; then \
				rm "$$target"; echo "  unlink $$name"; fi; \
		done; \
	done

status:
	@for dir in $(HOST_DIRS); do \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$(REPO)/$$path" ]; then echo "  linked   $$name"; \
			elif [ -L "$$target" ]; then echo "  other    $$name -> $$(readlink "$$target")"; \
			else echo "  unlinked $$name"; fi; \
		done; \
	done
