# 🚀 NodeHire: The AI-Assisted Freelance Ecosystem

NodeHire is a secure, intelligent freelance marketplace that bridges the trust gap between clients and developers. Featuring sandboxed escrow payments, AI project scoping, and a built-in developer community.

## ✨ Key Features
* **🛡️ Secure Escrow Sandbox:** Funds are held securely and released only upon simulated deliverable submission.
* **🤖 AI Project Scoper:** Translates vague client ideas (e.g., "I need a store app") into structured, technical job briefs instantly.
* **💬 Real-Time Encrypted Chat:** Cross-tab messaging system for seamless client-freelancer communication.
* **🎖️ AI Skill Verification:** Freelancers can take assessments to earn verified skill badges for their portfolios.
* **🌐 Community Hub:** Features a live public feed, mentorship matching, and weekly coding challenges.

## 🛠️ Tech Stack
* **Frontend:** Vanilla HTML5, CSS3, JavaScript (Zero dependencies)
* **Backend:** Python, FastAPI
* **Database:** MySQL 
* **State Management:** Browser LocalStorage API (for chat, financials, and portfolio sync)

## ⚙️ How to Run Locally (Demo Mode)

### 1. Database Setup
1. Ensure MySQL is running on your machine.
2. Import the provided SQL schema and seed data to create the `nodehire_db`.
3. *Note: Ensure your database has at least one Client (ID: 1) and one Freelancer (ID: 2) to prevent foreign key constraints when posting jobs.*

### 2. Backend Server
1. Navigate to your backend directory.
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload