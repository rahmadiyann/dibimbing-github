# Definisikan variabel
SCRIPT = run.sh
OUTPUT = output.txt

# Target default
all: help

# Target untuk menjalankan script Bash
run-script: $(SCRIPT)
	@echo "Menjalankan script Bash..."
	bash $(SCRIPT)

# Target untuk membersihkan file output
clean:
	@echo "Membersihkan file output..."
	rm -f $(OUTPUT)

# Target untuk menampilkan pesan bantuan
help:
	@echo "Gunakan 'make run-script' untuk menjalankan script Bash."
	@echo "Gunakan 'make clean' untuk membersihkan file output."
	@echo "Gunakan 'make help' untuk melihat pesan ini."

# contoh:
# make
