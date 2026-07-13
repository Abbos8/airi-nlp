# P16: Render'dagi LSTM sentiment xizmati

Bu papka P16 o'qituvchi demosining deployment loyihasi. Avvalgi capstone'dagi
PyTorch `LSTMClassifier` tayyor artefakt sifatida FastAPI xizmatiga yuklanadi.
Docker bir xil runtime beradi, GitHub Actions CI/CT'ni, Render esa CD'ni bajaradi.

## Arxitektura

- `artifacts/lstm-v1`: tasdiqlangan model og'irliklari, vocabulary va metadata;
- `p16_service`: `/health`, `/version`, `/predict`, `/batch`, `/metrics` API;
- `p16-ci.yml`: testlar va Docker build;
- `p16-train-lstm.yml`: manual training, quality gate va candidate artefakt;
- `render.yaml`: CI o'tgan `main` commitini Render'ga deploy qilish.

Xizmat ishga tushganda modelni CPU'ga bir marta yuklaydi. Har bir request'da
model qayta o'qitilmaydi yoki tashqi model serveridan yuklanmaydi.

## Lokal tekshiruv

Repository ildizidan:

```bash
python -m pip install -r deployment/p16/requirements-dev.txt
PYTHONPATH="$PWD:$PWD/deployment/p16" pytest -q deployment/p16/tests
docker build -t p16-sentiment deployment/p16
docker run --rm -p 7860:7860 p16-sentiment
```

Keyin `http://localhost:7860/docs` yoki `http://localhost:7860/health` ni oching.

## Render'ga deploy

1. Render Dashboard'da **New -> Blueprint** ni tanlang.
2. Public GitHub repository'ni ulang.
3. Render repository ildizidagi `render.yaml` faylini o'qiydi.
4. Blueprint'ni tasdiqlang; secret yoki API key kerak emas.
5. Deploy tugagach xizmat `https://airi-nlp-p16.onrender.com` da ishlaydi.

`autoDeployTrigger: checksPass` sababli `main` branch'dagi P16 CI muvaffaqiyatli
tugagandan keyingina Render yangi commitni deploy qiladi. Free instance uyqudan
uyg'onganda birinchi request odatdagidan sekinroq bo'lishi mumkin.

## Continuous training va promotion

GitHub'da **Actions -> P16 - CT train LSTM candidate -> Run workflow** ni ishga
tushiring. Workflow modelni o'qitadi, F1 va latency quality gate'ini tekshiradi
hamda o'tgan candidate'ni 7 kunlik Actions artefakti sifatida saqlaydi.

Production promotion avtomatik emas: candidate'ni ko'rib chiqing, uning
fayllarini `artifacts/lstm-v1` ga joylang va alohida commit qiling. CI shu commitni
tekshiradi; Render esa tekshiruvdan keyin deploy qiladi.

## Rollback

Render Dashboard'da service'ning **Events** bo'limini oching, oldingi
muvaffaqiyatli deployni tanlang va **Rollback** ni bosing. Render oldingi build
artefaktini qayta ishga tushiradi. Git commit tarixi o'sha deploydagi model,
dataset va kod lineage'ini tiklashga yordam beradi.

## Endpointlar

- `GET /health`: xizmat va yuklangan model holati;
- `GET /version`: model, dataset va revision lineage;
- `POST /predict`: bitta matn tasnifi;
- `POST /batch`: 1-32 matn tasnifi;
- `GET /metrics`: request, xato, latency va confidence signallari.
