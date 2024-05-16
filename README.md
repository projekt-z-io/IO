# How to setup this app?

### On docker via the docker image:

1. Pull the Docker image:
    ```bash
    docker pull stachu420/parabank
    ```

2. Run the Docker container:
    ```bash
    docker run -p 5000:5000 stachu420/parabank
    ```

3. Open `localhost:5000` in your web browser.

### Locally:

1. Clone this repository.

2. Make sure you have Python installed.

3. In your command line:

    a. Create a Python virtual environment:
        ```bash
        python3 -m venv env   # or python -m venv env
        ```

    b. Activate the virtual environment:
        - **MacOS & Linux**:
            ```bash
            source env/bin/activate
            ```
        - **Windows**:
            ```bash
            env\Scripts\activate
            ```

        Note: If you encounter an error like "env\Scripts\activate : File C:\path\env\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system. (...)", run Windows PowerShell as an Administrator and execute the following command:
        ```powershell
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
        ```
        Then type: `Y`.

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the application:
    ```bash
    python run.py
    ```

6. Open `localhost:5000` in your web browser.

If the application doesn't work, check if `app.run(debug=True)` is set in `run.py`.

# Post:
If you wish to install additional packages, don't forget to update the `requirements.txt` file by running:
```bash
pip freeze > requirements.txt
