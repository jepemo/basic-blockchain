all:
	@echo "If you want the library just installit with pip:"
	@echo "  pip install bbchain"
	@echo ""
	@echo "For development:"
	@echo "  python3 -m venv venv; source venv/bin/activate"
	@echo "  pip3 install -r requirements.txt"

.PHONY: test
test:
	./tests/test_connection.sh
	./tests/test_data.sh
