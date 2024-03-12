import json
from pathlib import Path
from pydantic import BaseModel, Field
import streamlit as st


st.title('Skill Assessment Settings')


class Check(BaseModel):
    ident: str
    title: str
    value: str 


class Skill(BaseModel):
    ident: str
    title: str
    checks: list[Check]


class Settings(BaseModel):
    # The allowed outcomes for a check.
    valid_outcomes: list[str] = Field(default=['success', 'failure', 'error'])
    # The skills that are being assessed.
    skills: list[Skill] = Field(default=[])

    @property
    def settings(self):
        return Path(__file__).parent / 'settings.json'

    def save(self):
        with open(self.settings, 'w') as f:
            json.dump(self.model_dump(), f, indent=4)


    def load(self):
        with open(self.settings, 'r') as f:
            return self.parse_obj(json.load(f))


    def update_check(self, check: Check):
        if check.title in st.session_state:
            check.value = st.session_state[check.title]
            self.save()

    
    def view(self):
        for skill in st.session_state.settings.skills:
            with st.container(border=True):
                columns = st.columns(len(skill.checks))
                
                for i, check in enumerate(skill.checks):
                    ckey = check.title
                    indx = self.valid_outcomes.index(check.value)

                    with columns[i]:
                        st.radio(
                            check.title,
                            self.valid_outcomes,
                            key=ckey,
                            index=indx,
                            on_change=self.update_check,
                            args=(check,)
                        )
                


def ensure_settings():
    if 'settings' not in st.session_state:
        st.session_state.settings = Settings().load()
    return st.session_state.settings


with st.container():
    ensure_settings().view()
                