# 🏦 Python Command-Line ATM Application

A robust, console-based **Python ATM application** designed to simulate real-world retail banking operations. Built with a modular, clean-code architecture, this system manages secure user authentication, multi-account processing, transaction handling, and persistent data storage using lightweight file streams.

This project showcases fundamental software engineering practices including the separation of concerns, secure state management, data serialization, and defensive input validation.

---

## 🚀 Key Features

* **🔒 Secure Authentication:** Implements custom PIN creation and encryption validation protocols using Python’s native `hashlib` to obfuscate sensitive user credentials.
* **💾 Persistent CSV Ledger:** Maintains a reliable, local database infrastructure using flat files (`accounts.csv` and `account_balances.csv`) to preserve user profiles, encrypted credentials, and current balances across system restarts.
* **💸 Core Banking Transactions:** Supports full transactional capabilities including real-time balance inquiries, cash deposits, verified cash withdrawals (with automatic overdraft/insufficient funds checks), and simulated Electronic Funds Transfers (EFT) between user accounts.
* **📋 Centralised Audit Logging:** Generates automated, timestamped system logs written dynamically to an external ledger (`log.csv`) for structural monitoring, system safety, and transaction history tracking.
* **🛡️ Defensive Error Handling:** Engineered with custom verification blocks to parse human inputs securely, avoiding terminal application crashes from bad menu prompts or malformed currency digits.

---

## 📁 Repository Structure

```text
├── accounts.py             # User account data definitions, PIN validation, and hashing mechanisms
├── account_balances.csv   # Flat-file ledger storing active checking/savings balances
├── log.csv                # System audit logs tracking complete transaction execution paths
├── main.py                # Main runtime engine, loop coordinator, and console UI controller
├── transactions.csv       # Relational record keeping for successful peer-to-peer transfers
└── transactions.py        # Core transactional business logic (withdrawals, deposits, transfers)
```

---

## 🛠️ Technical Focus & Architecture

* **Modular Domain Separation:** The codebase strictly decouples user identity logic (`accounts.py`) from transaction state processing (`transactions.py`), ensuring that functional updates to one module don't degrade the reliability of another.
* **File I/O Data Streams:** Built leveraging Python's internal `csv` ecosystem to handle lightweight atomic writes and read operations, effectively simulating database transactions within local environments.
* **Cryptographic Baselines:** Utilises secure, one-way cryptographic functions to handle credential verification, ensuring user credentials are never stored or exposed in plain text inside the configuration files.

---

## 💻 Getting Started

### Prerequisites
* **Python 3.10 or higher** installed on your operating system.
* Standard environment terminals (Bash, Zsh, Command Prompt, or PowerShell).

### Installation & Execution
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com
   cd python-atm-app
   ```

2. Run the application from the project root folder:
   ```bash
   python main.py
   ```

3. Follow the console prompts to log in, register a simulated bank account, or perform financial transactions.
