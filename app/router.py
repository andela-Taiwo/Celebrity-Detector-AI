import os
import base64
from typing import Optional, Union

from flask import Blueprint, render_template, request  # type: ignore
from app.agent.celebrity_detector import CelebrityDetector, CelebrityProfile
from app.agent.image_handler import process_image
from app.agent.qa_engine import QAEngine

router = Blueprint("router", __name__)

celebrity_detector = CelebrityDetector()
qa_engine = QAEngine()


@router.route("/", methods=["GET", "POST"])
def index():
    celebrity_info: Union[CelebrityProfile, str, None] = None
    result_img_data: Optional[str] = None
    user_question = ""
    answer = ""
    error = None

    if request.method == "POST":
        image_file = request.files.get("image")
        user_question = request.form.get("question", "").strip()

        if image_file and image_file.filename:
            image_bytes, face_box = process_image(image_file)
            if face_box is None:
                celebrity_info = "No face detected. Please try another image."
            else:
                celebrity_info = celebrity_detector.detect_celebrity(image_bytes)
                result_img_data = base64.b64encode(image_bytes).decode()

        elif user_question:
            player_name = request.form.get("player_name", "").strip()
            player_info_raw = request.form.get("player_info", "").strip()
            result_img_data = request.form.get("result_img_data")

            if not (player_name and player_info_raw and result_img_data):
                error = "Celebrity data missing. Please detect a celebrity before asking questions."
            else:
                celebrity_info = CelebrityProfile.from_response(player_info_raw)
                answer = qa_engine.ask_question_about_image(player_name, user_question)
        else:
            error = "Please upload an image or enter a question."

    return render_template(
        "index.html",
        player_info=celebrity_info,
        result_img_data=result_img_data,
        user_question=user_question,
        answer=answer,
        error=error,
    )
