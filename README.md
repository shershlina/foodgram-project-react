# foodgram
Project that allow you making your own cooking book and share it with community.

### How to launch the project:

Clone the repository and open it through terminal.
In some cases you need to use "python" instead of "python3".

Create and activate virtual environment:
* If you have Linux/macOS

    ```
    python3 -m venv env 
    source env/bin/activate
    ```

* If you have windows

    ```
    python3 -m venv venv
    source venv/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Install all requirements from requirements.txt file:

```
pip install -r requirements.txt
```

Change the directory:

```
cd .\backend\
```

Make migrations:

```
python3 manage.py migrate
```

Fill the database with test data:
* If you want to upload a lot of ingredients:
  ```
  python3 manage.py import_csv
  ```
  
Run the project:

```
python3 manage.py runserver
```

In the second terminal you can run the frontend part of the project:

Change the directory:
```
cd .\frontend\
```
Install requirements:
```
npm i --legacy-peer-deps
```
If you see some critical vulnerabilities:
```
npm audit fix --force
```
Then start:
```
npm start
```
