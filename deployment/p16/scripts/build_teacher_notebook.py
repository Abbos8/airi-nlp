from __future__ import annotations

import base64
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT = REPO_ROOT / "practices/d16_p16_mlops_deploy.ipynb"


def markdown(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(True)}


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(True),
    }


def svg_image(alt: str, svg: str) -> str:
    payload = base64.b64encode(svg.encode()).decode()
    return f"![{alt}](data:image/svg+xml;base64,{payload})"


PIPELINE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="980" height="230" viewBox="0 0 980 230">
<rect width="980" height="230" fill="#f7f8fa"/><text x="36" y="38" font-family="Arial" font-size="22" font-weight="700" fill="#17212b">P16: modeldan kuzatiladigan xizmatgacha</text>
<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#65727e"/></marker></defs>
<g font-family="Arial" text-anchor="middle"><g><rect x="34" y="75" width="150" height="92" rx="6" fill="#e5f1ff" stroke="#2878b5"/><text x="109" y="111" font-size="17" font-weight="700" fill="#184d73">Ma'lumot</text><text x="109" y="137" font-size="14" fill="#27333d">dataset revision</text></g>
<g><rect x="226" y="75" width="150" height="92" rx="6" fill="#e9f6ee" stroke="#308451"/><text x="301" y="111" font-size="17" font-weight="700" fill="#205c38">O'qitish</text><text x="301" y="137" font-size="14" fill="#27333d">LSTM / DistilBERT</text></g>
<g><rect x="418" y="75" width="150" height="92" rx="6" fill="#fff2db" stroke="#b56a13"/><text x="493" y="111" font-size="17" font-weight="700" fill="#77450d">Reyestr</text><text x="493" y="137" font-size="14" fill="#27333d">model revision</text></g>
<g><rect x="610" y="75" width="150" height="92" rx="6" fill="#f2eafb" stroke="#7551a6"/><text x="685" y="111" font-size="17" font-weight="700" fill="#513775">FastAPI</text><text x="685" y="137" font-size="14" fill="#27333d">test + metrics</text></g>
<g><rect x="802" y="75" width="144" height="92" rx="6" fill="#ffe9e6" stroke="#b34e43"/><text x="874" y="111" font-size="17" font-weight="700" fill="#79332c">Space</text><text x="874" y="137" font-size="14" fill="#27333d">deploy / rollback</text></g></g>
<g stroke="#65727e" stroke-width="2" marker-end="url(#a)"><path d="M184 121H216"/><path d="M376 121H408"/><path d="M568 121H600"/><path d="M760 121H792"/></g>
<text x="36" y="205" font-family="Arial" font-size="14" fill="#4e5b66">Har bosqichda artefakt, metrika va aniq revision saqlanadi.</text></svg>"""

LINEAGE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="980" height="240" viewBox="0 0 980 240">
<rect width="980" height="240" fill="#f7f8fa"/><text x="36" y="38" font-family="Arial" font-size="22" font-weight="700" fill="#17212b">Bitta model versiyasining kelib chiqishi</text>
<defs><marker id="b" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#65727e"/></marker></defs>
<g font-family="Arial"><rect x="42" y="75" width="210" height="54" rx="6" fill="#e5f1ff" stroke="#2878b5"/><text x="147" y="108" text-anchor="middle" font-size="16">dataset SHA</text><rect x="42" y="151" width="210" height="54" rx="6" fill="#e9f6ee" stroke="#308451"/><text x="147" y="184" text-anchor="middle" font-size="16">Git commit SHA</text>
<rect x="385" y="91" width="210" height="96" rx="6" fill="#fff2db" stroke="#b56a13"/><text x="490" y="126" text-anchor="middle" font-size="17" font-weight="700">MLflow run</text><text x="490" y="154" text-anchor="middle" font-size="14">parametr + metrika</text>
<rect x="728" y="91" width="210" height="96" rx="6" fill="#f2eafb" stroke="#7551a6"/><text x="833" y="126" text-anchor="middle" font-size="17" font-weight="700">Model artefakti</text><text x="833" y="154" text-anchor="middle" font-size="14">model revision SHA</text></g>
<g stroke="#65727e" stroke-width="2" marker-end="url(#b)"><path d="M252 102H374"/><path d="M252 178H374"/><path d="M595 139H717"/></g></svg>"""

