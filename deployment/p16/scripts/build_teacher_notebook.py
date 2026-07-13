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
<g><rect x="226" y="75" width="150" height="92" rx="6" fill="#e9f6ee" stroke="#308451"/><text x="301" y="111" font-size="17" font-weight="700" fill="#205c38">O'qitish</text><text x="301" y="137" font-size="14" fill="#27333d">capstone LSTM</text></g>
<g><rect x="418" y="75" width="150" height="92" rx="6" fill="#fff2db" stroke="#b56a13"/><text x="493" y="111" font-size="17" font-weight="700" fill="#77450d">Artefakt</text><text x="493" y="137" font-size="14" fill="#27333d">Git revision</text></g>
<g><rect x="610" y="75" width="150" height="92" rx="6" fill="#f2eafb" stroke="#7551a6"/><text x="685" y="111" font-size="17" font-weight="700" fill="#513775">FastAPI</text><text x="685" y="137" font-size="14" fill="#27333d">test + metrics</text></g>
<g><rect x="802" y="75" width="144" height="92" rx="6" fill="#ffe9e6" stroke="#b34e43"/><text x="874" y="111" font-size="17" font-weight="700" fill="#79332c">Render</text><text x="874" y="137" font-size="14" fill="#27333d">deploy / rollback</text></g></g>
<g stroke="#65727e" stroke-width="2" marker-end="url(#a)"><path d="M184 121H216"/><path d="M376 121H408"/><path d="M568 121H600"/><path d="M760 121H792"/></g>
<text x="36" y="205" font-family="Arial" font-size="14" fill="#4e5b66">Har bosqichda artefakt, metrika va aniq revision saqlanadi.</text></svg>"""

LINEAGE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="980" height="240" viewBox="0 0 980 240">
<rect width="980" height="240" fill="#f7f8fa"/><text x="36" y="38" font-family="Arial" font-size="22" font-weight="700" fill="#17212b">Bitta model versiyasining kelib chiqishi</text>
<defs><marker id="b" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#65727e"/></marker></defs>
<g font-family="Arial"><rect x="42" y="75" width="210" height="54" rx="6" fill="#e5f1ff" stroke="#2878b5"/><text x="147" y="108" text-anchor="middle" font-size="16">dataset SHA</text><rect x="42" y="151" width="210" height="54" rx="6" fill="#e9f6ee" stroke="#308451"/><text x="147" y="184" text-anchor="middle" font-size="16">Git commit SHA</text>
<rect x="385" y="91" width="210" height="96" rx="6" fill="#fff2db" stroke="#b56a13"/><text x="490" y="126" text-anchor="middle" font-size="17" font-weight="700">MLflow run</text><text x="490" y="154" text-anchor="middle" font-size="14">parametr + metrika</text>
<rect x="728" y="91" width="210" height="96" rx="6" fill="#f2eafb" stroke="#7551a6"/><text x="833" y="126" text-anchor="middle" font-size="17" font-weight="700">Model artefakti</text><text x="833" y="154" text-anchor="middle" font-size="14">Git commit ichida</text></g>
<g stroke="#65727e" stroke-width="2" marker-end="url(#b)"><path d="M252 102H374"/><path d="M252 178H374"/><path d="M595 139H717"/></g></svg>"""

CICD_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="980" height="250" viewBox="0 0 980 250">
<rect width="980" height="250" fill="#f7f8fa"/><text x="36" y="38" font-family="Arial" font-size="22" font-weight="700" fill="#17212b">CI / CT / CD: uch xil mas'uliyat</text>
<defs><marker id="c" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#65727e"/></marker></defs>
<g font-family="Arial" text-anchor="middle"><rect x="36" y="78" width="250" height="108" rx="6" fill="#e5f1ff" stroke="#2878b5"/><text x="161" y="113" font-size="20" font-weight="700">CI</text><text x="161" y="141" font-size="15">test + Docker build</text><text x="161" y="165" font-size="13">har bir push</text>
<rect x="365" y="78" width="250" height="108" rx="6" fill="#e9f6ee" stroke="#308451"/><text x="490" y="113" font-size="20" font-weight="700">CT</text><text x="490" y="141" font-size="15">train + quality gate</text><text x="490" y="165" font-size="13">manual yoki yangi dataset</text>
<rect x="694" y="78" width="250" height="108" rx="6" fill="#fff2db" stroke="#b56a13"/><text x="819" y="113" font-size="20" font-weight="700">CD</text><text x="819" y="141" font-size="15">Render deploy</text><text x="819" y="165" font-size="13">CI o'tgan commit</text></g>
<g stroke="#65727e" stroke-width="2" marker-end="url(#c)"><path d="M286 132H354"/><path d="M615 132H683"/></g><text x="36" y="222" font-family="Arial" font-size="14" fill="#4e5b66">Rollback: Render oldingi muvaffaqiyatli build artefaktini qayta ishga tushiradi.</text></svg>"""


cells = [
    markdown("""# P16: NLP modelni production xizmatga chiqarish

