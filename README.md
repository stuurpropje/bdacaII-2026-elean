# Big Data and Automated Content Analysis II – Starter Project

This project serves as a template repository for students to set up their own
projects. When creating your own repository from this template, please ensure
that it is set to **private**.

Follow the steps carefully. You do **not** need to know anything about Python or
programming.

---

## Repository Structure

Your project follows this organization:

- **README.md** – Short description of the project, research question, and how
  to open/run notebooks
- **notebooks/** – All Jupyter notebooks, numbered in the rough order they
  should be run
- **data/raw/** – Original data files (if small and shareable) or a text file
  explaining how to obtain them
- **data/processed/** – Cleaned data you actually analyze
- **tables/** – Final plots/tables you might include in the report

---

## Before You Start

This guide helps you get everything ready to work with Python.

- **Part A – First-time setup:** Steps 1–5 (you only do these once)
- **Part B – Everyday work:** Steps 6–8 (you'll use these later)

If something doesn’t work, don’t worry. You can always return to this file and
follow the steps again.

---

## Part A. First-Time Setup (Do This Once)

### Step 1. Install the required programs

You only do this once. These programs let you write code, manage files, and run
Python.

---

#### 1. Visual Studio Code

Visual Studio Code (VS Code) is the program you’ll use to write and run Python.

1. Go to [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Download the version for your computer (Windows, macOS, or Linux)
3. Open the downloaded file and follow the installation steps
4. When VS Code opens, it may ask to install the **Python** and **Jupyter**
   extensions — click **Install**

If it does not ask:

- Click the **Extensions** icon on the left (it looks like four squares)
- Search for **Python** and click **Install**
- Search for **Jupyter** and click **Install**
- Search for **Data Wrangler** and click **Install**
- Search for **GitHub Pull Requests** and click **Install**

**Check your setup:** In VS Code, open the left sidebar and click the
**Extensions** icon (four squares). You should see green checkmarks next to the
installed extensions. If not, install them now.

---

#### 2. Git

Git allows you to download your personal project and save your work.

**Windows:**

1. Go to [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Download the file and open it
3. Keep clicking **Next** until the installation finishes

**macOS:**

1. Open the **Terminal** app (search for “Terminal” in Spotlight)
2. Type:

   ```bash
   xcode-select --install
   ```

3. Press Enter and follow the prompts

**Linux (Ubuntu or similar):**

```bash
sudo apt install git
```

After installing Git, close and reopen your terminal. If the `git` command still
doesn’t work, restart your computer once.

---

#### 3. uv

`uv` installs Python and all the packages you need. It is safe and will not
change anything else on your computer.

**Windows:**

1. Click the Start Menu and type **PowerShell**
2. Right-click **Windows PowerShell** → choose **Run as administrator**
3. Paste this command and press Enter:

   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   ```

4. Wait until it finishes, then close PowerShell

**macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Important:** After installing `uv`, you must **completely close and reopen VS
Code** (not just the terminal). This allows your system to recognize the new
`uv` command.

If the `uv` command still isn't found after reopening VS Code, restart your
computer once.

---

### Step 2. Create a GitHub account and sign in

GitHub is where your project lives online. You need an account to access your
work.

#### Create a GitHub account (if you don't have one)

1. Go to [https://github.com/](https://github.com/)
2. Click **Sign up**
3. Follow the steps to create a free account
4. Use your **student email address** if possible (this may give you access to
   free features)

#### Sign in to GitHub in VS Code

You need to connect VS Code to your GitHub account so you can download and
upload your work.

1. Open VS Code
2. Click the **Accounts** icon in the bottom-left corner (it looks like a
   person)
3. Click **Sign in with GitHub**
4. Your browser will open — click **Authorize Visual-Studio-Code**
5. Return to VS Code — you should now see your GitHub username in the
   bottom-left

**Alternative method if the above doesn't work:**

1. Press **Ctrl+Shift+P** (Windows/Linux) or **Cmd+Shift+P** (Mac)
2. Type **GitHub: Sign In** → press Enter
3. Follow the browser prompts to sign in

Once you're signed in, you're ready to work with your project.

---

### Step 3. Get your personal project

You will create your own copy of the course project by **using this template**
repository.

1. You are already in the template repository. Now, create your own copy by
   following the steps below.
2. Click the green **"Use this template"** button on the repository page.
3. On the next page, make sure your username is selected as the owner.
4. **Important:** Change the repository name to `bdacaII-year-name` (replace
   "year" with the current year and "name" with your name, e.g.,
   `bdacaII-2026-maria`).
5. Ensure the repository is set to **private**.
6. Click **Create repository**.

You now have your own copy of the project! Next, share it with your instructor:

Go to Settings -> Collaborators and Teams -> Manage access -> Add people ->
_GITHUB USERNAME OF INSTRUCTOR_ -> give Write access

You will now open it in Visual Studio Code.

1. On this GitHub page, click the green **Code** button
2. Choose **Open with Visual Studio Code**

If that option doesn’t appear:

- Click the small arrow next to **Code**
- Copy the HTTPS link

Then:

1. Open VS Code
2. Press **Ctrl+Shift+P** (Windows/Linux) or **Cmd+Shift+P** (Mac)
3. Type **Git: Clone** → press Enter
4. Paste the link you copied and press Enter
5. Choose a folder on your computer (e.g. Documents)
6. When VS Code asks, click **Open**
7. When VS Code asks if you **trust the authors**, click **Yes** (this allows
   notebooks to run).

You should now see your project folder (e.g. `bdacaII-2026-maria`) and files
like `start-here.ipynb` on the left.

If you see a blank VS Code window, click **File → Open Folder...** and select
your project folder manually.

---

### Step 4. Set up Python for the project

Now you will install Python and all needed packages.

1. In VS Code’s top menu, click **Terminal → Run Task...**
   - If you don’t see this, look at the top menu bar (next to File and Edit),
     not inside the terminal window.

2. Choose **Setup Python env (uv)** Continue without scanning the task output
3. Wait a few minutes (the first setup can take time)
4. When it finishes, a folder named `.venv` will appear in your project. That
   means it worked.

If you see a message like _“No Python interpreter found”_, click **Select Python
Interpreter** and choose `.venv/bin/python` (Mac/Linux) or
`.venv\\Scripts\\python.exe` (Windows).

If you see an error, close VS Code, reopen it, and try again. And check section 8, 
it talks about the most common errors!

---

### Step 5. Test that it works

1. In VS Code, open the file **`start-here.ipynb`**
2. In the top-right corner, check which Python environment is selected. It
   should say **py-class**. If not:
   - Click the kernel name in the top-right corner
   - If you don't see **py-class** immediately, first click **Python
     Environments**
   - Then select **py-class** from the list

   _(This is called the kernel — it's just the Python setup for your notebook.)_

3. Click **Run All** at the top, or press **Shift + Enter** to run the notebook.

If everything is correct, you will see:

- printed Python and package versions,
- small charts and text outputs,
- a summary telling you everything is ok.

Your setup is now complete.

---

## Part B. Everyday Work (Use These Later)

### Step 6. Save and upload your work

In this course, saving your work happens in two parts:

1. **Commit** – saves your changes on your computer
2. **Push** – uploads your work to GitHub so your instructor can see it

Steps:

1. Click the **Source Control** icon on the left (three connected dots)
2. Write a short message, e.g. `finished exercise 1`
3. Click the **checkmark** to commit
4. Click the **three dots (...) → Push** to upload

Repeat this whenever you have made updates to your code you would like to save.

---

### Step 7. Add extra Python libraries (if needed)

If you need additional Python packages for your project, you can add them
easily.

1. In VS Code, open a terminal (**Terminal → New Terminal**)
2. Type the following command and press Enter:

   ```bash
   uv add package-name
   ```

   Replace `package-name` with the actual package you need (e.g.,
   `uv add beautifulsoup4`)

3. Wait for the installation to complete
4. The files `pyproject.toml` and `uv.lock` will be automatically updated

**Important:** After adding new packages, commit and push the changes:

1. Go to **Source Control** on the left
2. You should see `pyproject.toml` and `uv.lock` listed as changed files
3. Write a message like `added beautifulsoup4 package`
4. Click the **checkmark** to commit
5. Click **three dots (...) → Push** to upload

This ensures your instructor and anyone else using your project will have the
same packages.

**To add multiple packages at once:**

```bash
uv add package1 package2 package3
```

---

### Step 8. If something goes wrong

Most problems can be fixed easily.

| Problem                              | What to do                                                                   |
| ------------------------------------ | ---------------------------------------------------------------------------- |
| VS Code says it cannot find Python   | Close VS Code completely and reopen it, then run the setup task again        |
| The command `uv` is not found        | **Close VS Code completely** (not just terminal) and reopen it               |
|                                      | If still not working: restart your computer                                  |
|                                      | On Mac, if still failing, see "Mac: zsh command not found" below             |
| The setup task fails                 | Delete the `.venv` folder, then run the setup task again                     |
| The notebook will not run            | Make sure the environment in the top right says **py-class**                 |
| Strange error messages               | Close VS Code, reopen, and rerun the setup task                              |
| Nothing works anymore                | Delete your project folder and clone your forked repository again            |
| **Mac: zsh command not found**       | Open a new terminal in VS Code and run these commands:                       |
|                                      | `source ~/.zshrc`                                                            |
|                                      | If that doesn't work, run: `export PATH="$HOME/.local/bin:$PATH"`            |
|                                      | Then try `uv --version` to check if it works                                 |
| On Windows: If PowerShell shuts down | In PowerShell: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`         |
|                                      | Press `y` and Enter, then run: `irm https://astral.sh/uv/install.ps1 \| iex` |

If you are unsure, take a screenshot and ask your instructor.

---

## Quick Reference

| Task                   | What to Do                                       |
| ---------------------- | ------------------------------------------------ |
| First setup            | Steps 1–5                                        |
| Open project next time | Open VS Code → File → Open Folder → your project |
| Run notebooks          | Open `.ipynb` → check **py-class** → Run All     |
| Save progress          | Source Control → Commit → Push                   |
| Update project         | Source Control → Pull → Run setup task           |
| Add Python packages    | Terminal → uv add package-name → Commit → Push   |
| Fix errors             | See Step 8                                       |

---

## Notes for Students

- Always open your `.ipynb` notebooks in VS Code.
- Do not install anything manually with `pip` or `conda`. Everything is handled
  by `uv`.
- You can delete and rebuild your environment (`.venv`) anytime using the setup
  task.
- Save and push your work regularly so it is backed up online.

---

## Notes for the Instructor

This setup uses `uv` for reproducible environments and local installation.
Students can use it on any operating system without needing Anaconda or system
Python.

### To test the template

1. Clone the repo fresh
2. Run the setup task
3. Open `start-here.ipynb`
4. Verify that the notebook runs without errors

If you need to reset your own environment, delete `.venv` and run `uv sync`
again.
