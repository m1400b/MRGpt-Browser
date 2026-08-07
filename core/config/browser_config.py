"""
MRGpt Browser

Browser Configuration Manager

مدیریت تنظیمات مرورگر
"""


from __future__ import annotations


import json

from pathlib import Path



class BrowserConfig:


    def __init__(
        self,
        config_file="config/browser.json"
    ):


        self.path = Path(
            config_file
        )


        self.path.parent.mkdir(
            exist_ok=True
        )


        self.defaults = {

            "home_page":
                "https://www.google.com",


            "search_engine":
                "https://www.google.com/search?q={query}",


            "download_path":
                "downloads",


            "theme":
                "light",


            "javascript_enabled":
                True,


            "save_session":
                True,


            "user_agent":
                "MRGptBrowser/1.0"

        }


        self.data = {}

        self.load()



    # ----------------------------------

    def load(self):


        if not self.path.exists():

            self.data = (
                self.defaults.copy()
            )

            self.save()

            return



        try:

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:


                self.data = json.load(
                    file
                )


        except Exception:


            self.data = (
                self.defaults.copy()
            )


            self.save()



    # ----------------------------------

    def save(self):


        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as file:


            json.dump(

                self.data,

                file,

                indent=4,

                ensure_ascii=False

            )



    # ----------------------------------

    def get(
        self,
        key,
        default=None
    ):


        return self.data.get(
            key,
            default
        )



    # ----------------------------------

    def set(
        self,
        key,
        value
    ):


        self.data[key] = value

        self.save()



    # ----------------------------------

    def reset(self):


        self.data = (
            self.defaults.copy()
        )

        self.save()