CICD_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="980" height="250" viewBox="0 0 980 250">
<rect width="980" height="250" fill="#f7f8fa"/><text x="36" y="38" font-family="Arial" font-size="22" font-weight="700" fill="#17212b">CI / CT / CD: uch xil mas'uliyat</text>
<defs><marker id="c" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#65727e"/></marker></defs>
<g font-family="Arial" text-anchor="middle"><rect x="36" y="78" width="250" height="108" rx="6" fill="#e5f1ff" stroke="#2878b5"/><text x="161" y="113" font-size="20" font-weight="700">CI</text><text x="161" y="141" font-size="15">test + Docker build</text><text x="161" y="165" font-size="13">har bir push</text>
<rect x="365" y="78" width="250" height="108" rx="6" fill="#e9f6ee" stroke="#308451"/><text x="490" y="113" font-size="20" font-weight="700">CT</text><text x="490" y="141" font-size="15">train + quality gate</text><text x="490" y="165" font-size="13">manual yoki yangi dataset</text>
<rect x="694" y="78" width="250" height="108" rx="6" fill="#fff2db" stroke="#b56a13"/><text x="819" y="113" font-size="20" font-weight="700">CD</text><text x="819" y="141" font-size="15">Space deploy</text><text x="819" y="165" font-size="13">tasdiqlangan revision</text></g>
<g stroke="#65727e" stroke-width="2" marker-end="url(#c)"><path d="M286 132H354"/><path d="M615 132H683"/></g><text x="36" y="222" font-family="Arial" font-size="14" fill="#4e5b66">Rollback: CD orqali avvalgi model revisionini qayta tanlash.</text></svg>"""


cells = [
    markdown("""# P16: NLP modelni production xizmatga chiqarish

**O'qituvchi demosiga mo'ljallangan 80 daqiqalik amaliy workshop.** Alohida student yoki solution notebook yo'q.

Bugun bitta to'liq yo'lni bajaramiz: avvalgi capstone LSTMni o'qitamiz, MLflow bilan tajribani qayd qilamiz, FastAPI orqali test qilamiz va GitHub Actions yordamida Hugging Face Docker Space'ga chiqarish oqimini ko'ramiz. Fine-tune qilingan multilingual DistilBERT shu API shartnomasiga ulanadigan ikkinchi backend bo'ladi.

