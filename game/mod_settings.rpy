
init python:
    import os
    import hashlib

    def is_original_file(path):
        if path.endswith("audio.rpa"):
            return hashlib.sha256(open(path, "rb").read()).hexdigest() == '121fedc50823e2a76d947025cc0f2dfa7c64b2454760b50091a64d1d36b7d2e7'
        elif path.endswith("fonts.rpa"):
            return hashlib.sha256(open(path, "rb").read()).hexdigest() == 'd48beafa7e1f3171b0e8e312f857af0e7eb387ef1e524a5be2595d46652d2018'
        elif path.endswith("images.rpa"):
            return hashlib.sha256(open(path, "rb").read()).hexdigest() == '6c3dccd4f35723ca1679b95710d4d09cec3d22439e24264bc6ff60d90640d393'
        elif path.endswith("scripts.rpa"):
            return hashlib.sha256(open(path, "rb").read()).hexdigest() == 'da7ba6d3cf9ec1ae666ec29ae07995a65d24cca400cd266e470deb55e03a51d4'

    def transfer_data(ddmm_path):
        modsTransferred = []
        try:
            for dirs in os.listdir(ddmm_path):
                if not os.path.exists(os.path.join(persistent.ddml_basedir, "game/mods", dirs)):
                    modsTransferred.append(dirs)
                    os.makedirs(os.path.join(persistent.ddml_basedir, "game/mods", dirs))
                    os.makedirs(os.path.join(persistent.ddml_basedir, "game/mods", dirs, "game"))

                    for ddmm_src, mod_dirs, mod_files in os.walk(ddmm_path + "/" + dirs):
                        dst_dir = ddmm_src.replace(ddmm_path + "/" + dirs, os.path.join(persistent.ddml_basedir, "game/mods", dirs))
                        for d in mod_dirs:
                            if d == "characters":
                                shutil.copytree(os.path.join(ddmm_src, d), os.path.join(dst_dir, d))
                        for f in mod_files:
                            if f.endswith((".rpa", ".rpyc", ".rpy")):
                                if not f.startswith("00"):
                                    mod_dir = ddmm_src
                                    break

                    for ddmm_src, mod_dirs, mod_files in os.walk(mod_dir):
                        dst_dir = ddmm_src.replace(mod_dir, os.path.join(persistent.ddml_basedir, "game/mods", dirs, "game"))
                        for mod_d in mod_dirs:
                            shutil.copytree(os.path.join(ddmm_src, mod_d), os.path.join(dst_dir, mod_d))
                        for mod_f in mod_files:
                            if mod_f.endswith(".rpa"):
                                if is_original_file(os.path.join(ddmm_src, mod_f)):
                                    continue
                            shutil.copy2(os.path.join(ddmm_src, mod_f), os.path.join(dst_dir, mod_f))

            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="Transferred all data sucessfully.")
        except OSError as err:
            if modsTransferred and os.path.exists(os.path.join(persistent.ddml_basedir, "game/mods", modsTransferred[-1])):
                shutil.rmtree(os.path.join(persistent.ddml_basedir, "game/mods", modsTransferred[-1]))
            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="A error has occured while transferring.", message2=str(err))
        except Exception as err:
            if modsTransferred and os.path.exists(os.path.join(persistent.ddml_basedir, "game/mods", modsTransferred[-1])):
                shutil.rmtree(os.path.join(persistent.ddml_basedir, "game/mods", modsTransferred[-1]))
            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="A unknown error has occured while transferring.", message2=str(err))

    def transfer_ddmm_data():
        if not renpy.windows:
            renpy.show_screen("ddmd_dialog", message="Transferring data from DDMM is only supported on Windows.")
            return
        renpy.show_screen("ddmd_progress", message="Transferring data. Please wait.")
        ddmm_path = os.path.join(
            os.getenv("APPDATA"), "DokiDokiModManager/GameData/installs"
        )
        if os.path.exists(ddmm_path):
            transfer_data(ddmm_path)
        else:
            renpy.show_screen("ddmd_dialog", message="Error: We were unable to locate a Doki Doki Manager folder in your AppData folder.", message2="If this is in error, please report it on Github.")

    def transfer_ddml_data():
        renpy.transition(Dissolve(0.25))
        renpy.show_screen("install_folder_directory")

