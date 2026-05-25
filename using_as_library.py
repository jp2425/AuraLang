from aura_lang import AuraLang

aura = AuraLang()
value = {
    "requested_index":3,
    "public_count": 3,
    "records": ["Document A", "Document B", "Document C", "Good Vibe Document", "flag{G00D_V1b3s_L4ngu4g3}"]
}
print(aura.run_program(open(r"C:\Users\nb30640\PycharmProjects\VibeLang\programs\level0.vibe" ).read(), value))