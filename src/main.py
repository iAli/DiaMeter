from app import app
from app import views
from predict_model import model_prediction
from followup_diabetes import weight_control, pressure_control, sugar_control


if __name__ == "__main__":
    app.run()
