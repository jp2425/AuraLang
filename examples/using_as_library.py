from aura_lang import AuraLang

aura = AuraLang()
value = {
    "X":3
}
print(aura.run_program(open(r"/programs/program.vibe", ).read(), value))