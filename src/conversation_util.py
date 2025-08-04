from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from pathlib import Path
import json

class Slide(BaseModel):
    rol: str
    mensaje: str

class ConversationData(BaseModel):
    isStoryReply: bool = False
    slides: List[Slide]


def save_conversation_data(conversation_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Validar los datos con el modelo Pydantic
        validated_data = ConversationData(**conversation_data)
        
        # Asegurarse de que el directorio existe
        conversation_path = Path("static/js/conversation.json")
        conversation_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar en el archivo con formato legible
        with open(conversation_path, 'w', encoding='utf-8') as f:
            json.dump(validated_data.dict(), f, ensure_ascii=False, indent=2, default=str)
            
        return validated_data.dict()
        
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail={"error": "Datos de conversación no válidos", "details": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Error al guardar la conversación", "details": str(e)}
        )


def read_conversation_data() -> Optional[Dict[str, Any]]:
    conversation_path = Path("static/js/conversation.json")
    if not conversation_path.exists():
        return None
        
    try:
        with open(conversation_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Error al leer la conversación", "details": str(e)}
        )
