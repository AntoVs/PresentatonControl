import platform


def get_controller():

    system = platform.system()

    if system == "Linux":

        from backend.controller.linux_controller \
            import LinuxController

        return LinuxController()

    raise Exception(
        "Unsupported platform"
    )