**Natija:** modelning o'zi bilan birga dataset, kod, metrika va deployment revisionlari ham kuzatiladi."""),
    markdown(svg_image("P16 MLOps oqimi", PIPELINE_SVG)),
    markdown("""## 0. Darsni boshlashdan oldin

GitHub'da **Actions -> P16 - Train LSTM and deploy -> Run workflow** ni ishga tushiring. Workflow fonda ishlayotgan paytda lokal oqimni Colab'da quramiz va oxirida tayyor Space endpointini tekshiramiz.

Oldindan GitHub repository variables sifatida `HF_MODEL_REPO`, `HF_SPACE_ID`, `HF_DATASET_REPO`, `HF_DATASET_REVISION`; secret sifatida esa `HF_TOKEN` kiritilgan bo'lishi kerak. Token notebook yoki workflow matnida yozilmaydi."""),
    markdown("""## 1. Colab muhiti va loyiha

Notebook GitHub'dan ochilgan bo'lsa, Colab faqat `.ipynb` faylini oladi. Quyidagi hujayra course repository'ni bir marta clone qiladi. Deployment fayllari notebook tomonidan yaratilmaydi: ular repository'da tayyor va alohida testlanadi."""),
    code("""from pathlib import Path
import subprocess
import sys

REPO_URL = "https://github.com/i-atadjanov/airi-nlp.git"
local_root = Path.cwd()
if not (local_root / "deployment/p16").exists():
    local_root = Path("/content/airi-nlp")
    if not local_root.exists():
        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, str(local_root)], check=True)

REPO_ROOT = local_root.resolve()
DEPLOY_DIR = REPO_ROOT / "deployment/p16"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(DEPLOY_DIR))
print("Repository:", REPO_ROOT)
print("Deployment:", DEPLOY_DIR)"""),
    markdown("""### Kerakli kutubxonalar

- **PyTorch**: LSTM va DistilBERT tensor hisoblari;
- **MLflow**: parametr, metrika, artefakt va lineage'ni run sifatida qayd qilish;
- **FastAPI + Pydantic**: HTTP endpoint va JSON validatsiyasi;
- **Transformers / Datasets**: ixtiyoriy DistilBERT backend va Hugging Face datasetlari;
- **httpx**: lokal yoki public API'ga HTTP so'rov yuborish.

Colab'da PyTorch odatda tayyor. Qolgan versiyalar loyiha requirements faylidan olinadi."""),
    code("""import importlib.util

required = ["torch", "fastapi", "httpx", "mlflow", "transformers", "datasets"]
missing = [name for name in required if importlib.util.find_spec(name) is None]
if missing:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", str(DEPLOY_DIR / "requirements-notebook.txt")],
        check=True,
    )
print("Muhit tayyor. Yetishmagan paketlar:", missing or "yo'q")"""),
    markdown("""### Dars konfiguratsiyasi

LSTM live o'qitiladi. Transformer uchun to'rtta qiymatni ajratamiz:

- `DISTILBERT_BASE_MODEL`: fine-tuning boshlanadigan pretrained checkpoint;
- `DISTILBERT_MODEL_REPO`: tayyor fine-tuned Hugging Face repo;
- `DISTILBERT_REVISION`: repo ichidagi o'zgarmas commit;
- `DISTILBERT_SERVICE_NAME`: API javobida ko'rinadigan qisqa nom.

Tashqi model uchta anonim label beradi. Ushbu binary API uchun `LABEL_0 -> salbiy`, `LABEL_1 -> ijobiy`; neytral `LABEL_2` olib tashlanib, qolgan ehtimollar qayta normallashtiriladi. Bu mapping model kartasida hujjatlashtirilmagan, shuning uchun darsda alohida tekshiriladi."""),
    code("""RUN_LSTM_TRAINING = True
LSTM_EPOCHS = 8

DISTILBERT_BASE_MODEL = "distilbert-base-multilingual-cased"
DISTILBERT_SERVICE_NAME = "external-uzbek-distilbert"
DISTILBERT_MODEL_REPO = "blackhole33/uzbek-sentiment-analysis-v5"
DISTILBERT_REVISION = "89b0997b3e12792942358d95d51023f3fe1ef228"
DISTILBERT_LABEL_MAP = {"LABEL_0": "salbiy", "LABEL_1": "ijobiy", "LABEL_2": None}
RUN_DISTILBERT_EVALUATION = True

SPACE_URL = ""                   # masalan: https://username-space.hf.space
print("Asosiy live backend: LSTM")
print("Tayyor Transformer:", DISTILBERT_MODEL_REPO)
print("Pinned revision:", DISTILBERT_REVISION[:12])"""),
    markdown("""## 2. Datasetni versiyalash

`dataset nomi` yetarli emas: repository ichidagi ma'lumot o'zgarishi mumkin. Lokal snapshot uchun SHA-256, Hugging Face Dataset Hub uchun esa commit revision ishlatamiz. Shunda aynan qaysi misollar modelni hosil qilganini qayta topish mumkin."""),
    code("""from collections import Counter
from deployment.p16.training.common import load_jsonl, sha256_file, stratified_split

DATA_PATH = REPO_ROOT / "practices/d14_checkpoints/uz_sentiment_mini.jsonl"
texts, numeric_labels = load_jsonl(DATA_PATH)
dataset_revision = sha256_file(DATA_PATH)
train_x, train_y, test_x, test_y = stratified_split(texts, numeric_labels)

print("Dataset:", DATA_PATH.name)
print("Revision:", dataset_revision[:16] + "...")
print("Train / test:", len(train_x), "/", len(test_x))
print("Sinflar:", Counter(numeric_labels))"""),
    markdown("""### Datasetni ko'z bilan tekshirish

Versiya takrorlanuvchanlikni beradi, lekin sifatni kafolatlamaydi. Sinf balansi va bir necha matnni ko'rish data pipeline'ning oddiy smoke testidir."""),
    code("""import matplotlib.pyplot as plt

counts = Counter(numeric_labels)
plt.figure(figsize=(6, 3))
plt.bar(["salbiy", "ijobiy"], [counts[0], counts[1]], color=["#b34e43", "#308451"])
plt.title("O'zbek sentiment datasetida sinf balansi")
plt.ylabel("Matnlar soni")
plt.grid(axis="y", alpha=0.2)
plt.show()

for text, label in list(zip(texts, numeric_labels))[:2]:
    print("ijobiy" if label else "salbiy", "->", text)"""),
    markdown("""## 3. Avvalgi capstone LSTMni o'qitish

Bu yerda LSTM qayta implementatsiya qilinmaydi. `m08_gru_lstm_classifier.py` dagi `LSTMClassifier` o'qitiladi. Deployment adapter uning `state_dict`, vocabulary, label va konfiguratsiyasini ochiq artefaktga ajratadi; server pickle qilingan butun Python obyektiga bog'lanib qolmaydi."""),
    code("""from deployment.p16.training.train_lstm import train_lstm

LIVE_ARTIFACT_DIR = Path("/content/p16-lstm-live") if Path("/content").exists() else Path("/tmp/p16-lstm-live")
if RUN_LSTM_TRAINING:
    lstm_result = train_lstm(
        DATA_PATH,
        LIVE_ARTIFACT_DIR,
        epochs=LSTM_EPOCHS,
        hidden_size=64,
        model_version="class-live-v1",
    )
else:
    LIVE_ARTIFACT_DIR = DEPLOY_DIR / "artifacts/lstm-v1"
    import json
    lstm_result = {
        "metrics": json.loads((LIVE_ARTIFACT_DIR / "metrics.json").read_text()),
        "metadata": json.loads((LIVE_ARTIFACT_DIR / "config.json").read_text()),
    }
lstm_result"""),
    markdown("""### Artefakt tarkibi

`model.pt` faqat og'irliklarni saqlaydi. `vocab.json` token IDlarini, `config.json` esa arxitektura, preprocessing, model va dataset revisionlarini saqlaydi. Ularning barchasi bir versiya sifatida yurishi kerak."""),
    code("""import json

for path in sorted(LIVE_ARTIFACT_DIR.iterdir()):
    print(f"{path.name:16} {path.stat().st_size / 1024:8.1f} KB")

lstm_config = json.loads((LIVE_ARTIFACT_DIR / "config.json").read_text())
lineage_keys = [
    "model_name", "model_version", "dataset_repo", "dataset_revision",
    "code_revision", "preprocessing_version",
]
print("\\nLineage:")
for key in lineage_keys:
    print(f"{key:24}: {lstm_config[key]}")"""),
    markdown(svg_image("Model lineage", LINEAGE_SVG)),
    markdown("""## 4. MLflow bilan tajribani qayd qilish

MLflow bu darsda alohida server emas. Colab runtime ichidagi tracking papkasiga run yozamiz va jadval orqali solishtiramiz. Production model reyestri sifatida esa Hugging Face Model Hub ishlatiladi."""),
    code("""import mlflow

MLRUNS_DIR = Path("/content/p16-mlruns") if Path("/content").exists() else Path("/tmp/p16-mlruns")
MLRUNS_DIR.mkdir(parents=True, exist_ok=True)
mlflow.set_tracking_uri(MLRUNS_DIR.as_uri())
mlflow.set_experiment("p16-uzbek-sentiment")

with mlflow.start_run(run_name="lstm-class-live") as run:
    mlflow.log_params({
        "backend": "lstm", "epochs": LSTM_EPOCHS, "hidden_size": 64,
        "dataset_revision": lstm_config["dataset_revision"],
        "code_revision": lstm_config["code_revision"],
    })
    mlflow.log_metrics(lstm_result["metrics"])
    mlflow.log_dict(lstm_config, "lineage.json")
    lstm_run_id = run.info.run_id
print("MLflow run ID:", lstm_run_id)"""),
    markdown("""### Runlarni taqqoslash

MLflow run ID tajribani topadi; model revision esa deployment artefaktini topadi. Bu ikkisi bir xil narsa emas, lekin lineage orqali bir-biriga bog'lanadi."""),
    code("""runs = mlflow.search_runs(experiment_names=["p16-uzbek-sentiment"])
columns = [
    "run_id", "tags.mlflow.runName", "params.backend",
    "metrics.f1", "metrics.accuracy", "metrics.inference_time",
    "metrics.parameter_count", "metrics.artifact_size_mb",
]
available = [column for column in columns if column in runs.columns]
runs[available].head()"""),
    markdown("""## 5. Ikkinchi backend: multilingual DistilBERT

Ikki model bir vaqtda production xotirasiga yuklanmaydi. Ular bir xil `predict_proba(text)` shartnomasini bajaradi, deployment manifest esa bittasini tanlaydi.

- **LSTM:** kichik va tez, CI CPU'da o'qitish mumkin;
- **multilingual DistilBERT:** kattaroq va odatda sifatliroq, fine-tuning uchun GPU ma'qul.

Quyidagi yordamchi funksiya faqat tayyor fine-tune qilingan repo va revision berilganda ikkinchi modelni baholaydi."""),
    code("""import time
from deployment.p16.training.common import classification_metrics

def evaluate_backend(backend, samples, labels):
    started = time.perf_counter()
    predictions = []
    for text in samples:
        probabilities = backend.predict_proba(text)
        predicted_name = max(probabilities, key=probabilities.get)
        predictions.append(1 if predicted_name == "ijobiy" else 0)
    elapsed_ms = (time.perf_counter() - started) * 1000 / len(samples)
    metrics = classification_metrics(labels, predictions)
    metrics["inference_time"] = round(elapsed_ms, 3)
    return metrics"""),
    markdown("""### Tayyor Uzbek DistilBERTni yuklash

Bu model qayta o'qitilmaydi: pinned Hugging Face revision to'g'ridan-to'g'ri yuklanadi. Tashqi modelning label kontrakti bizning binary API kontraktimizdan farq qilgani uchun mapping ochiq konfiguratsiya sifatida beriladi. Natijalar albatta bizning Day 14 test bo'lagimizda qayta o'lchanadi."""),
    code("""from p16_service.backends import DistilBERTBackend
from p16_service.config import Settings

distilbert_metrics = None
if RUN_DISTILBERT_EVALUATION and DISTILBERT_MODEL_REPO and DISTILBERT_REVISION:
    bert_settings = Settings(
        backend="distilbert",
        model_name=DISTILBERT_SERVICE_NAME,
        model_version="candidate-v2",
        model_repo=DISTILBERT_MODEL_REPO,
        model_revision=DISTILBERT_REVISION,
        model_label_map=DISTILBERT_LABEL_MAP,
        dataset_revision=dataset_revision,
    )
    distilbert_backend = DistilBERTBackend(bert_settings)
    print("Raw labels:", distilbert_backend.raw_labels)
    for expected, text in [("ijobiy", "Bu juda ajoyib!"), ("salbiy", "Bu juda yomon!")]:
        probabilities = distilbert_backend.predict_proba(text)
        predicted = max(probabilities, key=probabilities.get)
        print(text, "->", predicted, probabilities)
        assert predicted == expected
    distilbert_metrics = evaluate_backend(distilbert_backend, test_x, test_y)
    print(distilbert_metrics)
else:
    print("DistilBERT baholash o'tkazib yuborildi: tayyor repo/revision kiriting.")"""),
    markdown("""### Qaror faqat F1 bilan qilinmaydi

Model tanlashda sifat, latency, parametrlar va artefakt hajmi birga qaraladi. Jadvalda faqat shu runtime'da real o'lchangan natijalar ko'rsatiladi; uydirma DistilBERT metrikasi qo'shilmaydi."""),
    code("""import pandas as pd

comparison = [{"backend": "LSTM", **lstm_result["metrics"]}]
if distilbert_metrics:
    comparison.append({"backend": "DistilBERT", **distilbert_metrics})
comparison_table = pd.DataFrame(comparison)
comparison_table"""),
    markdown("""## 6. Production backendni yuklash

Server LSTMni o'qitmaydi. U tayyor artefaktni CPU'ga bir marta yuklaydi va barcha so'rovlar uchun shu obyektni qayta ishlatadi."""),
    code("""from p16_service.backends import LSTMBackend

live_settings = Settings(
    backend="lstm",
    model_name=lstm_config["model_name"],
    model_version=lstm_config["model_version"],
    artifact_path=str(LIVE_ARTIFACT_DIR),
    dataset_repo=lstm_config["dataset_repo"],
    dataset_revision=dataset_revision,
    code_revision=lstm_config["code_revision"],
)
live_backend = LSTMBackend(LIVE_ARTIFACT_DIR, live_settings)

for sample in ["Mahsulot juda yaxshi", "Sifatsiz va yomon mahsulot"]:
    print(sample, "->", live_backend.predict_proba(sample))"""),
    markdown("""## 7. FastAPI: modelni HTTP shartnomasiga o'rash

Pydantic bo'sh matnni rad etadi. Javob label va confidence bilan cheklanmaydi: `model_name`, `model_version` va `latency_ms` ham qaytadi. Bu debugging va monitoring uchun kerak."""),
    code("""from fastapi.testclient import TestClient
from p16_service.app import create_app

api = create_app(backend=live_backend, settings=live_settings)
client = TestClient(api)
client.__enter__()

health = client.get("/health")
version = client.get("/version")
print("/health", health.status_code, health.json())
print("/version", version.status_code, version.json())"""),
    markdown("""### `/predict`: haqiqiy model chiqishi

`TestClient` tarmoqsiz to'liq HTTP siklini bajaradi: JSON validatsiyasi, endpoint, model inference va response schema."""),
    code("""response = client.post(
    "/predict",
    json={"text": "Yetkazib berish tez, mahsulot juda yaxshi"},
)
print("Status:", response.status_code)
response.json()"""),
    markdown("""### Noto'g'ri input ham test qilinadi

Production test faqat yaxshi yo'lni tekshirmaydi. Bo'sh matn modelgacha yetib bormasdan `422 Unprocessable Entity` qaytarishi kerak."""),
    code("""bad_response = client.post("/predict", json={"text": "   "})
print("Status:", bad_response.status_code)
print("Detail:", bad_response.json()["detail"][0]["msg"])
assert bad_response.status_code == 422"""),
    markdown("""### `/batch` va `/metrics`

Batch endpoint 1-32 matnni qabul qiladi. Metrics endpoint texnik holatni va confidence taqsimotidagi oddiy signalni ko'rsatadi. `quality_alert` haqiqiy ground-truth sifat o'lchovi emas; u tekshirish kerakligini bildiruvchi signal."""),
    code("""batch = client.post(
    "/batch",
    json={"texts": [
        "Ajoyib sifat, tavsiya qilaman",
        "Bir kunda buzildi, umuman yomon",
        "Mahsulot oddiy ekan",
    ]},
)
print("Batch status:", batch.status_code)
for prediction in batch.json()["predictions"]:
    print(prediction["label"], round(prediction["confidence"], 3), prediction["text"])
print("\\nMetrics:", client.get("/metrics").json())"""),
    markdown("""## 8. Docker: bir xil runtime

FastAPI kirish nuqtasini beradi; Docker Python va kutubxona muhitini takrorlanuvchan qiladi. Modelning katta DistilBERT og'irliklari image ichiga nusxalanmaydi: Space ishga tushganda pinned Hub revision yuklanadi."""),
    code("""from IPython.display import Code, display

dockerfile = (DEPLOY_DIR / "Dockerfile").read_text()
display(Code(dockerfile, language="dockerfile"))"""),
    markdown(svg_image("CI CT CD oqimi", CICD_SVG)),
    markdown("""## 9. GitHub Actions: pipeline'ni avtomatlashtirish

Loyiha uchta workflow beradi:

1. `p16-ci.yml`: har push'da API test va Docker build;
2. `p16-train-lstm.yml`: LSTM continuous training, quality gate, model publish va deploy;
3. `p16-deploy.yml`: tayyor LSTM yoki DistilBERT revisionini deploy qilish va rollback.

DistilBERT fine-tuning oddiy bepul GitHub CPU runner'da majburiy emas; u Colab GPU'da tayyorlanadi, keyin xuddi shu validation/deployment kontraktiga kiradi."""),
    code("""workflow_dir = REPO_ROOT / ".github/workflows"
for name in ["p16-ci.yml", "p16-train-lstm.yml", "p16-deploy.yml"]:
    path = workflow_dir / name
    print(f"{name:24} {len(path.read_text().splitlines()):3} qator")

ci_lines = (workflow_dir / "p16-ci.yml").read_text().splitlines()
display(Code("\\n".join(ci_lines[18:36]), language="yaml"))"""),
    markdown("""### Quality gate

Yangi model avtomatik ravishda production'ga chiqmasligi kerak. CT workflow avval F1 va latency chegaralarini tekshiradi. Chegaradan o'tmagan run artefakt sifatida saqlanishi mumkin, lekin CD bosqichi boshlanmaydi."""),
    code("""quality_gate = (DEPLOY_DIR / "scripts/check_quality.py").read_text().splitlines()
display(Code("\\n".join(quality_gate[10:29]), language="python"))

metrics = lstm_result["metrics"]
approved = metrics["f1"] >= 0.70 and metrics["inference_time"] <= 100
print("Live LSTM deployment qarori:", "TASDIQLANDI" if approved else "RAD ETILDI")"""),
    markdown("""## 10. Public Hugging Face Space'ni tekshirish

Colab doimiy server emas. Public FastAPI Docker Space'da `7860` portda ishlaydi. `SPACE_URL` kiritilgan bo'lsa, quyidagi hujayra real endpoint javobini ko'rsatadi."""),
    code("""import httpx

if SPACE_URL:
    public_health = httpx.get(f"{SPACE_URL.rstrip('/')}/health", timeout=60)
    public_prediction = httpx.post(
        f"{SPACE_URL.rstrip('/')}/predict",
        json={"text": "Mahsulot sifati juda yaxshi"},
        timeout=60,
    )
    print("Public health:", public_health.status_code, public_health.json())
    print("Public output:", public_prediction.status_code, public_prediction.json())
else:
    print("SPACE_URL bo'sh: workflow tugagach public Space URL'ni kiriting.")"""),
    markdown("""## 11. Rollback: oldingi revisionni qayta deploy qilish

Rollback model faylini qo'lda almashtirish emas. GitHub Actions'dagi **P16 - Deploy or rollback** workflow'ga avvalgi `model_revision` SHA beriladi. `deployment.json` aynan shu SHA'ni pin qiladi va Space qayta build bo'ladi."""),
    code("""current_manifest = json.loads((DEPLOY_DIR / "deployment.json").read_text())
rollback_example = {
    **current_manifest,
    "model_version": "v1-stable",
    "model_repo": "username/uzbek-sentiment-lstm",
    "model_revision": "OLD_STABLE_COMMIT_SHA",
}
print(json.dumps(rollback_example, indent=2))"""),
    markdown("""## 12. Yakuniy tekshiruv

Workshop oxirida quyidagi savollarga javob bera olish kerak:

- Qaysi dataset va kod revisioni modelni hosil qildi?
- Nega MLflow run ID va model revision SHA alohida?
- Nega server modelni har request'da yuklamaydi?
- CI, CT va CD nima bilan farq qiladi?
- Nega rollback uchun oldingi artefakt saqlanishi shart?
- LSTM va DistilBERT orasidagi production trade-off nima?"""),
    code("""assert health.status_code == 200
assert response.status_code == 200
assert bad_response.status_code == 422
assert batch.status_code == 200
assert "model_version" in response.json()
assert "p95_latency_ms" in client.get("/metrics").json()
client.__exit__(None, None, None)
print("P16 lokal vertikal oqimi to'liq ishladi. [OK]")"""),
    markdown("""## Appendix: DistilBERTni Colab GPU'da tayyorlash

Asosiy 80 daqiqalik yo'lda bu buyruq bajarilmaydi. Day 14 datasetida fine-tuning qilish uchun GPU runtime tanlanadi:

```bash
python deployment/p16/training/train_distilbert.py \
  --data practices/d14_checkpoints/uz_sentiment_mini.jsonl \
  --output /content/uzbek-sentiment-distilbert \
  --model-name distilbert-base-multilingual-cased \
  --epochs 2 --batch-size 16
```

Bu yerdagi `--model-name` pretrained base checkpointni aniq belgilaydi. So'ng artefakt Hugging Face Model Hub'ga yuboriladi va qaytgan commit SHA `DISTILBERT_REVISION` sifatida ishlatiladi. Tokenni Colab Secrets yoki GitHub Secrets'da saqlang; kod hujayrasiga yozmang."""),
]


def validate(cells: list[dict]) -> None:
    for index, cell in enumerate(cells):
        if cell["cell_type"] == "code":
            line_count = len("".join(cell["source"]).splitlines())
            if line_count > 25:
                raise ValueError(f"Code cell {index} has {line_count} lines")
        if index and cell["cell_type"] == cells[index - 1]["cell_type"] == "code":
            raise ValueError(f"Consecutive code cells at {index - 1}/{index}")


validate(cells)
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
        "colab": {"name": OUTPUT.name, "provenance": []},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}
OUTPUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=1))
print(f"Wrote {OUTPUT} with {len(cells)} cells")
