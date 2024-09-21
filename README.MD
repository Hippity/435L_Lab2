# Python Application

### 1. Create a Virtual Environment

#### For Windows
1. Open Command Prompt or PowerShell.
2. Run the following command to create the virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```

#### For macOS
1. Open Terminal.
2. Run the following command to create the virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

### 2. Install the Required Libraries

Once the virtual environment is activated, install the required libraries using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Run the Application

With the virtual environment activated and dependencies installed, you can run the application:

#### For Windows
```bash
python appTkinter.py
```
```bash
python appPYQT.py
```

#### For macOS
```bash
python3 appTkinter.py
```
#### For macOS
```bash
python3 appPYQT.py
```