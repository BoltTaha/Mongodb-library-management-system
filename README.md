# 📚 Library Management System (MongoDB + Tkinter)

A beginner-friendly **Library Management System** built with **Python**, **MongoDB**, and a **Tkinter GUI**. This project manages books, users, and transactions using modern database operations — ideal for students learning backend + GUI development!

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![MongoDB](https://img.shields.io/badge/MongoDB-Used-brightgreen?logo=mongodb)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-yellow?logo=python)
![Status](https://img.shields.io/badge/Project-Complete-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 🧠 What Makes It Special?

> 🔥 This ain’t your basic file-handling project.
> 🚀 It uses **MongoDB** for real-time database management and a **Tkinter GUI** for better user interaction.

---

## 🎥 Demo

> 🎩 Video demo included! See how it works from start to finish.

[![Watch the video](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](./demo.zip)

> Can’t play it here? [Click to download/watch](./demo.zip)

---

## 💻 Features

* 📗 **Add**, 🧾 **Issue**, ↻ **Return**, ❌ **Delete** books
* 👤 Manage users and transaction history
* 💾 MongoDB handles all data (books, users, logs)
* 🕐 **Time entry** feature to track actions
* 🪟 Clean **Tkinter-based GUI**
* 🧹 Modular, readable Python code

---

## ✨ Tech Stack

| Tech        | Role                     |
| ----------- | ------------------------ |
| Python 🐍   | Core logic + backend     |
| MongoDB 🍃  | NoSQL database           |
| PyMongo 🔗  | MongoDB Connector        |
| Tkinter 🖼️ | Graphical User Interface |

---

## 🛠️ How to Run

1. **Clone the repo:**

   ```bash
   git clone https://github.com/your-username/mongodb-library-management-tkinter.git
   cd mongodb-library-management-tkinter
   ```

2. **Install dependencies:**

   ```bash
   pip install pymongo
   ```

3. **Make sure your MongoDB server is running:**

   * Local MongoDB: Run it via MongoDB Compass or shell
   * OR connect to **MongoDB Atlas** (free cloud DB)

4. **Run the app:**

   ```bash
   python task1.py
   ```

---

## ⚙️ MongoDB Setup Guide

* Use local MongoDB or Atlas.
* Update your MongoDB connection in `task1.py`:

```python
client = pymongo.MongoClient("mongodb://localhost:27017/")  # or your Mongo URI
db = client["library"]
```

* Collections used:

  * `books`
  * `users`
  * `transactions` (optional, for logs)

---

## 📸 Demo Preview

> 🎬 Check out `demo.zip` for a full walkthrough!

---

## 🙌 Contributions

Wanna add cool features like PDF receipts, export buttons, or login screens? Fork it, improve it, and send a pull request!

---

## 📄 License

MIT License

---

Made with 💚 by **Tee (Muhammad Taha)**

> Computer Science Student | MongoDB Enthusiast | Cybersecurity Learner