screen mod_settings():
    zorder 101
    style_prefix "modSettings"

    drag:
        drag_name "msettings"
        drag_handle (0, 0, 1.0, 40)
        xsize 500
        ysize 300
        xpos 0.3
        ypos 0.3
        
        frame:
            hbox:
                ypos 0.005
                xalign 0.52 
                text "Settings"

            hbox:
                ypos -0.005
                xalign 0.98
                imagebutton:
                    idle "ddmd_close_icon"
                    hover "ddmd_close_icon_hover"
                    action Hide("mod_settings", Dissolve(0.25))

            side "c":
                xpos 0.05
                ypos 0.15
                xsize 450
                ysize 250
                spacing 5

                viewport id "msw":
                    mousewheel True
                    draggable True
                    has vbox
                    spacing 1

                    imagebutton:
                        idle ConditionSwitch("config.gl2", Composite((250, 40), (0, 0), "ddmd_toggle_on",
                            (55, 13), Text("Enable OpenGL 2 Globally", style="modSettings_text", size=18)), "True",
                            Composite((250, 40), (0, 0), "ddmd_toggle_off", (55, 13), 
                            Text("Enable OpenGL 2 Globally", style="modSettings_text", size=18)))
                        hover ConditionSwitch("config.gl2", Composite((250, 40), (0, 0), "ddmd_toggle_on_hover",
                            (55, 14), Text("Enable OpenGL 2 Globally", style="modSettings_text", size=18)), "True", 
                            Composite((250, 40), (0, 0), "ddmd_toggle_off_hover", (55, 13), Text("Enable OpenGL 2 Globally", 
                            style="modSettings_text", size=18)))
                        action If(config.gl2, Show("ddmd_confirm", Dissolve(0.25), message="Disable OpenGL 2?", 
                            message2="Some mods may not have certain effects display if this setting is turned off. {b}A restart is required to load OpenGL 2{/b}.", 
                            yes_action=[SetField(config, "gl2", False), Function(set_settings_json), Quit()], no_action=Hide("ddmd_confirm", 
                            Dissolve(0.25))), Show("ddmd_confirm", Dissolve(0.25), message="Enable OpenGL 2?", 
                            message2="Some mods may suffer from broken affects if this setting is turned on. {b}A restart is required to load OpenGL 2{/b}.", 
                            yes_action=[SetField(config, "gl2", True), Function(set_settings_json), Quit()], no_action=Hide("ddmd_confirm", 
                            Dissolve(0.25))))

                    imagebutton:
                        idle ConditionSwitch("persistent.military_time", Composite((250, 40), (0, 0), "ddmd_toggle_on",
                            (55, 13), Text("Use 24-Hour Format", style="modSettings_text", size=18)), "True",
                            Composite((250, 40), (0, 0), "ddmd_toggle_off", (55, 13), 
                            Text("Use 24-Hour Format", style="modSettings_text", size=18)))
                        hover ConditionSwitch("persistent.military_time", Composite((250, 40), (0, 0), "ddmd_toggle_on_hover",
                            (55, 14), Text("Use 24-Hour Format", style="modSettings_text", size=18)), "True", 
                            Composite((250, 40), (0, 0), "ddmd_toggle_off_hover", (55, 13), Text("Use 24-Hour Format", 
                            style="modSettings_text", size=18)))
                        action [If(persistent.military_time, SetField(persistent, "military_time", False),
                            SetField(persistent, "military_time", True))]

                    imagebutton:
                        idle Composite((410, 40), (0, 0), "ddmd_transfer_icon", (55, 7), 
                            Text("[Beta] Transfer DDMM Mods to DDMD", style="modSettings_text", substitute=False, size=18))
                        hover Composite((410, 40), (0, 0), "ddmd_transfer_icon_hover", (55, 7), 
                            Text("[Beta] Transfer DDMM Mods to DDMD", style="modSettings_text", substitute=False, size=18))
                        action If(not persistent.transfer_warning, Show("ddmd_confirm", message="Transfer Warning", 
                            message2="Transferring mods is in beta and some mods may not work due to Ren'Py version differences. By accepting this disclaimer, transferring will proceed.", 
                            yes_action=[SetField(persistent, "transfer_warning", True), Hide("ddmd_confirm"), Function(transfer_ddmm_data)], 
                            no_action=Hide("ddmd_confirm")), Function(transfer_ddmm_data))

                    imagebutton:
                        idle Composite((410, 40), (0, 0), "ddmd_transfer_icon", (55, 7), 
                            Text("[Beta] Transfer DDML Mods to DDMD", style="modSettings_text", substitute=False, size=18))
                        hover Composite((410, 40), (0, 0), "ddmd_transfer_icon_hover", (55, 7), 
                            Text("[Beta] Transfer DDML Mods to DDMD", style="modSettings_text", substitute=False, size=18))
                        action If(not persistent.transfer_warning, Show("ddmd_confirm", message="Transfer Warning", 
                            message2="Transferring mods is in beta and some mods may not work due to Ren'Py version differences. By accepting this disclaimer, transferring will proceed.", 
                            yes_action=[SetField(persistent, "transfer_warning", True), Hide("ddmd_confirm"), Function(transfer_ddml_data)], 
                            no_action=Hide("ddmd_confirm")), Function(transfer_ddml_data))
