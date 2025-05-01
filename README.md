 # AI-Powered QA Automation for TODO App
 This repository demonstrates a fully automated QA pipeline for a TODO application (frontend in React, backend in .NET), where AI is used to discover, formalize and document requirements and tests through prompt engineering.
 
 ## 📁 Repository Structure
 ```bash
 ├── TodoApi/
 │   ├── Controllers/
 │   ├── Models/
 │   ├── prompt_engineering/
 │   │   ├── prompts/
 │   │   │   ├── doc_prompt.md
 │   │   │   ├── testcases_prompt.md
 │   │   │   └── userstories_prompt.md
 │   │   └── responses/
 │   │       ├── doc_response.md
 │   │       ├── testcases_response.md
 │   │       └── userstories_response.md
 │   └── TodoApi.csproj
 ├── todo-client/
 │   ├── public/
 │   ├── src/
 │   ├── scripts/
 │   │   ├── generate_user_stories_selenium.py
 │   │   ├── generate_test_cases_selenium.py
 │   │   ├── generate_documentation_selenium.py
 │   │   ├── run_tests.sh
 │   │   └── test_todo_app.py
 │   └── docs/
 │       ├── USER_STORIES.md
 │       ├── TEST_CASES.md
 │       └── TECHNICAL_DOCUMENTATION.md
 ├── .gitignore
 └── README.md
 ```
 
 ## 🚀 Getting Started
 
 **1. Backend**
    
   ```bash
   cd TodoApi
   dotnet run
   # should listen on http://localhost:5141
   ```
 
 **2. Frontend**
 
   ```bash
   cd todo-client
   npm install
   npm start
   # should serve at http://localhost:3000
   ```
 
 **3. Run the automated tests**
 
   ```bash
   cd todo-client
   bash scripts/run_tests.sh
   ```
 
 ## 🛠️ QA Automation
 
 All end-to-end tests are implemented with **Selenium** and **pytest**. A unique username is generated on each run to avoid collisions and ensure idempotency.
 
 ## 🤖 AI & Prompt Engineering
 
 We leverage AI both in the **frontend** and the **backend** to bootstrap and maintain our QA artifacts:
 
 1. **Frontend** (**React** – ```todo-client```)
 
   * **Prompts** (scripts invoking the AI):
 
     * ```scripts/generate_user_stories_selenium.py```
 
     * ```scripts/generate_test_cases_selenium.py```
 
     * ```scripts/generate_documentation_selenium.py```
 
   * **Responses** (AI outputs stored here):
 
     * ```docs/USER_STORIES```
 
     * ```docs/TEST_CASES```
 
     * ```docs/TECHNICAL_DOCUMENTATION```
 
 2. **Backend** (**.NET** – ```TodoApi```)
 
   * **Prompts** (HTTP or script files):
 
     * ```prompt_engineering/prompts/generate_user_stories.md```
 
     * ```prompt_engineering/prompts/generate_test_cases.md```
 
     * ```prompt_engineering/prompts/generate_documentation.md```
 
   * **Responses** (AI-generated markdown):
 
     * ```prompt_engineering/responses/userstories_response.md```
 
     * ```prompt_engineering/responses/testcases_response.md```
 
     * ```prompt_engineering/responses/doc_response.md```
 
 With this approach, AI helps us to:
 
   * **Elicit** and **structure** user stories
 
   * **Design** robust end-to-end test scenarios
 
   * **Produce** up-to-date technical documentation
 
   * **Keep** our QA pipeline agile and repeatable
 
 **Enjoy a smarter, AI-driven QA workflow!**
 
 ## 📄 License
 
 This project is under MIT license.
