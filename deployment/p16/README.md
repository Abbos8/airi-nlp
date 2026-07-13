---
title: Uzbek Sentiment MLOps
sdk: docker
app_port: 7860
---

# P16: Uzbek sentiment xizmati

Bu papka P16 o'qituvchi demosining haqiqiy deployment loyihasi. Bitta FastAPI
xizmati ikki almashtiriladigan backendni qo'llaydi:

- kichik PyTorch LSTM;
- fine-tune qilingan `distilbert-base-multilingual-cased`.

Xizmat ishga tushganda faqat `deployment.json` da tanlangan modelni yuklaydi.
Model har bir so'rovda qayta yuklanmaydi.

## Lokal tekshiruv

```bash
python -m pip install -r deployment/p16/requirements-dev.txt
cd deployment/p16
pytest -q
uvicorn p16_service.app:app --host 0.0.0.0 --port 7860
```

## Endpointlar

- `GET /health`: xizmat va yuklangan model holati;
- `GET /version`: model, dataset va revision lineage;
- `POST /predict`: bitta matn tasnifi;
- `POST /batch`: 1-32 matn tasnifi;
- `GET /metrics`: so'rovlar, xatolar, latency va confidence alert.

## GitHub sozlamalari

Repository secret:

- `HF_TOKEN`: faqat kerakli model va Space repolariga yozish huquqli token.

Repository variables:

- `HF_MODEL_REPO`: masalan, `username/uzbek-sentiment-lstm`;
- `HF_SPACE_ID`: masalan, `username/uzbek-sentiment-api`;
- `HF_DATASET_REPO`: dataset repo ID;
- `HF_DATASET_REVISION`: o'qitishda ishlatilgan aniq commit SHA.

`P16 - Train LSTM and deploy` workflow LSTMni o'qitadi, quality gate'dan
o'tkazadi, modelni Hub'ga yuboradi va Space'ni yangilaydi. `P16 - Deploy or
rollback` esa mavjud model revisionini deploy qilish yoki avvalgi revisionga
qaytish uchun ishlatiladi.

Datasetni birinchi marta Hub'ga chiqarish:

```bash
python deployment/p16/training/publish_dataset.py \
  --file practices/d14_checkpoints/uz_sentiment_mini.jsonl \
  --repo username/uzbek-sentiment-p16 \
  --token "$HF_TOKEN"
```

Buyruq chiqargan commit SHA qiymatini `HF_DATASET_REVISION` variable sifatida
saqlang. CT workflow aynan shu revisionni yuklaydi.
