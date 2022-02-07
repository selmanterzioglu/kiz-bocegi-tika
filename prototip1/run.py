import libs
from structure_ui import init_and_run_UI
from main_window_constructor import Ui_Camera_API_Main


if __name__ == "__main__":
    app, ui = init_and_run_UI(
        "Camera Developer UI",
        Ui_Camera_API_Main,
        UI_File_Path="main_window.ui"
    )
