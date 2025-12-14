.PHONY: build deploy clean patch help run

# Default target
help:
	@echo "Usage:"
	@echo "  make build   - Build with pygbag and apply patches"
	@echo "  make deploy  - Build, patch, and push to GitHub"
	@echo "  make patch   - Apply iOS Safari fix to docs/index.html"
	@echo "  make run     - Run locally with python"
	@echo "  make clean   - Remove build directory"

# Run locally
run:
	python3 main.py

# Build with pygbag
build:
	@echo "==> Building with pygbag..."
	pygbag --build .
	@echo "==> Copying build files to docs/..."
	cp -r build/web/* docs/
	@echo "==> Applying patches..."
	$(MAKE) patch
	@echo "==> Build complete!"

# Apply iOS Safari touch fix patch
patch:
	@echo "==> Patching docs/index.html..."
	python3 scripts/patch_index.py
	@echo "==> Patch complete!"

# Full deploy: build, patch, commit, and push
deploy:
	@echo "==> Starting deploy process..."
	$(MAKE) build
	@echo "==> Committing changes..."
	git add .
	git commit -m "Deploy: $$(date '+%Y-%m-%d %H:%M:%S')" || echo "Nothing to commit"
	@echo "==> Pushing to GitHub..."
	git push
	@echo "==> Deploy complete!"
	@echo ""
	@echo "Check: https://moohoorama.github.io/kshdraw/"

# Clean build directory
clean:
	@echo "==> Cleaning build directory..."
	rm -rf build/
	@echo "==> Clean complete!"
