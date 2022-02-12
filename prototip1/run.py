import libs
from structure_ui import init_and_run_UI
from structure_system import System_Object
from main_window_constructor import Ui_Camera_API_Developer
# from main import Ui_Camera_API_Developer


if __name__ == "__main__":
    system_o = System_Object()
    system_o.thread_print_info()
    
    app, ui = init_and_run_UI(
        "Kız Böcegi TIKA Kontrol Yazilimi",
        Ui_Camera_API_Developer,
        UI_File_Path="main_window.ui"
    )
