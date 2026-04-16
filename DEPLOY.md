# 🚀 Οδηγός Deploy — Ιδέες App

## Δομή project
```
idees-app/
├── app.py           ← Flask backend
├── wsgi.py          ← Entrypoint για Railway
├── requirements.txt ← Python πακέτα
├── Procfile         ← Οδηγίες εκκίνησης για Railway
├── .gitignore
└── templates/
    └── index.html   ← Frontend
```

---

## Βήμα 1 — Δημιουργία GitHub repository

1. Πήγαινε στο https://github.com/new
2. Όνομα: `idees-app` (ή ό,τι θες)
3. Visibility: **Private** (αν θες μόνο εσύ να το βλέπεις)
4. Πάτα **Create repository**
5. Στον υπολογιστή σου, άνοιξε terminal μέσα στον φάκελο `idees-app/` και τρέξε:

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ΤΟ_USERNAME_ΣΟΥ/idees-app.git
git push -u origin main
```

---

## Βήμα 2 — Deploy στο Railway

1. Πήγαινε στο https://railway.app
2. Πάτα **New Project → Deploy from GitHub repo**
3. Διάλεξε το `idees-app` repository
4. Railway θα το ανιχνεύσει αυτόματα ως Python app

---

## Βήμα 3 — Προσθήκη PostgreSQL βάσης

1. Μέσα στο project στο Railway, πάτα **+ New Service**
2. Διάλεξε **Database → PostgreSQL**
3. Railway θα φτιάξει αυτόματα μια βάση

---

## Βήμα 4 — Σύνδεση βάσης με app

1. Πήγαινε στο **service του app** (όχι της βάσης)
2. Πάτα **Variables** tab
3. Πάτα **+ New Variable** και γράψε:
   - Name: `DATABASE_URL`
   - Value: πάτα **Add Reference → PostgreSQL → DATABASE_URL**
4. Πάτα **Save** — το Railway κάνει αυτόματα redeploy

---

## Βήμα 5 — Generate domain

1. Στο service του app, πάτα **Settings**
2. Κάτω από **Networking**, πάτα **Generate Domain**
3. Σου δίνει URL τύπου `https://idees-app-xxxx.up.railway.app`

✅ Έτοιμο! Η εφαρμογή σου τρέχει live.

---

## Τοπικό τεστ (προαιρετικό)

```bash
pip install -r requirements.txt
export DATABASE_URL="postgresql://user:pass@localhost/idees"
python app.py
```

Άνοιξε http://localhost:5000

---

## Αν θες να κάνεις αλλαγές αργότερα

```bash
git add .
git commit -m "αλλαγές"
git push
```
Το Railway κάνει αυτόματα redeploy μόλις κάνεις push! 🎉