**O'qituvchi demosiga mo'ljallangan 80 daqiqalik amaliy workshop.** Alohida student yoki solution notebook yo'q.

Bugun bitta to'liq yo'lni bajaramiz: avvalgi capstone LSTMni o'qitamiz, MLflow bilan tajribani qayd qilamiz, FastAPI orqali test qilamiz, Docker image quramiz va CI tekshiruvlaridan keyin Render'ga deploy qilamiz.

**Natija:** modelning o'zi bilan birga dataset, kod, metrika va deployment revisionlari ham kuzatiladi."""),
    markdown(svg_image("P16 MLOps oqimi", PIPELINE_SVG)),
    markdown("""## 0. Darsni boshlashdan oldin

GitHub'da **Actions -> P16 - CT train LSTM candidate -> Run workflow** ni ishga tushiring. Workflow fonda candidate artefakt yaratadi; Colab'da esa shu jarayonni bosqichma-bosqich ko'ramiz.

Render'da repository'dagi `render.yaml` Blueprint tanlanadi. Alohida model hosting hisobi yoki API key kerak emas. Render `main` branch'dagi GitHub CI tekshiruvlari o'tgach Docker service'ni yangilaydi."""),
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

- **PyTorch**: LSTM tensor hisoblari;
- **MLflow**: parametr, metrika, artefakt va lineage'ni run sifatida qayd qilish;
- **FastAPI + Pydantic**: HTTP endpoint va JSON validatsiyasi;
- **httpx**: lokal yoki public API'ga HTTP so'rov yuborish.

Colab'da PyTorch odatda tayyor. Qolgan versiyalar loyiha requirements faylidan olinadi."""),
    code("""import importlib.util

required = ["torch", "fastapi", "httpx", "mlflow"]
missing = [name for name in required if importlib.util.find_spec(name) is None]
if missing:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", str(DEPLOY_DIR / "requirements-notebook.txt")],
        check=True,
    )
print("Muhit tayyor. Yetishmagan paketlar:", missing or "yo'q")"""),
    markdown("""### Dars konfiguratsiyasi

Faqat capstone LSTM ishlatiladi. `RENDER_SERVICE_NAME` Blueprint va public URL'da bir xil nomni beradi. Public tekshiruv dars oxirida, Render deploy tugagach yoqiladi."""),
    code("""RUN_LSTM_TRAINING = True
LSTM_EPOCHS = 8

RENDER_SERVICE_NAME = "airi-nlp-p16"
RENDER_URL = f"https://{RENDER_SERVICE_NAME}.onrender.com"
CHECK_PUBLIC_RENDER = False

print("Production backend: LSTM")
print("Render URL:", RENDER_URL)"""),
    markdown("""## 2. Datasetni versiyalash

`dataset nomi` yetarli emas: repository ichidagi ma'lumot o'zgarishi mumkin. Lokal snapshot uchun SHA-256 hisoblaymiz. Shunda aynan qaysi misollar modelni hosil qilganini qayta topish mumkin."""),
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

