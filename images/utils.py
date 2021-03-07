

def get_right_model_name(name):
    if name == 'pz_4':
        return ['Pz-4'], 'Pz-4'
    elif name == 'H_pz4':
        return ['Pz-4 F2', 'Pz-4 G', 'Pz-4 H', 'Pz-4 J'], 'Pz-4 F2 / Pz-4 G / Pz-4 H / Pz-4 J'
    elif name == 'E_pz4':
        return ['Pz-4 A', 'Pz-4 B', 'Pz-4 C', 'Pz-4 D', 'Pz-4 E', 'Pz-4 F1'], \
               'Pz-4 A / Pz-4 B / Pz-4 C / Pz-4 D / Pz-4 E / Pz-4 F1'
    elif name == 't_34':
        return ['T-34'], 'T-34'
    elif name == '41_t34':
        return ['T-34 (1941)'], 'T-34 образца 1941 года'
    elif name == '43_t34':
        return ['T-34 (1943)'], 'T-34 образца 1943 года'
    elif name == 'sIG33':
        return ['sIG-33 auf Pz-1 B'], '15 cm sIG 33 (mot S) auf Pz.Kpfw.I Ausf.B'


