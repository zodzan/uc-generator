from uc_adapter import UseCaseAdapter

class LatexAdapter(UseCaseAdapter):

    def __init__(self):
        UseCaseAdapter.__init__(self)
        
        self.TEX_HEADER = \
                '\documentclass[a4paper, 11pt]{article}\n' \
                + '\\usepackage[T1]{fontenc}\n' \
                + '\\usepackage[utf8]{inputenc}\n' \
                + '\\usepackage[english]{babel}\n\n' \
                + '\\usepackage{enumitem}\n\n' \
                + '\\newcommand{\createsection}[1]{\\noindent\\textbf{#1}:}\n' \
                + '\\newcommand{\createextension}[2]{\\noindent\hspace*{0.8em}\\textbf{#1}: #2}\n\n' \
                + '\\newlist{extension}{enumerate}{1}\n' \
                + '\\setlist[extension]{label=\\arabic*., left=1.6em}\n\n'
        self.BEGIN = '\\begin{{{s}}}'
        self.END = '\end{{{s}}}'
        self.SUBSECTION = '\subsection{{{s}}}'
        self.SECTION = '\createsection{{{s}}} '
        self.EXTENSION_SECTION = '\createextension{{{s}}}{{{e}}}'
        self.ENUMERATE = 'enumerate'
        self.ITEMIZE = 'itemize'
        self.EXTENSION = 'extension'

        self.USE_CASE = '\n\n' + self._create_section('Use case')
        self.PRIMARY_ACTOR = '\n\n' + self._create_section('Primary actor')
        self.SCOPE = '\n\n' + self._create_section('Scope')
        self.LEVEL = '\n\n' + self._create_section('Level')
        self.STAKEHOLDERS = '\n\n' + self._create_section('Stakeholders')
        self.PRECONDITIONS = '\n\n' + self._create_section('Preconditions')
        self.POSTCONDITIONS = '\n\n' + self._create_section('Postconditions')
        self.NOMINAL_CASE = '\n\n' + self._create_section('Nominal case')
        self.EXTENSIONS = '\n\n' + self._create_section('Extensions')
        self.OTHER = '\n\n' + self._create_section('Other')

    def _reset_text_data(self):
        self.text_data['title'] = ''
        self.text_data['use_case'] = self.USE_CASE
        self.text_data['primary_actor'] = self.PRIMARY_ACTOR
        self.text_data['scope'] = self.SCOPE
        self.text_data['level'] = self.LEVEL
        self.text_data['stakeholders'] = self.STAKEHOLDERS
        self.text_data['preconditions'] = self.PRECONDITIONS
        self.text_data['postconditions'] = self.POSTCONDITIONS
        self.text_data['nominal_case'] = self.NOMINAL_CASE
        self.text_data['extensions'] = self.EXTENSIONS
        self.text_data['other'] = self.OTHER

    def _create_section(self, section):
        return self.SECTION.format(s=section)

    def _create_extension(self, extension, nominal_step):
        s = 'Extension ' + str(nominal_step)
        return '\n' + self.EXTENSION_SECTION.format(s=s, e=extension)

    def _create_list(self, list_type, items):
        list_str = '\n' + self.BEGIN.format(s=list_type) + '\n'
        for i in items:
            list_str += '\item ' + i + '\n'
        list_str += self.END.format(s=list_type)
        return list_str

    def _create_extension_steps(self, nominal_step, steps):
        list_str = '\n' + self.BEGIN.format(s=self.EXTENSION)
        list_str += '[label={ns}.\\arabic*]\n'.format(ns=nominal_step)
        for s in steps:
            list_str += '\item ' + s + '\n'
        list_str += self.END.format(s=self.EXTENSION)
        return list_str

    def convert_data(self, json_data):
        UseCaseAdapter.convert_data(self, json_data)
        self._reset_text_data()
        
        title_str = self.data['id'] + ': ' + self.data['use_case']
        self.text_data['title'] = self.SUBSECTION.format(s=title_str)
        self.text_data['use_case'] += self.data['use_case']
        self.text_data['primary_actor'] += self.data['primary_actor']
        self.text_data['scope'] += self.data['scope']
        self.text_data['level'] += self.data['level']
        self.text_data['other'] += self.data['other']

        stakeholders = self.data['stakeholders']
        stakeholders_text = ''
        if len(stakeholders) > 1:
            goals = [stakeholder['goal'] for stakeholder in stakeholders]
            stakeholders_text = self._create_list(self.ITEMIZE, goals)
        elif len(stakeholders) > 0:
            stakeholders_text = stakeholders[0]['goal']
        self.text_data['stakeholders'] += stakeholders_text

        preconditions = self.data['preconditions']
        preconditions_text = self._create_list(self.ENUMERATE, preconditions)
        self.text_data['preconditions'] += preconditions_text

        postconditions = self.data['postconditions']
        postconditions_text = self._create_list(self.ENUMERATE, postconditions)
        self.text_data['postconditions'] += postconditions_text
        
        nominal_steps = self.data['nominal_case']
        nominal_case_text = self._create_list(self.ENUMERATE, nominal_steps)
        self.text_data['nominal_case'] += nominal_case_text

        extensions = self.data['extensions']
        extensions_text = '\n\n\\vspace{1em}'
        for e in extensions:
            e_text = self._create_extension(e['extension'], e['nominal_step'])
            e_text += self._create_extension_steps(e['nominal_step'], e['steps'])
            extensions_text += e_text
        self.text_data['extensions'] += extensions_text


    def export(self, fp):
        with open(fp, 'w') as f:
            f_text = self.TEX_HEADER \
                    + self.BEGIN.format(s='document') \
                    + self.text_data['title'] \
                    + self.text_data['use_case'] \
                    + self.text_data['primary_actor'] \
                    + self.text_data['scope'] \
                    + self.text_data['level'] \
                    + self.text_data['stakeholders'] \
                    + self.text_data['preconditions'] \
                    + self.text_data['postconditions'] \
                    + self.text_data['nominal_case'] \
                    + self.text_data['extensions'] \
                    + self.text_data['other'] \
                    + '\n\n' \
                    + self.END.format(s='document')

            f.write(f_text)
            f.close()