MLflow bu darsda alohida server emas. Colab runtime ichidagi tracking papkasiga run yozamiz va jadval orqali tajribalarni solishtiramiz. Production'ga tasdiqlangan artefakt esa `deployment/p16/artifacts/lstm-v1` ichida saqlanadi; uni qaysi Git commit deploy qilganini Render ko'rsatadi."""),
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

MLflow run ID tajribani topadi; Git commit SHA esa production'dagi kod va model artefaktini topadi. Bu ikkisi bir xil narsa emas, lekin `config.json` dagi lineage orqali bir-biriga bog'lanadi."""),
    code("""runs = mlflow.search_runs(experiment_names=["p16-uzbek-sentiment"])
columns = [
    "run_id", "tags.mlflow.runName", "params.backend",
    "metrics.f1", "metrics.accuracy", "metrics.inference_time",
    "metrics.parameter_count", "metrics.artifact_size_mb",
]
available = [column for column in columns if column in runs.columns]
runs[available].head()"""),
    markdown("""## 5. Production backendni yuklash

Server LSTMni o'qitmaydi. U tayyor artefaktni CPU'ga bir marta yuklaydi va barcha so'rovlar uchun shu obyektni qayta ishlatadi."""),
    code("""from p16_service.backends import LSTMBackend
from p16_service.config import Settings

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
    markdown("""## 6. FastAPI: modelni HTTP shartnomasiga o'rash

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
    markdown("""## 7. Docker: bir xil runtime

FastAPI kirish nuqtasini beradi; Docker Python va kutubxona muhitini takrorlanuvchan qiladi. Tasdiqlangan LSTM og'irliklari, vocabulary va konfiguratsiya image ichiga qo'shiladi. Render aynan CI tekshirgan image ta'rifini quradi."""),
    code("""from IPython.display import Code, display

dockerfile = (DEPLOY_DIR / "Dockerfile").read_text()
display(Code(dockerfile, language="dockerfile"))"""),
    markdown(svg_image("CI CT CD oqimi", CICD_SVG)),
    markdown("""## 8. GitHub Actions va Render: pipeline'ni avtomatlashtirish

Loyiha ikkita GitHub Actions workflow va bitta Render Blueprint beradi:

1. `p16-ci.yml`: har push'da API test va Docker build;
2. `p16-train-lstm.yml`: manual continuous training, quality gate va candidate artefakt;
3. `render.yaml`: `main` branch CI tekshiruvlaridan o'tgach Docker service'ni deploy qilish.

CT'dan o'tgan candidate avtomatik production bo'lmaydi. Uni ko'rib chiqib, `artifacts/lstm-v1` o'rniga qo'yish va commit qilish model promotion hisoblanadi."""),
    code("""workflow_dir = REPO_ROOT / ".github/workflows"
for name in ["p16-ci.yml", "p16-train-lstm.yml"]:
    path = workflow_dir / name
    print(f"{name:24} {len(path.read_text().splitlines()):3} qator")

ci_lines = (workflow_dir / "p16-ci.yml").read_text().splitlines()
display(Code("\\n".join(ci_lines[18:36]), language="yaml"))
display(Code((REPO_ROOT / "render.yaml").read_text(), language="yaml"))"""),
    markdown("""### Quality gate

Yangi model avtomatik ravishda production'ga chiqmasligi kerak. CT workflow avval F1 va latency chegaralarini tekshiradi. Chegaradan o'tgan candidate yuklab olinadi, ko'rib chiqiladi va alohida commit bilan promotion qilinadi; shundan keyingina CI va Render CD ishlaydi."""),
    code("""quality_gate = (DEPLOY_DIR / "scripts/check_quality.py").read_text().splitlines()
display(Code("\\n".join(quality_gate[10:29]), language="python"))

metrics = lstm_result["metrics"]
approved = metrics["f1"] >= 0.70 and metrics["inference_time"] <= 100
print("Live LSTM deployment qarori:", "TASDIQLANDI" if approved else "RAD ETILDI")"""),
    markdown("""## 9. Public Render xizmatini tekshirish

Colab doimiy server emas. Render Docker container'ni public HTTPS URL bilan ishga tushiradi va `PORT` environment variable'ni o'zi beradi. Birinchi free-tier build yoki uyqudan uyg'onish biroz vaqt olishi mumkin."""),
    code("""import httpx

if CHECK_PUBLIC_RENDER:
    public_health = httpx.get(f"{RENDER_URL}/health", timeout=90)
    public_prediction = httpx.post(
        f"{RENDER_URL}/predict",
        json={"text": "Mahsulot sifati juda yaxshi"},
        timeout=90,
    )
    print("Public health:", public_health.status_code, public_health.json())
    print("Public output:", public_prediction.status_code, public_prediction.json())
else:
    print("Render deploy tugagach CHECK_PUBLIC_RENDER = True qiling.")"""),
    markdown("""## 10. Rollback: oldingi muvaffaqiyatli deployga qaytish

Render Dashboard'dagi **Events** bo'limidan oldingi muvaffaqiyatli deploy tanlanadi va **Rollback** bosiladi. Render oldingi build artefaktini qayta ishga tushiradi; repository tarixi esa qaysi model va kod versiyasi ekanini ko'rsatadi."""),
    code("""current_manifest = json.loads((DEPLOY_DIR / "deployment.json").read_text())
print("Hozirgi production manifest:")
print(json.dumps(current_manifest, indent=2))

render_lines = (REPO_ROOT / "render.yaml").read_text().splitlines()
print("\\nRender CD sozlamasi:")
print("\\n".join(line for line in render_lines if "autoDeploy" in line or "healthCheck" in line))"""),
    markdown("""## 11. Yakuniy tekshiruv

Workshop oxirida quyidagi savollarga javob bera olish kerak:

- Qaysi dataset va kod revisioni modelni hosil qildi?
- Nega MLflow run ID va Git commit SHA alohida?
- Nega server modelni har request'da yuklamaydi?
- CI, CT va CD nima bilan farq qiladi?
- Nega quality gate'dan o'tgan candidate avtomatik production bo'lmaydi?
- Nega rollback uchun oldingi artefakt saqlanishi shart?
- Render'dagi `PORT` qiymatini nima uchun kodga qattiq yozmaymiz?"""),
    code("""assert health.status_code == 200
assert response.status_code == 200
assert bad_response.status_code == 422
assert batch.status_code == 200
assert "model_version" in response.json()
assert "p95_latency_ms" in client.get("/metrics").json()
client.__exit__(None, None, None)
print("P16 lokal vertikal oqimi to'liq ishladi. [OK]")"""),
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
