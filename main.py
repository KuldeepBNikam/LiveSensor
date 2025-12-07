from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, RedirectResponse
from uvicorn import run as app_run
import pandas as pd
import numpy as np
import os
import uuid
import sys

from sensor.logger import logging
from sensor.exception import SensorException
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.constant.application import APP_HOST, APP_PORT
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.utils.main_utils import load_object


# -----------------------------------------------------------
#                    FASTAPI APPLICATION
# -----------------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------
#                     ROUTES
# -----------------------------------------------------------

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train():
    try:
        training_pipeline = TrainPipeline()

        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")

        training_pipeline.run_pipeline()
        return Response("Training successfully completed!")

    except Exception as e:
        logging.exception(e)
        return Response(f"Error Occurred! {e}")


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read uploaded CSV file
        contents = await file.read()
        try:
            df = pd.read_csv(pd.io.common.BytesIO(contents))
            df = df.replace("na", np.nan)
        except Exception:
            return {"status": "error", "message": "Invalid CSV file"}

        # Remove target if present
        if "class" in df.columns:
            df = df.drop(columns=["class"])

        # Load best model
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)

        if not model_resolver.is_model_exists():
            return {"status": "error", "message": "Model not available"}

        best_model_path = model_resolver.get_best_model_path()
        model = load_object(best_model_path)

        # Predict
        y_pred = model.predict(df)
        df["predicted_class"] = y_pred

        # -----------------------------------------------------------
        #                    FIXED MAPPING (IMPORTANT FIX)
        # -----------------------------------------------------------
        mapping = TargetValueMapping().reverse_mapping()
        df["predicted_class"] = df["predicted_class"].replace(mapping)
        # -----------------------------------------------------------

        # Save output CSV
        os.makedirs("prediction_outputs", exist_ok=True)
        filename = f"prediction_{uuid.uuid4()}.csv"
        file_path = os.path.join("prediction_outputs", filename)
        df.to_csv(file_path, index=False)

        # Distribution for charts
        distribution = df["predicted_class"].value_counts().to_dict()

        # API Response
        return {
            "status": "success",
            "rows": len(df),
            "sample_predictions": df["predicted_class"].head(10).tolist(),
            "distribution": distribution,
            "download_file": filename,
        }

    except Exception as e:
        raise SensorException(e, sys)


# -----------------------------------------------------------
#                    MAIN EXECUTION
# -----------------------------------------------------------

def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        logging.exception(e)
        print(e)


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
