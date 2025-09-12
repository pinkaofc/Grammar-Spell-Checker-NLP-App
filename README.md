
## 📘 Grammar & Spell Checker NLP App

A Flask-based web application that corrects grammar and spelling errors using NLP models powered by Hugging Face Transformers and TextBlob. Containerized with Docker for seamless deployment.

---

### 🚀 Features

- ✅ Grammar and spelling correction using deep learning
- ✅ Web interface built with Flask
- ✅ NLP powered by Transformers, Torch, and TextBlob
- ✅ Dockerized for consistent deployment
- ✅ Real-time text correction with intuitive UI

---

### 🧠 Technologies Used

| Tool/Library     | Purpose                              |
|------------------|---------------------------------------|
| Python 3.10      | Core programming language             |
| Flask            | Web framework                         |
| Hugging Face     | Transformer-based NLP models          |
| Torch            | Deep learning backend                 |
| TextBlob         | Grammar and spelling correction       |
| Docker           | Containerization and deployment       |

---

### 📦 Installation (Local)

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/grammar-spell-checker.git
cd grammar-spell-checker
```

#### 2. Build the Docker image

```bash
docker build -t grammar-spell-checker .
```

#### 3. Run the container

```bash
docker run -p 5000:5000 grammar-spell-checker
```

#### 4. Open in browser

```
http://localhost:5000
```

---

### 🧪 Sample Input

```
He dont has no idea how many informations was missing from the report.
```

### ✅ Output

```
He doesn't have any idea how much information was missing from the report.
```

---

### 🌐 Live Demo (Optional)

> Coming soon: [https://grammar-checker.onrender.com](#)

---

### 📁 Project Structure

```
grammar-spell-checker/
├── app.py
├── Model.py
├── templates/
│   └── index.html
├── Dockerfile
├── requirements.txt
└── README.md
```

---

### 🧰 Developer Notes

- Debug mode is enabled for development
- For production, consider using Gunicorn or uWSGI
- NLP model can be swapped or fine-tuned for custom grammar rules

---

### 📣 Connect with Me

Built with ❤️ by [Priyanka](https://www.linkedin.com/in/your-profile)

