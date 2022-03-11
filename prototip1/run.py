import libs
from structure_ui import init_and_run_UI
# from main_window_constructor import kiz_UI
from gui_test_script import kiz_UI

if __name__ == "__main__":
    
    app, ui = init_and_run_UI(
        title="Kiz Bocegi TIKA Control Software",
        Class_UI=kiz_UI,
        UI_File_Path="main_window_v1.ui"
    )

    # 