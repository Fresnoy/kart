# 🎨 KART - Information System for Le Fresnoy

**KART** is a Django-based application designed to manage the information system of **artworks** and **events** produced at [Le Fresnoy – Studio national des arts contemporains](https://www.lefresnoy.net).  
It helps organize, archive, and interconnect artistic productions, artists, educational sessions, and exhibitions (past, current, and upcoming).

> This repository provides a *Dockerized* version of the application, making it easy to deploy on a VPS or any environment supporting Docker.

---

## 🖼️ Project Goals

- Manage metadata of artworks produced at Le Fresnoy
- Archive events (exhibitions, screenings, performances)
- Link artworks, artists, academic years, and related documents
- Offer an API for integration with other systems
- Provide a robust admin interface for internal teams

---

## ⚙️ Tech Stack

- **Framework**: Django (Python 3.x)
- **Database**: PostgreSQL
- **Web Server**: Gunicorn + Nginx
- **Containerization**: Docker + Docker Compose
- **Static/Media files**: persistent volumes
- **Security**: user and permission management

---

## 📁 Repository Structure

```
KART/
├── app/                  # Django source code
│   ├── kart/             # Main application
│   └── manage.py
├── nginx/                # Nginx configuration
├── docker/               # Docker files (Dockerfile, entrypoints)
├── docker-compose.yml
├── .env.example          # Environment variable sample
├── requirements.txt
└── README.md
```

---

## 🛠️ Local Installation (via Docker)

1. **Clone the project**
   ```bash
   git clone https://github.com/your-username/KART.git
   cd KART
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit the .env file as needed (secret key, DB, debug, etc.)
   ```

3. **Start containers**
   ```bash
   docker-compose up --build
   ```

4. **Initialize the database**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**
   - App: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

---

## 🐳 VPS Deployment

> You can easily deploy KART to a VPS using Docker Compose:

1. **Prepare the VPS (Git, Docker, Docker Compose)**
2. **Push the code or clone from GitHub**
3. **Configure a production-ready `.env`**
4. **Start in detached mode**
   ```bash
   docker-compose -f docker-compose.yml up -d --build
   ```

5. **Configure Nginx + HTTPS with Certbot**

---

## 🔐 Security Recommendations

- Use a strong `SECRET_KEY`
- Set `DEBUG=False` in production
- Properly configure `ALLOWED_HOSTS`
- Use HTTPS (Let's Encrypt / Certbot)
- Back up the database regularly

---

## 🧪 Running Tests

```bash
docker-compose exec web python manage.py test
```

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to open an issue or pull request to improve features, fix bugs, or enhance the documentation.

---

## 📄 License

Released under the **MIT License** — free to use, modify and distribute.

---

## 🖋️ Authors

Developed by **Le Fresnoy – Studio national des arts contemporains**  
Contact: [poleweb@lefresnoy.net]

