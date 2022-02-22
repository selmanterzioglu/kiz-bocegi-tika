import libs
from structure_ui import init_and_run_UI
from structure_system import System_Object
from main_window_constructor import kiz_UI
# from main import kiz_UI


if __name__ == "__main__":
    # system_o = System_Object()
    # system_o.thread_print_info()
    
    app, ui = init_and_run_UI(
        title="Kız Böcegi TIKA Kontrol Yazilimi",
        Class_UI=kiz_UI,
        UI_File_Path="main_window_v2.ui"
    )
