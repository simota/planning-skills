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
HOST_DIRS  := $(CLAUDE_DIR) $(CODEX_DIR) $(AGY_DIR)

.DEFAULT_GOAL := help
.PHONY: help check validate test figures figures-full figures-rewrite engines refute render hooks link unlink status

help:
	@echo "make check     validate + test + figures (what CI runs)"
	@echo "make validate  static rules over the corpus"
	@echo "make test      prove every rule still fires"
	@echo "make refute CLAIMS=f.json RUNNING=claude   put each claim to the engines that did not make it"
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

engines:
	@python3 planning-tools/engine.py --selftest

refute:
	@test -n "$(CLAIMS)" || { echo "usage: make refute CLAIMS=claims.json RUNNING=claude"; exit 2; }
	@python3 planning-tools/refute.py --running "$(or $(RUNNING),claude)" "$(CLAIMS)"

render:
	@python3 planning-tools/render.py

figures:
	@python3 planning-tools/figures_check.py

figures-full:
	@python3 planning-tools/figures_check.py --full

figures-rewrite:
	@python3 planning-tools/figures_check.py --rewrite

hooks:
	@mkdir -p .git/hooks
	@cp planning-tools/githooks/pre-commit .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "pre-commit installed"

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
			if [ -L "$$target" ]; then rm "$$target"; echo "  unlink $$name"; fi; \
		done; \
	done

status:
	@for dir in $(HOST_DIRS); do \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -L "$$target" ]; then echo "  linked   $$name"; \
			else echo "  unlinked $$name"; fi; \
		done; \
	done
