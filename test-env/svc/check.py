from pathlib import Path

from flask import Flask
from pydantic import BaseModel, Field


app = Flask(__name__)   

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



@app.route('/skill/<skill>/check/<check>', methods=['GET'])
def check(skill: str, check: str):
    s = Settings.parse_file(Path(__file__).parent / 'settings.json')
    # Normalize to lowercase.
    skill = skill.lower()
    check = check.lower()

    # Find the skill.
    for s in s.skills:
        if s.ident.lower() == skill:
            # Find the check.
            for c in s.checks:
                if c.ident.lower() == check:
                    return c.value.lower(), 200
            return 'Check not found', 404    
    return 'Skill not found', 404


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8502)
    

    

