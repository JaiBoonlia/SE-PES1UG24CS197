# Lab 5: Static Code Analysis — Reflection

### 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, and coding-style violations. It helps developers detect problems early and improve code quality and maintainability.

### 2. What did Pylint, Bandit, and Flake8 identify?

Pylint identified issues such as missing docstrings, mutable default arguments, broad exception handling, global statements, and unsafe file-handling practices. Bandit identified the use of ordinary pseudo-random number generation and a silent exception handler. Flake8 identified formatting violations, including excessive line lengths, insufficient blank lines, and bare exception handlers.

### 3. What changes were made to improve the program?

The program was updated to use a safer random-number generator, validate vehicle plates and parking zones, handle exceptions more explicitly, use context managers for file operations, validate expiry dates, follow Python naming conventions, and include docstrings. The changes were checked using all three static analysis tools.

### 4. How does static analysis contribute to software quality?

Static analysis helps identify problems before deployment, improves consistency and readability, and highlights potentially unsafe coding practices. However, a clean analysis report does not guarantee that a program is free of functional bugs. Runtime testing is still necessary.
