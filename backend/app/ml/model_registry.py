import os
import joblib
import logging
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class ModelRegistry:
    def __init__(self):
        self.models_dir = settings.MODELS_DIR
        os.makedirs(self.models_dir, exist_ok=True)
        self._loaded_models: Dict[str, Any] = {}

    def save_artifact(self, name: str, artifact: Any, metadata: Optional[Dict[str, Any]] = None):
        file_path = os.path.join(self.models_dir, f"{name}.joblib")
        joblib.dump(artifact, file_path)
        self._loaded_models[name] = artifact
        if metadata:
            meta_path = os.path.join(self.models_dir, f"{name}_meta.joblib")
            joblib.dump(metadata, meta_path)
        logger.info(f"Saved ML artifact {name} to {file_path}")

    def load_artifact(self, name: str) -> Optional[Any]:
        if name in self._loaded_models:
            return self._loaded_models[name]
        file_path = os.path.join(self.models_dir, f"{name}.joblib")
        if os.path.exists(file_path):
            try:
                artifact = joblib.load(file_path)
                self._loaded_models[name] = artifact
                return artifact
            except Exception as e:
                logger.error(f"Error loading artifact {name}: {e}")
                return None
        return None

    def get_metadata(self, name: str) -> Dict[str, Any]:
        meta_path = os.path.join(self.models_dir, f"{name}_meta.joblib")
        if os.path.exists(meta_path):
            try:
                return joblib.load(meta_path)
            except Exception:
                return {}
        return {}

    def is_model_available(self, name: str) -> bool:
        return (name in self._loaded_models) or os.path.exists(os.path.join(self.models_dir, f"{name}.joblib"))


registry = ModelRegistry()
