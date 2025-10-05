"""
Trained Model Registry - Quản lý các trained models

Module này quản lý việc lưu trữ, tải và tracking các trained models
"""
import json
import logging
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime
from ..config import settings

logger = logging.getLogger(__name__)


class TrainedModelRegistry:
    """
    Quản lý registry của các trained models

    Tracking version, metrics, paths của models
    """

    def __init__(self, registry_path: Optional[Path] = None):
        """
        Khởi tạo Model Registry

        INPUT:
            registry_path: Path to registry JSON file (optional)
        """
        if registry_path is None:
            registry_path = settings.MODELS_DIR / "model_registry.json"

        self.registry_path = registry_path
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """
        Load registry từ file

        INPUT: None
        OUTPUT: Dictionary chứa registry data
        """
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading registry: {str(e)}")
                return {"models": []}
        else:
            return {"models": []}

    def _save_registry(self):
        """
        Lưu registry vào file

        INPUT: None
        OUTPUT: None
        SIDE EFFECTS: Ghi file registry
        """
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving registry: {str(e)}")
            raise

    def register_model(
        self,
        model_name: str,
        model_version: str,
        model_type: str,
        model_path: str,
        metrics: Optional[Dict[str, Any]] = None,
        is_active: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict:
        """
        Đăng ký một model mới vào registry

        INPUT:
            model_name: Tên model (vd: "vsl_gesture_recognizer")
            model_version: Version (vd: "v1.0.0", "20240101")
            model_type: Loại model ("vsl_recognition", "gesture", "emotion", etc.)
            model_path: Đường dẫn đến model file
            metrics: Dictionary chứa metrics (accuracy, f1_score, etc.)
            is_active: Model có đang active không
            metadata: Thông tin bổ sung
        OUTPUT:
            {
                'success': bool,
                'model_id': str,
                'message': str
            }
        """
        try:
            model_id = f"{model_name}_{model_version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            model_entry = {
                "id": model_id,
                "model_name": model_name,
                "model_version": model_version,
                "model_type": model_type,
                "model_path": model_path,
                "metrics": metrics or {},
                "is_active": is_active,
                "metadata": metadata or {},
                "created_at": datetime.now().isoformat()
            }

            self.registry["models"].append(model_entry)
            self._save_registry()

            logger.info(f"Model registered: {model_id}")
            return {
                "success": True,
                "model_id": model_id,
                "message": f"Model {model_name} registered successfully"
            }
        except Exception as e:
            logger.error(f"Error registering model: {str(e)}")
            return {
                "success": False,
                "model_id": None,
                "message": str(e)
            }

    def get_model(self, model_id: str) -> Optional[Dict]:
        """
        Lấy thông tin model theo ID

        INPUT:
            model_id: ID của model
        OUTPUT:
            Dictionary chứa thông tin model hoặc None nếu không tìm thấy
        """
        for model in self.registry["models"]:
            if model["id"] == model_id:
                return model
        return None

    def get_active_model(self, model_type: str) -> Optional[Dict]:
        """
        Lấy active model theo loại

        INPUT:
            model_type: Loại model ("vsl_recognition", "gesture", etc.)
        OUTPUT:
            Dictionary chứa thông tin model hoặc None nếu không tìm thấy
        """
        for model in self.registry["models"]:
            if model["model_type"] == model_type and model["is_active"]:
                return model
        return None

    def list_models(self, model_type: Optional[str] = None) -> List[Dict]:
        """
        Liệt kê tất cả models

        INPUT:
            model_type: Filter theo loại model (optional)
        OUTPUT:
            List of model dictionaries
        """
        if model_type:
            return [m for m in self.registry["models"] if m["model_type"] == model_type]
        return self.registry["models"]

    def set_active_model(self, model_id: str) -> Dict:
        """
        Đặt một model làm active (và deactivate các models khác cùng type)

        INPUT:
            model_id: ID của model cần activate
        OUTPUT:
            {
                'success': bool,
                'message': str
            }
        """
        try:
            target_model = self.get_model(model_id)
            if not target_model:
                return {
                    "success": False,
                    "message": f"Model {model_id} not found"
                }

            # Deactivate all models of same type
            for model in self.registry["models"]:
                if model["model_type"] == target_model["model_type"]:
                    model["is_active"] = False

            # Activate target model
            target_model["is_active"] = True
            self._save_registry()

            logger.info(f"Model {model_id} set as active")
            return {
                "success": True,
                "message": f"Model {model_id} is now active"
            }
        except Exception as e:
            logger.error(f"Error setting active model: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }

    def update_model_metrics(self, model_id: str, metrics: Dict[str, Any]) -> Dict:
        """
        Cập nhật metrics cho model

        INPUT:
            model_id: ID của model
            metrics: Dictionary chứa metrics mới
        OUTPUT:
            {
                'success': bool,
                'message': str
            }
        """
        try:
            model = self.get_model(model_id)
            if not model:
                return {
                    "success": False,
                    "message": f"Model {model_id} not found"
                }

            model["metrics"].update(metrics)
            model["updated_at"] = datetime.now().isoformat()
            self._save_registry()

            return {
                "success": True,
                "message": "Metrics updated successfully"
            }
        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }

    def delete_model(self, model_id: str) -> Dict:
        """
        Xóa model khỏi registry

        INPUT:
            model_id: ID của model cần xóa
        OUTPUT:
            {
                'success': bool,
                'message': str
            }
        NOTE: Chỉ xóa registry entry, không xóa model file
        """
        try:
            initial_count = len(self.registry["models"])
            self.registry["models"] = [
                m for m in self.registry["models"] if m["id"] != model_id
            ]

            if len(self.registry["models"]) < initial_count:
                self._save_registry()
                logger.info(f"Model {model_id} removed from registry")
                return {
                    "success": True,
                    "message": f"Model {model_id} removed successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Model {model_id} not found"
                }
        except Exception as e:
            logger.error(f"Error deleting model: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }


# Global instance
trained_model_registry = TrainedModelRegistry()
